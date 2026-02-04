# Dialog Export Directory

This directory stores exported development conversations for reference.

## Purpose

- Preserve development context between sessions
- Enable knowledge sharing with team members
- Debug issues by reviewing conversation history
- Document decision-making processes

## Privacy

All dialog exports are **automatically ignored by git** to protect:
- Sensitive discussion content
- API keys or credentials that may appear in conversation
- Personal information

## File Naming

Exports follow the pattern:
```
YYYY-MM-DD-[session-id].md
```

Example: `2026-02-04-abc123.md`

## Manual Export

To manually export a conversation, the Completion Protocol will:
1. Save conversation to this directory
2. Redact any detected credentials
3. Format as readable Markdown

## Sharing

If you need to share a dialog:
1. Review for sensitive content first
2. Redact any credentials manually
3. Share via secure channel (not git)
