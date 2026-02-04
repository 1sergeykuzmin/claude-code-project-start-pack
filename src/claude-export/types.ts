/**
 * Type definitions for Claude Dialog Exporter
 */

/**
 * Tool call in a message
 */
export interface ToolCall {
  id: string;
  name: string;
  input: Record<string, unknown>;
  output?: string;
}

/**
 * Single message in a session
 */
export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
  tool_calls?: ToolCall[];
}

/**
 * Session metadata
 */
export interface SessionMetadata {
  project?: string;
  workingDirectory?: string;
  model?: string;
  startTime?: string;
  endTime?: string;
  messageCount?: number;
  toolCallCount?: number;
}

/**
 * Complete session data
 */
export interface Session {
  id: string;
  timestamp: string;
  messages: Message[];
  metadata: SessionMetadata;
}

/**
 * Export options
 */
export interface ExportOptions {
  /** Redact credentials and secrets */
  redact: boolean;
  /** Output format */
  format: 'md' | 'html' | 'json';
  /** Output directory */
  outputDir: string;
  /** Include tool call details */
  includeToolCalls: boolean;
  /** Include YAML frontmatter in markdown */
  includeFrontmatter: boolean;
}

/**
 * Default export options
 */
export const DEFAULT_EXPORT_OPTIONS: ExportOptions = {
  redact: true,
  format: 'md',
  outputDir: 'dialog',
  includeToolCalls: true,
  includeFrontmatter: true,
};

/**
 * Server options
 */
export interface ServerOptions {
  /** Server port */
  port: number;
  /** Server host */
  host: string;
  /** Dialog directory to serve */
  dialogDir: string;
  /** Open browser automatically */
  openBrowser: boolean;
}

/**
 * Default server options
 */
export const DEFAULT_SERVER_OPTIONS: ServerOptions = {
  port: 3333,
  host: 'localhost',
  dialogDir: 'dialog',
  openBrowser: true,
};

/**
 * Watcher options
 */
export interface WatcherOptions {
  /** Session directories to watch */
  sessionDirs: string[];
  /** Export options to use */
  exportOptions: ExportOptions;
  /** Debounce interval in ms */
  debounceMs: number;
}

/**
 * Default watcher options
 */
export const DEFAULT_WATCHER_OPTIONS: WatcherOptions = {
  sessionDirs: [],
  exportOptions: DEFAULT_EXPORT_OPTIONS,
  debounceMs: 500,
};

/**
 * Dialog summary for listing
 */
export interface DialogSummary {
  id: string;
  filename: string;
  date: string;
  messageCount: number;
  preview: string;
  exported: boolean;
  exportPath?: string;
}

/**
 * Credential patterns for redaction
 */
export const CREDENTIAL_PATTERNS: RegExp[] = [
  // API Keys
  /sk-[a-zA-Z0-9]{32,}/g,
  /sk_live_[a-zA-Z0-9]+/g,
  /sk_test_[a-zA-Z0-9]+/g,
  /pk_live_[a-zA-Z0-9]+/g,
  /pk_test_[a-zA-Z0-9]+/g,

  // GitHub tokens
  /ghp_[a-zA-Z0-9]{36}/g,
  /gho_[a-zA-Z0-9]{36}/g,
  /ghu_[a-zA-Z0-9]{36}/g,
  /ghs_[a-zA-Z0-9]{36}/g,

  // AWS
  /AKIA[0-9A-Z]{16}/g,

  // Generic patterns
  /password\s*[:=]\s*['"][^'"]+['"]/gi,
  /api_key\s*[:=]\s*['"][^'"]+['"]/gi,
  /apiKey\s*[:=]\s*['"][^'"]+['"]/gi,
  /secret\s*[:=]\s*['"][^'"]+['"]/gi,
  /token\s*[:=]\s*['"][^'"]+['"]/gi,

  // Bearer tokens
  /Bearer [a-zA-Z0-9._-]+/g,

  // Basic auth
  /Basic [a-zA-Z0-9+/=]+/g,

  // Private keys
  /-----BEGIN [A-Z]+ PRIVATE KEY-----/g,
];

/**
 * Redaction replacement text
 */
export const REDACTION_TEXT = '[REDACTED]';
