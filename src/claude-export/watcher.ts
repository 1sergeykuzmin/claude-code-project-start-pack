/**
 * Session watcher - monitors for new Claude sessions and auto-exports
 */

import * as chokidar from 'chokidar';
import * as path from 'path';
import * as os from 'os';
import * as fs from 'fs';
import {
  WatcherOptions,
  ExportOptions,
  DEFAULT_WATCHER_OPTIONS,
  DEFAULT_EXPORT_OPTIONS,
} from './types';
import { exportSession, findSessions } from './exporter';

/**
 * Default session directories to watch
 */
const DEFAULT_SESSION_DIRS = [
  path.join(os.homedir(), '.claude', 'projects'),
  path.join(process.cwd(), '.claude', 'sessions'),
];

/**
 * Track exported sessions to avoid duplicates
 */
const exportedSessions = new Set<string>();

/**
 * Debounce timer
 */
let debounceTimer: NodeJS.Timeout | null = null;

/**
 * Pending files to process
 */
const pendingFiles = new Set<string>();

/**
 * Start watching for new sessions
 */
export async function startWatcher(
  options: WatcherOptions = DEFAULT_WATCHER_OPTIONS
): Promise<void> {
  const sessionDirs =
    options.sessionDirs.length > 0
      ? options.sessionDirs
      : DEFAULT_SESSION_DIRS.filter((dir) => fs.existsSync(dir));

  if (sessionDirs.length === 0) {
    console.log('No session directories found to watch.');
    console.log('Expected directories:');
    DEFAULT_SESSION_DIRS.forEach((dir) => console.log(`  - ${dir}`));
    return;
  }

  // Load already exported sessions
  await loadExportedSessions(options.exportOptions.outputDir);

  console.log('Watching directories:');
  sessionDirs.forEach((dir) => console.log(`  - ${dir}`));
  console.log('');

  // Create watcher
  const watcher = chokidar.watch(sessionDirs, {
    ignored: /(^|[\/\\])\../, // Ignore dotfiles
    persistent: true,
    ignoreInitial: false,
    depth: 10,
    awaitWriteFinish: {
      stabilityThreshold: 1000,
      pollInterval: 100,
    },
  });

  // Handle file events
  watcher.on('add', (filePath: string) => {
    if (isSessionFile(filePath)) {
      queueFile(filePath, options);
    }
  });

  watcher.on('change', (filePath: string) => {
    if (isSessionFile(filePath)) {
      queueFile(filePath, options);
    }
  });

  watcher.on('error', (error: Error) => {
    console.error('Watcher error:', error);
  });

  // Keep process running
  return new Promise(() => {
    // This promise never resolves - keeps the watcher running
    process.on('SIGINT', () => {
      console.log('\nStopping watcher...');
      watcher.close();
      process.exit(0);
    });
  });
}

/**
 * Check if a file is a session file
 */
function isSessionFile(filePath: string): boolean {
  return filePath.endsWith('.jsonl');
}

/**
 * Queue a file for processing with debouncing
 */
function queueFile(filePath: string, options: WatcherOptions): void {
  pendingFiles.add(filePath);

  // Clear existing timer
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }

  // Set new timer
  debounceTimer = setTimeout(() => {
    processPendingFiles(options);
  }, options.debounceMs);
}

/**
 * Process all pending files
 */
async function processPendingFiles(options: WatcherOptions): Promise<void> {
  const files = Array.from(pendingFiles);
  pendingFiles.clear();

  for (const filePath of files) {
    await processFile(filePath, options);
  }
}

/**
 * Process a single session file
 */
async function processFile(
  filePath: string,
  options: WatcherOptions
): Promise<void> {
  const sessionId = path.basename(filePath, '.jsonl');

  // Skip if already exported
  if (exportedSessions.has(sessionId)) {
    return;
  }

  try {
    console.log(`New session detected: ${sessionId}`);

    const result = await exportSession(sessionId, options.exportOptions);

    if (result) {
      exportedSessions.add(sessionId);
      console.log(`  Exported to: ${result.exportPath}`);
    } else {
      console.log(`  Could not export (may be empty or invalid)`);
    }
  } catch (error) {
    console.error(`  Export failed: ${error}`);
  }
}

/**
 * Load already exported sessions from output directory
 */
async function loadExportedSessions(outputDir: string): Promise<void> {
  if (!fs.existsSync(outputDir)) {
    return;
  }

  const files = fs.readdirSync(outputDir);
  const extensions = ['.md', '.html', '.json'];

  for (const file of files) {
    for (const ext of extensions) {
      if (file.endsWith(ext)) {
        const sessionId = path.basename(file, ext);
        exportedSessions.add(sessionId);
        break;
      }
    }
  }

  if (exportedSessions.size > 0) {
    console.log(`Found ${exportedSessions.size} already exported session(s)`);
  }
}

/**
 * Export all new sessions (one-time scan)
 */
export async function exportNewSessions(
  options: ExportOptions = DEFAULT_EXPORT_OPTIONS
): Promise<number> {
  // Load existing exports
  await loadExportedSessions(options.outputDir);

  // Find all sessions
  const sessions = await findSessions();

  let exported = 0;

  for (const session of sessions) {
    if (!exportedSessions.has(session.id)) {
      try {
        const result = await exportSession(session.id, options);
        if (result) {
          exported++;
          console.log(`Exported: ${session.id}`);
        }
      } catch (error) {
        console.error(`Failed to export ${session.id}:`, error);
      }
    }
  }

  return exported;
}
