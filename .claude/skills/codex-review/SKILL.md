---
name: codex-review
description: Run Codex CLI to review uncommitted changes. Use when you want a second opinion on uncommitted code changes.
---

# Codex Review

## Overview

Run OpenAI's Codex CLI in non-interactive mode to get a code review of uncommitted changes.

## Prerequisites

Before running, verify:
- `codex` CLI is installed and available

```bash
which codex
```

## Usage

### Review uncommitted changes (staged, unstaged, and untracked)

```bash
codex review --uncommitted
```

### Review changes against a base branch

```bash
codex review --base main
```

### Review a specific commit

```bash
codex review --commit <SHA>
```

### With custom review instructions

```bash
codex review --uncommitted "Focus on security vulnerabilities and error handling"
```

## Success Criteria

- Codex review output is displayed
- Exit code 0 indicates success
