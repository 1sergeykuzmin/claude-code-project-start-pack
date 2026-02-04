# Dialog Exporter Decision

## Status
Accepted

## Date
2026-02-04

## Context

Our framework had `/ui` and `/watch` commands that provided instructions for Claude to execute dialog viewing and watching. The claude-code-starter framework has actual TypeScript code that runs standalone without Claude.

We needed to decide how to implement dialog export functionality.

## Decision

**Selected: Option A - Full Implementation**

Implement actual TypeScript code that works standalone without Claude.

## Options Considered

### Option A: Full Implementation
Create complete TypeScript source code in `src/claude-export/` with CLI, exporter, web server, and watcher.

**Pros:**
- Works standalone without active Claude session
- Users can export/view dialogs anytime
- Web UI accessible via browser
- Professional tooling experience
- Can be published as npm package

**Cons:**
- Requires Node.js dependency
- More code to maintain
- Must handle edge cases in code
- Build/compile step required

### Option B: Instruction-Based
Keep current approach - commands are instructions Claude executes.

**Pros:**
- Simpler, no runtime dependencies
- Flexible - Claude adapts to situations
- No build step

**Cons:**
- Only works during Claude session
- Can't view dialogs without Claude
- Inconsistent experience
- No web UI

### Option C: Hybrid
Instructions that call TypeScript if available, fall back to Claude.

**Pros:**
- Best of both worlds
- Graceful degradation

**Cons:**
- Two implementations to maintain
- Inconsistent behavior
- Complex documentation

## Rationale

We chose Full Implementation because:

1. **Standalone Value**: Users often want to view past dialogs when Claude isn't running. A web UI at localhost:3333 provides this.

2. **Professional Tooling**: npm scripts (`dialog:export`, `dialog:ui`, `dialog:watch`) integrate with existing development workflows.

3. **Consistent Experience**: TypeScript code always behaves the same way, unlike Claude-based approaches that may vary.

4. **Node.js is Common**: Most web developers already have Node.js installed for their projects.

5. **Separation of Concerns**: Dialog export is infrastructure, not AI-assisted development. It makes sense as standalone tooling.

## Consequences

### Positive
- Web viewer at localhost:3333
- `npm run dialog:export` works anytime
- File watcher for auto-export
- Session listing and search
- Credential redaction built-in

### Negative
- Node.js 18+ required (for dialog features)
- Must compile TypeScript
- Additional npm dependencies (express, chokidar, marked)

### Mitigation
- Node.js dependency is optional (framework works without it)
- Pre-compiled JavaScript can be distributed
- Clear installation instructions

## Technical Details

### Directory Structure
```
src/claude-export/
├── cli.ts (entry point)
├── exporter.ts (session → markdown)
├── server.ts (web UI)
├── watcher.ts (file system monitoring)
├── gitignore.ts (auto-update .gitignore)
├── types.ts (TypeScript interfaces)
├── package.json
└── tsconfig.json
```

### npm Scripts
```json
{
  "scripts": {
    "dialog:export": "ts-node cli.ts export",
    "dialog:ui": "ts-node cli.ts ui",
    "dialog:watch": "ts-node cli.ts watch",
    "dialog:list": "ts-node cli.ts list"
  }
}
```

### Dependencies
- `express` ^4.18.0 (web server)
- `chokidar` ^3.5.0 (file watching)
- `marked` ^9.0.0 (markdown rendering)
- `typescript` ^5.0.0 (dev)

### Features
- Export sessions to markdown/HTML/JSON
- Web viewer with search
- Automatic credential redaction
- Real-time file watching
- Session inventory listing

## Related Decisions

- `execution-mode-decision.md` - Overall execution approach
- `preset-system-design.md` - How dialog settings interact with presets
