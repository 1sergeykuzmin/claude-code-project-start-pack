#!/usr/bin/env npx ts-node
/**
 * Claude Dialog Exporter - CLI Entry Point
 *
 * Commands:
 *   export [session-id]  Export sessions to markdown/html/json
 *   ui                   Start web viewer at localhost:3333
 *   watch                Watch for new sessions and auto-export
 *   list                 List all available sessions
 */

import { Command } from 'commander';
import * as path from 'path';
import * as fs from 'fs';
import { exportSession, exportAllSessions, findSessions } from './exporter';
import { startServer } from './server';
import { startWatcher } from './watcher';
import {
  ExportOptions,
  ServerOptions,
  DEFAULT_EXPORT_OPTIONS,
  DEFAULT_SERVER_OPTIONS,
  DialogSummary,
} from './types';

const VERSION = '2.0.0';

const program = new Command();

program
  .name('claude-dialog')
  .description('Dialog export and viewer for Claude Code sessions')
  .version(VERSION);

// Export command
program
  .command('export [session-id]')
  .description('Export sessions to markdown/html/json')
  .option('-f, --format <format>', 'Output format (md, html, json)', 'md')
  .option('-o, --output <dir>', 'Output directory', 'dialog')
  .option('-r, --redact', 'Redact credentials and secrets', true)
  .option('--no-redact', 'Do not redact credentials')
  .option('--no-frontmatter', 'Exclude YAML frontmatter in markdown')
  .option('--no-tool-calls', 'Exclude tool call details')
  .option('-a, --all', 'Export all sessions')
  .action(async (sessionId: string | undefined, options) => {
    const exportOptions: ExportOptions = {
      redact: options.redact,
      format: options.format as 'md' | 'html' | 'json',
      outputDir: options.output,
      includeToolCalls: options.toolCalls !== false,
      includeFrontmatter: options.frontmatter !== false,
    };

    try {
      // Ensure output directory exists
      if (!fs.existsSync(exportOptions.outputDir)) {
        fs.mkdirSync(exportOptions.outputDir, { recursive: true });
      }

      if (options.all || !sessionId) {
        console.log('Exporting all sessions...');
        const results = await exportAllSessions(exportOptions);
        console.log(`Exported ${results.length} session(s) to ${exportOptions.outputDir}/`);
        results.forEach((r) => {
          console.log(`  - ${r.filename}`);
        });
      } else {
        console.log(`Exporting session: ${sessionId}`);
        const result = await exportSession(sessionId, exportOptions);
        if (result) {
          console.log(`Exported to: ${result.exportPath}`);
        } else {
          console.error(`Session not found: ${sessionId}`);
          process.exit(1);
        }
      }
    } catch (error) {
      console.error('Export failed:', error);
      process.exit(1);
    }
  });

// UI command
program
  .command('ui')
  .description('Start web viewer at localhost:3333')
  .option('-p, --port <port>', 'Server port', '3333')
  .option('-h, --host <host>', 'Server host', 'localhost')
  .option('-d, --dialog-dir <dir>', 'Dialog directory', 'dialog')
  .option('--no-open', 'Do not open browser automatically')
  .action(async (options) => {
    const serverOptions: ServerOptions = {
      port: parseInt(options.port, 10),
      host: options.host,
      dialogDir: options.dialogDir,
      openBrowser: options.open !== false,
    };

    try {
      await startServer(serverOptions);
    } catch (error) {
      console.error('Server failed to start:', error);
      process.exit(1);
    }
  });

// Watch command
program
  .command('watch')
  .description('Watch for new sessions and auto-export')
  .option('-o, --output <dir>', 'Output directory', 'dialog')
  .option('-f, --format <format>', 'Output format (md, html, json)', 'md')
  .option('-r, --redact', 'Redact credentials', true)
  .option('--no-redact', 'Do not redact credentials')
  .option('-i, --interval <ms>', 'Debounce interval in ms', '500')
  .action(async (options) => {
    const exportOptions: ExportOptions = {
      redact: options.redact,
      format: options.format as 'md' | 'html' | 'json',
      outputDir: options.output,
      includeToolCalls: true,
      includeFrontmatter: true,
    };

    try {
      console.log('Starting session watcher...');
      console.log(`  Output: ${exportOptions.outputDir}/`);
      console.log(`  Format: ${exportOptions.format}`);
      console.log(`  Redact: ${exportOptions.redact}`);
      console.log('');
      console.log('Watching for new sessions. Press Ctrl+C to stop.');
      console.log('');

      await startWatcher({
        sessionDirs: [],  // Will use defaults
        exportOptions,
        debounceMs: parseInt(options.interval, 10),
      });
    } catch (error) {
      console.error('Watcher failed:', error);
      process.exit(1);
    }
  });

// List command
program
  .command('list')
  .description('List all available sessions')
  .option('--json', 'Output as JSON')
  .option('-e, --exported', 'Show only exported sessions')
  .option('-n, --new', 'Show only new (unexported) sessions')
  .action(async (options) => {
    try {
      const sessions = await findSessions();
      const dialogDir = 'dialog';

      const summaries: DialogSummary[] = sessions.map((session) => {
        const exportPath = path.join(dialogDir, `${session.id}.md`);
        const exported = fs.existsSync(exportPath);

        return {
          id: session.id,
          filename: `${session.id}.md`,
          date: session.timestamp,
          messageCount: session.messages.length,
          preview: session.messages[0]?.content.substring(0, 100) || '',
          exported,
          exportPath: exported ? exportPath : undefined,
        };
      });

      // Apply filters
      let filtered = summaries;
      if (options.exported) {
        filtered = filtered.filter((s) => s.exported);
      }
      if (options.new) {
        filtered = filtered.filter((s) => !s.exported);
      }

      if (options.json) {
        console.log(JSON.stringify(filtered, null, 2));
      } else {
        if (filtered.length === 0) {
          console.log('No sessions found.');
          return;
        }

        console.log(`Found ${filtered.length} session(s):\n`);
        filtered.forEach((s) => {
          const status = s.exported ? '[exported]' : '[new]';
          console.log(`  ${s.id}`);
          console.log(`    Date: ${s.date}`);
          console.log(`    Messages: ${s.messageCount}`);
          console.log(`    Status: ${status}`);
          if (s.preview) {
            console.log(`    Preview: ${s.preview.substring(0, 60)}...`);
          }
          console.log('');
        });
      }
    } catch (error) {
      console.error('Failed to list sessions:', error);
      process.exit(1);
    }
  });

// Parse and execute
program.parse();
