# UI Command (Dialog Viewer)

Launch a web interface for browsing exported development dialogs.

## Usage

```
/ui
```

## Purpose

Provides a browser-based interface to:
- Browse all exported dialogs
- Search conversation history
- Review past development decisions
- Share context with team members

## How It Works

### Step 1: Check Prerequisites

```
Verify:
- Node.js installed
- dialog/ directory exists
- Exported dialogs present
```

### Step 2: Start Server

```bash
# The command launches a local web server
# Default port: 3333
# Access at: http://localhost:3333
```

### Step 3: Browse Interface

The UI provides:

```
┌─────────────────────────────────────────────────────────────────┐
│ Dialog Viewer                                    [Search... 🔍] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Recent Sessions                                                  │
│ ├── 2024-01-15 - Feature: User Authentication (2h 15m)         │
│ ├── 2024-01-14 - Bug Fix: Login redirect issue (45m)           │
│ ├── 2024-01-13 - Setup: Initial project structure (1h 30m)     │
│ └── 2024-01-12 - Planning: Architecture decisions (3h)         │
│                                                                  │
│ [View] [Export] [Delete]                                        │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│ Statistics                                                       │
│ Total sessions: 15 | Total time: ~24h | Files changed: 156     │
└─────────────────────────────────────────────────────────────────┘
```

### Step 4: View Dialog

Clicking a session shows:

```
┌─────────────────────────────────────────────────────────────────┐
│ Session: 2024-01-15 - Feature: User Authentication              │
├─────────────────────────────────────────────────────────────────┤
│ Duration: 2h 15m | Tasks: 3 | Commits: 2                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ User: Let's implement user authentication                       │
│                                                                  │
│ Claude: I'll help you implement authentication. First, let me   │
│ review the TRD for the auth requirements...                     │
│                                                                  │
│ [Tool: Read dev-docs/trd.md]                                    │
│                                                                  │
│ Based on the spec, we need:                                     │
│ 1. JWT-based authentication                                     │
│ 2. Refresh token rotation                                       │
│ ...                                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Features

### Search
- Full-text search across all dialogs
- Filter by date range
- Filter by topic/tags

### Export
- Export single dialog as Markdown
- Export multiple dialogs as ZIP
- Redact credentials before export

### Statistics
- Session duration tracking
- Tasks completed per session
- Files changed over time

## Privacy

- All data stays local (no external transmission)
- Dialogs are gitignored by default
- Credential redaction available
- Delete functionality for sensitive sessions

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the viewer.

## Requirements

- Node.js 18+
- Exported dialogs in `dialog/` directory

## When No Dialogs Exist

```
No dialogs found in dialog/ directory.

Dialogs are created when:
1. Completion Protocol exports the session (/fi)
2. Manual export via /watch command

To enable auto-export, ensure settings.json has:
{
  "protocols": {
    "completion": {
      "exportDialog": true
    }
  }
}
```

## Configuration

In `.claude/settings.json`:
```json
{
  "dialog": {
    "exportPath": "dialog/",
    "viewerPort": 3333,
    "redactCredentials": true
  }
}
```

## Alternative: Manual Browsing

If you prefer not to use the web UI:
```bash
# List all dialogs
ls -la dialog/

# Read specific dialog
cat dialog/2024-01-15-session.md

# Search across dialogs
grep -r "authentication" dialog/
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/ui` | Browse dialogs (this command) |
| `/watch` | Auto-export dialogs in real-time |
| `/fi` | End session and export dialog |
