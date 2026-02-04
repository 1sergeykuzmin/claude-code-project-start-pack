/**
 * Session exporter - converts Claude sessions to various formats
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import {
  Session,
  Message,
  ExportOptions,
  DialogSummary,
  CREDENTIAL_PATTERNS,
  REDACTION_TEXT,
  DEFAULT_EXPORT_OPTIONS,
} from './types';

/**
 * Standard session directories to search
 */
const SESSION_DIRS = [
  path.join(os.homedir(), '.claude', 'projects'),
  path.join(process.cwd(), '.claude', 'sessions'),
];

/**
 * Find all Claude session files
 */
export async function findSessions(): Promise<Session[]> {
  const sessions: Session[] = [];

  for (const baseDir of SESSION_DIRS) {
    if (!fs.existsSync(baseDir)) {
      continue;
    }

    try {
      const entries = await findSessionFiles(baseDir);
      for (const entry of entries) {
        try {
          const session = await parseSessionFile(entry);
          if (session) {
            sessions.push(session);
          }
        } catch {
          // Skip invalid session files
        }
      }
    } catch {
      // Skip inaccessible directories
    }
  }

  // Sort by timestamp, newest first
  sessions.sort((a, b) =>
    new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  );

  return sessions;
}

/**
 * Recursively find session files (*.jsonl)
 */
async function findSessionFiles(dir: string): Promise<string[]> {
  const files: string[] = [];

  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      const subFiles = await findSessionFiles(fullPath);
      files.push(...subFiles);
    } else if (entry.name.endsWith('.jsonl')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Parse a session file into a Session object
 */
async function parseSessionFile(filePath: string): Promise<Session | null> {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);

    if (lines.length === 0) {
      return null;
    }

    const messages: Message[] = [];
    let firstTimestamp = '';

    for (const line of lines) {
      try {
        const entry = JSON.parse(line);

        // Extract message based on entry type
        if (entry.type === 'user' || entry.type === 'human') {
          messages.push({
            role: 'user',
            content: extractContent(entry),
            timestamp: entry.timestamp,
          });
        } else if (entry.type === 'assistant' || entry.type === 'ai') {
          messages.push({
            role: 'assistant',
            content: extractContent(entry),
            timestamp: entry.timestamp,
            tool_calls: entry.tool_calls || entry.toolCalls,
          });
        } else if (entry.type === 'system') {
          messages.push({
            role: 'system',
            content: extractContent(entry),
            timestamp: entry.timestamp,
          });
        }

        // Track first timestamp
        if (!firstTimestamp && entry.timestamp) {
          firstTimestamp = entry.timestamp;
        }
      } catch {
        // Skip malformed lines
      }
    }

    if (messages.length === 0) {
      return null;
    }

    // Generate session ID from filename
    const sessionId = path.basename(filePath, '.jsonl');

    return {
      id: sessionId,
      timestamp: firstTimestamp || new Date().toISOString(),
      messages,
      metadata: {
        messageCount: messages.length,
        toolCallCount: messages.reduce(
          (count, m) => count + (m.tool_calls?.length || 0),
          0
        ),
      },
    };
  } catch {
    return null;
  }
}

/**
 * Extract content from various entry formats
 */
function extractContent(entry: Record<string, unknown>): string {
  if (typeof entry.content === 'string') {
    return entry.content;
  }
  if (entry.message && typeof entry.message === 'string') {
    return entry.message;
  }
  if (Array.isArray(entry.content)) {
    return entry.content
      .map((c: { text?: string; type?: string }) => c.text || '')
      .join('\n');
  }
  return '';
}

/**
 * Redact credentials from content
 */
export function redactCredentials(content: string): string {
  let redacted = content;

  for (const pattern of CREDENTIAL_PATTERNS) {
    redacted = redacted.replace(pattern, REDACTION_TEXT);
  }

  return redacted;
}

/**
 * Convert session to Markdown format
 */
export function toMarkdown(
  session: Session,
  options: ExportOptions = DEFAULT_EXPORT_OPTIONS
): string {
  const lines: string[] = [];

  // YAML frontmatter
  if (options.includeFrontmatter) {
    lines.push('---');
    lines.push(`id: ${session.id}`);
    lines.push(`date: ${session.timestamp}`);
    lines.push(`messages: ${session.messages.length}`);
    if (session.metadata.project) {
      lines.push(`project: ${session.metadata.project}`);
    }
    lines.push('---');
    lines.push('');
  }

  // Title
  const dateStr = new Date(session.timestamp).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
  lines.push(`# Claude Session - ${dateStr}`);
  lines.push('');

  // Messages
  for (const message of session.messages) {
    // Role header
    const roleIcon = message.role === 'user' ? '👤' : message.role === 'assistant' ? '🤖' : '⚙️';
    const roleLabel = message.role.charAt(0).toUpperCase() + message.role.slice(1);
    lines.push(`## ${roleIcon} ${roleLabel}`);
    lines.push('');

    // Content (optionally redacted)
    let content = message.content;
    if (options.redact) {
      content = redactCredentials(content);
    }
    lines.push(content);
    lines.push('');

    // Tool calls
    if (options.includeToolCalls && message.tool_calls?.length) {
      lines.push('<details>');
      lines.push('<summary>Tool Calls</summary>');
      lines.push('');
      for (const call of message.tool_calls) {
        lines.push(`**${call.name}**`);
        lines.push('```json');
        lines.push(JSON.stringify(call.input, null, 2));
        lines.push('```');
        if (call.output) {
          lines.push('Output:');
          lines.push('```');
          let output = call.output;
          if (options.redact) {
            output = redactCredentials(output);
          }
          // Truncate long outputs
          if (output.length > 1000) {
            output = output.substring(0, 1000) + '\n... (truncated)';
          }
          lines.push(output);
          lines.push('```');
        }
        lines.push('');
      }
      lines.push('</details>');
      lines.push('');
    }

    lines.push('---');
    lines.push('');
  }

  return lines.join('\n');
}

/**
 * Convert session to HTML format
 */
export function toHTML(
  session: Session,
  options: ExportOptions = DEFAULT_EXPORT_OPTIONS
): string {
  const marked = require('marked');
  const markdown = toMarkdown(session, { ...options, includeFrontmatter: false });
  const htmlContent = marked.parse(markdown);

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude Session - ${session.id}</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      line-height: 1.6;
      color: #333;
    }
    h1 { border-bottom: 2px solid #4A90D9; padding-bottom: 10px; }
    h2 { margin-top: 30px; color: #4A90D9; }
    pre {
      background: #f4f4f4;
      padding: 15px;
      border-radius: 5px;
      overflow-x: auto;
    }
    code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
    hr { border: none; border-top: 1px solid #ddd; margin: 30px 0; }
    details { margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 5px; }
    summary { cursor: pointer; font-weight: bold; }
  </style>
</head>
<body>
  ${htmlContent}
</body>
</html>`;
}

/**
 * Convert session to JSON format
 */
export function toJSON(
  session: Session,
  options: ExportOptions = DEFAULT_EXPORT_OPTIONS
): string {
  if (options.redact) {
    const redactedSession = {
      ...session,
      messages: session.messages.map((m) => ({
        ...m,
        content: redactCredentials(m.content),
        tool_calls: m.tool_calls?.map((tc) => ({
          ...tc,
          output: tc.output ? redactCredentials(tc.output) : undefined,
        })),
      })),
    };
    return JSON.stringify(redactedSession, null, 2);
  }
  return JSON.stringify(session, null, 2);
}

/**
 * Export a single session
 */
export async function exportSession(
  sessionId: string,
  options: ExportOptions = DEFAULT_EXPORT_OPTIONS
): Promise<DialogSummary | null> {
  const sessions = await findSessions();
  const session = sessions.find((s) => s.id === sessionId);

  if (!session) {
    return null;
  }

  // Convert based on format
  let content: string;
  let extension: string;

  switch (options.format) {
    case 'html':
      content = toHTML(session, options);
      extension = 'html';
      break;
    case 'json':
      content = toJSON(session, options);
      extension = 'json';
      break;
    case 'md':
    default:
      content = toMarkdown(session, options);
      extension = 'md';
      break;
  }

  // Write to file
  const filename = `${session.id}.${extension}`;
  const outputPath = path.join(options.outputDir, filename);

  fs.mkdirSync(options.outputDir, { recursive: true });
  fs.writeFileSync(outputPath, content, 'utf-8');

  return {
    id: session.id,
    filename,
    date: session.timestamp,
    messageCount: session.messages.length,
    preview: session.messages[0]?.content.substring(0, 100) || '',
    exported: true,
    exportPath: outputPath,
  };
}

/**
 * Export all sessions
 */
export async function exportAllSessions(
  options: ExportOptions = DEFAULT_EXPORT_OPTIONS
): Promise<DialogSummary[]> {
  const sessions = await findSessions();
  const results: DialogSummary[] = [];

  for (const session of sessions) {
    const result = await exportSession(session.id, options);
    if (result) {
      results.push(result);
    }
  }

  return results;
}
