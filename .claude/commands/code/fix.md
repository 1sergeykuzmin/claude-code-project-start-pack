# Fix Command

Systematically debug and fix issues in the codebase.

## Process

### Step 1: Gather Information

Understand the problem:
- **Expected behavior**: What should happen?
- **Actual behavior**: What is happening?
- **Error messages**: Exact text of any errors
- **Reproduction steps**: How to trigger the issue
- **Recent changes**: What changed before issue appeared?

```bash
# Check recent commits
git log --oneline -10

# Check for modified files
git status
git diff
```

### Step 2: Analyze Code

Examine relevant files:
- Locate the code responsible for the failing behavior
- Trace the execution flow
- Check related components and dependencies
- Review recent changes to affected files

```bash
# Find recent changes to a file
git log -p --follow -5 -- path/to/file

# Search for related code
grep -r "searchTerm" src/
```

### Step 3: Formulate Hypotheses

Rank probable causes by likelihood:

1. **Most Likely**: [Hypothesis with supporting evidence]
2. **Possible**: [Alternative explanation]
3. **Less Likely**: [Edge case or unusual scenario]

**Common Issue Categories:**
- Missing validation
- Null/undefined handling
- Async/await mistakes
- Type errors
- Race conditions
- Authorization issues
- Caching problems
- Environment differences

### Step 4: Test Hypotheses

Add temporary debugging:
```javascript
console.log('[DEBUG] variable:', variable);
console.log('[DEBUG] state:', JSON.stringify(state, null, 2));
```

Check:
- Database state
- API responses
- Environment variables
- Network requests

### Step 5: Implement Fix

Apply the fix with:
- Clear explanation of what was wrong
- Why this fix addresses the issue
- Any side effects to be aware of

**Fix Patterns:**
```javascript
// Add null check
if (!data) return null;

// Add error boundary
try {
  await operation();
} catch (error) {
  handleError(error);
}

// Add validation
if (!isValid(input)) {
  throw new ValidationError('Invalid input');
}
```

### Step 6: Verify Fix

- [ ] Issue no longer reproduces
- [ ] No new errors introduced
- [ ] Related functionality still works
- [ ] Tests pass (if applicable)

### Step 7: Prevent Recurrence

Consider:
- Adding a test case for this scenario
- Improving error messages
- Adding documentation
- Creating a code pattern to prevent similar issues

## Common Issues Reference

### Null/Undefined
```javascript
// Problem
const value = obj.property; // obj might be undefined

// Fix
const value = obj?.property ?? defaultValue;
```

### Async/Await
```javascript
// Problem
const data = fetchData(); // Missing await

// Fix
const data = await fetchData();
```

### Race Condition
```javascript
// Problem
useEffect(() => {
  fetchData().then(setData);
}, [id]);

// Fix
useEffect(() => {
  let cancelled = false;
  fetchData().then(data => {
    if (!cancelled) setData(data);
  });
  return () => { cancelled = true; };
}, [id]);
```

### Type Error
```typescript
// Problem
const length = arr.length; // arr might not be array

// Fix
const length = Array.isArray(arr) ? arr.length : 0;
```

## Output Format

After fixing, provide:
1. **Root Cause**: What was actually wrong
2. **Fix Applied**: What was changed
3. **Verification**: How the fix was tested
4. **Prevention**: How to avoid this in future

## Next Steps

After fixing:
1. Run `/codex-review` to validate fix
2. Run `/commit` to commit the fix
3. Update any related documentation
