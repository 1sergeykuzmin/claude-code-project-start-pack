# Execution Mode Decision

## Status
Accepted

## Date
2026-02-04

## Context

The claude-code-starter framework introduced "silent mode" protocols that produce zero output on success, showing output only when user input is required or errors occur. Our framework (claude-code-project-start-pack) historically used verbose output showing all progress steps.

We needed to decide how to integrate these approaches.

## Decision

**Selected: Option A - Dual Mode**

Offer both verbose AND silent protocols. Users choose via a preset system.

## Options Considered

### Option A: Dual Mode
Maintain both verbose and silent protocol variants. Users select behavior via presets.

**Pros:**
- User choice - different workflows for different needs
- Backward compatibility - existing users keep current behavior
- Gradual adoption - users can try silent mode without commitment
- Flexibility - can mix and match behaviors

**Cons:**
- More code to maintain (6 protocol files instead of 3)
- Complexity in protocol routing
- Potential confusion about which mode is active

### Option B: Silent Default
Make silent mode the default, verbose optional.

**Pros:**
- Matches claude-code-starter philosophy
- Cleaner user experience for experienced users
- Less visual noise

**Cons:**
- Breaking change for existing users
- Less visibility for debugging
- Harder for new users to understand what's happening

### Option C: Configurable Verbosity
Single protocol with verbosity setting (0-3 levels).

**Pros:**
- Simpler code structure
- Fine-grained control

**Cons:**
- More complex protocol logic
- Harder to optimize for each mode
- Muddled user experience

## Rationale

We chose Dual Mode because:

1. **Backward Compatibility**: Existing users expect verbose output. Changing this would be disruptive.

2. **User Autonomy**: Different projects have different needs. A personal prototype benefits from silent mode; a team project may need verbose mode for debugging.

3. **Preset System**: The preset system naturally supports this by mapping presets to protocol variants:
   - `verbose`, `paranoid` → verbose protocols
   - `balanced` → optimized protocols
   - `autopilot`, `silent` → silent protocols

4. **Clear Separation**: Separate protocol files are easier to maintain than conditional logic within a single file.

## Consequences

### Positive
- Users can choose their preferred experience
- Framework appeals to both transparency-focused and flow-focused users
- Clear upgrade path from v1.x (verbose is default)

### Negative
- Must maintain 6 protocol files instead of 3
- Protocol router adds complexity
- Documentation must cover both modes

### Neutral
- `/codex-review` remains mandatory in all modes (framework invariant)

## Implementation

Protocol files:
- `cold-start.md` (verbose)
- `cold-start-optimized.md` (balanced)
- `cold-start-silent.md` (silent)
- `completion.md` (verbose)
- `completion-optimized.md` (balanced)
- `completion-silent.md` (silent)

Router logic in `router.md` selects appropriate protocol based on active preset.

## Related Decisions

- `preset-system-design.md` - How presets control behavior
- `silent-mode-philosophy.md` - Philosophy behind silent mode
