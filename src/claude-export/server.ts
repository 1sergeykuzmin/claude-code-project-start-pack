/**
 * Web server for viewing dialog exports
 */

import express, { Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';
import { ServerOptions, DEFAULT_SERVER_OPTIONS, DialogSummary } from './types';

/**
 * Start the dialog viewer web server
 */
export async function startServer(
  options: ServerOptions = DEFAULT_SERVER_OPTIONS
): Promise<void> {
  const app = express();
  const { port, host, dialogDir, openBrowser } = options;

  // Ensure dialog directory exists
  if (!fs.existsSync(dialogDir)) {
    fs.mkdirSync(dialogDir, { recursive: true });
  }

  // Dashboard route
  app.get('/', (req: Request, res: Response) => {
    const dialogs = getDialogList(dialogDir);
    const html = renderDashboard(dialogs);
    res.send(html);
  });

  // Individual dialog view
  app.get('/dialog/:id', (req: Request, res: Response) => {
    const { id } = req.params;
    const filePath = findDialogFile(dialogDir, id);

    if (!filePath) {
      res.status(404).send(render404(id));
      return;
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const html = renderDialog(id, content, filePath);
    res.send(html);
  });

  // Search route
  app.get('/search', (req: Request, res: Response) => {
    const query = (req.query.q as string) || '';
    const results = searchDialogs(dialogDir, query);
    const html = renderSearchResults(query, results);
    res.send(html);
  });

  // API: List dialogs as JSON
  app.get('/api/dialogs', (req: Request, res: Response) => {
    const dialogs = getDialogList(dialogDir);
    res.json(dialogs);
  });

  // API: Get single dialog
  app.get('/api/dialog/:id', (req: Request, res: Response) => {
    const { id } = req.params;
    const filePath = findDialogFile(dialogDir, id);

    if (!filePath) {
      res.status(404).json({ error: 'Dialog not found' });
      return;
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    res.json({ id, content, path: filePath });
  });

  // Static file serving for dialog directory
  app.use('/files', express.static(dialogDir));

  // Start server
  return new Promise((resolve) => {
    app.listen(port, host, () => {
      const url = `http://${host}:${port}`;
      console.log(`Dialog viewer running at ${url}`);
      console.log(`Serving dialogs from: ${path.resolve(dialogDir)}`);
      console.log('');
      console.log('Press Ctrl+C to stop.');

      // Open browser if requested
      if (openBrowser) {
        openInBrowser(url);
      }

      resolve();
    });
  });
}

/**
 * Get list of dialog files
 */
function getDialogList(dialogDir: string): DialogSummary[] {
  const dialogs: DialogSummary[] = [];

  if (!fs.existsSync(dialogDir)) {
    return dialogs;
  }

  const files = fs.readdirSync(dialogDir);

  for (const file of files) {
    if (!file.endsWith('.md') && !file.endsWith('.html') && !file.endsWith('.json')) {
      continue;
    }

    const filePath = path.join(dialogDir, file);
    const stat = fs.statSync(filePath);

    // Get preview from first few lines
    let preview = '';
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.split('\n').slice(0, 10);
      preview = lines
        .filter((l) => l && !l.startsWith('#') && !l.startsWith('---'))
        .join(' ')
        .substring(0, 150);
    } catch {
      // Ignore read errors
    }

    dialogs.push({
      id: path.basename(file, path.extname(file)),
      filename: file,
      date: stat.mtime.toISOString(),
      messageCount: 0, // Would need to parse to get accurate count
      preview,
      exported: true,
      exportPath: filePath,
    });
  }

  // Sort by date, newest first
  dialogs.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return dialogs;
}

/**
 * Find a dialog file by ID
 */
function findDialogFile(dialogDir: string, id: string): string | null {
  const extensions = ['.md', '.html', '.json'];

  for (const ext of extensions) {
    const filePath = path.join(dialogDir, `${id}${ext}`);
    if (fs.existsSync(filePath)) {
      return filePath;
    }
  }

  return null;
}

/**
 * Search dialogs for a query
 */
function searchDialogs(
  dialogDir: string,
  query: string
): Array<{ dialog: DialogSummary; matches: string[] }> {
  const results: Array<{ dialog: DialogSummary; matches: string[] }> = [];
  const dialogs = getDialogList(dialogDir);
  const queryLower = query.toLowerCase();

  for (const dialog of dialogs) {
    if (!dialog.exportPath) continue;

    try {
      const content = fs.readFileSync(dialog.exportPath, 'utf-8');
      const contentLower = content.toLowerCase();

      if (contentLower.includes(queryLower)) {
        // Find matching lines
        const lines = content.split('\n');
        const matches: string[] = [];

        for (let i = 0; i < lines.length; i++) {
          if (lines[i].toLowerCase().includes(queryLower)) {
            const context = lines
              .slice(Math.max(0, i - 1), i + 2)
              .join(' ')
              .substring(0, 200);
            matches.push(context);
            if (matches.length >= 3) break;
          }
        }

        results.push({ dialog, matches });
      }
    } catch {
      // Ignore read errors
    }
  }

  return results;
}

/**
 * Open URL in default browser
 */
function openInBrowser(url: string): void {
  const { exec } = require('child_process');
  const platform = process.platform;

  let command: string;
  if (platform === 'darwin') {
    command = `open "${url}"`;
  } else if (platform === 'win32') {
    command = `start "${url}"`;
  } else {
    command = `xdg-open "${url}"`;
  }

  exec(command, (err: Error | null) => {
    if (err) {
      console.log(`Could not open browser automatically. Visit: ${url}`);
    }
  });
}

// --- HTML Templates ---

const CSS = `
<style>
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    line-height: 1.6;
    color: #333;
    background: #f5f5f5;
  }
  h1 { color: #4A90D9; margin-bottom: 10px; }
  .subtitle { color: #666; margin-bottom: 30px; }
  .search-form {
    margin-bottom: 30px;
    display: flex;
    gap: 10px;
  }
  .search-form input {
    flex: 1;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
  }
  .search-form button {
    padding: 10px 20px;
    background: #4A90D9;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  .search-form button:hover { background: #3a7bc8; }
  .card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .card h2 {
    margin: 0 0 10px 0;
    font-size: 18px;
  }
  .card h2 a { color: #4A90D9; text-decoration: none; }
  .card h2 a:hover { text-decoration: underline; }
  .card .meta { color: #666; font-size: 14px; margin-bottom: 10px; }
  .card .preview { color: #555; font-size: 14px; }
  .content {
    background: white;
    border-radius: 8px;
    padding: 30px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .content h1 { font-size: 24px; }
  .content h2 { font-size: 20px; margin-top: 30px; color: #4A90D9; }
  .content pre {
    background: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
  }
  .content code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
  .back-link { margin-bottom: 20px; }
  .back-link a { color: #4A90D9; }
  .no-results { text-align: center; padding: 40px; color: #666; }
  .match { background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 4px; }
</style>
`;

function renderDashboard(dialogs: DialogSummary[]): string {
  const dialogCards = dialogs.map((d) => `
    <div class="card">
      <h2><a href="/dialog/${d.id}">${d.id}</a></h2>
      <div class="meta">${new Date(d.date).toLocaleString()}</div>
      <div class="preview">${escapeHtml(d.preview)}...</div>
    </div>
  `).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude Dialog Viewer</title>
  ${CSS}
</head>
<body>
  <h1>Claude Dialog Viewer</h1>
  <p class="subtitle">${dialogs.length} dialog(s) available</p>

  <form class="search-form" action="/search" method="get">
    <input type="text" name="q" placeholder="Search dialogs..." />
    <button type="submit">Search</button>
  </form>

  ${dialogs.length > 0 ? dialogCards : '<div class="no-results">No dialogs found. Export some sessions first.</div>'}
</body>
</html>`;
}

function renderDialog(id: string, content: string, filePath: string): string {
  const marked = require('marked');
  const ext = path.extname(filePath);

  let renderedContent: string;
  if (ext === '.md') {
    renderedContent = marked.parse(content);
  } else if (ext === '.html') {
    renderedContent = content;
  } else {
    renderedContent = `<pre>${escapeHtml(content)}</pre>`;
  }

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dialog: ${id}</title>
  ${CSS}
</head>
<body>
  <div class="back-link"><a href="/">&larr; Back to Dashboard</a></div>
  <div class="content">
    ${renderedContent}
  </div>
</body>
</html>`;
}

function renderSearchResults(
  query: string,
  results: Array<{ dialog: DialogSummary; matches: string[] }>
): string {
  const resultCards = results.map((r) => `
    <div class="card">
      <h2><a href="/dialog/${r.dialog.id}">${r.dialog.id}</a></h2>
      <div class="meta">${new Date(r.dialog.date).toLocaleString()}</div>
      ${r.matches.map((m) => `<div class="match">${escapeHtml(m)}</div>`).join('')}
    </div>
  `).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Search: ${escapeHtml(query)}</title>
  ${CSS}
</head>
<body>
  <div class="back-link"><a href="/">&larr; Back to Dashboard</a></div>
  <h1>Search Results</h1>
  <p class="subtitle">Query: "${escapeHtml(query)}" - ${results.length} result(s)</p>

  <form class="search-form" action="/search" method="get">
    <input type="text" name="q" value="${escapeHtml(query)}" placeholder="Search dialogs..." />
    <button type="submit">Search</button>
  </form>

  ${results.length > 0 ? resultCards : '<div class="no-results">No results found.</div>'}
</body>
</html>`;
}

function render404(id: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Not Found</title>
  ${CSS}
</head>
<body>
  <div class="back-link"><a href="/">&larr; Back to Dashboard</a></div>
  <div class="no-results">
    <h1>Dialog Not Found</h1>
    <p>The dialog "${escapeHtml(id)}" could not be found.</p>
  </div>
</body>
</html>`;
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
