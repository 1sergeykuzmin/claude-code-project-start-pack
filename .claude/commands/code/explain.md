# Explain Command

Provide clear explanations of code with complexity-aware detail levels.

## Complexity Assessment

| Complexity | Lines | Explanation Depth |
|------------|-------|-------------------|
| Simple | 1-10 | Brief (2-3 sentences) |
| Medium | 10-50 | Overview + step-by-step |
| Complex | 50+ | Full analysis |

## Simple Code (1-10 lines)

Provide:
- What it does (1-2 sentences)
- Key point or gotcha (if any)

**Example:**
```javascript
const doubled = arr.map(x => x * 2);
```
> Creates a new array with each element multiplied by 2. Uses `map` which doesn't mutate the original array.

## Medium Code (10-50 lines)

Provide:
1. **Overview**: What the code accomplishes
2. **Step-by-step**: Key operations in sequence
3. **Edge cases**: Important conditions or error handling

**Example:**
```javascript
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return { success: false, error: error.message };
  }
}
```

> **Overview**: Fetches user data from an API with error handling.
>
> **Flow**:
> 1. Makes GET request to `/api/users/{userId}`
> 2. Checks if response is successful (status 200-299)
> 3. Parses JSON response
> 4. Returns success object with data
>
> **Error handling**: Catches network errors and non-OK responses, returning failure object instead of throwing.

## Complex Code (50+ lines)

Provide:
1. **Purpose**: High-level goal
2. **Architecture**: How components interact
3. **Data flow**: Input → transformations → output
4. **Key algorithms**: Important logic explained
5. **Dependencies**: External code relied upon
6. **Edge cases**: Error handling, boundary conditions
7. **Potential improvements**: (only if requested)

## Explanation Principles

### Focus on What and Why
```javascript
// Don't explain: "Sets isLoading to true"
// Do explain: "Shows loading state while data is being fetched"
```

### Highlight Non-Obvious Behavior
```javascript
// Mention this gotcha:
const arr = [1, 2, 3];
arr.length = 0; // Clears array in-place, affects all references
```

### Explain Business Logic
```javascript
// Don't just say "multiplies by 0.1"
// Say "applies 10% discount for premium members"
const discount = isPremium ? price * 0.1 : 0;
```

### Clarify Complex Patterns
```javascript
// Explain the pattern:
const memoized = useMemo(() => expensiveCalculation(data), [data]);
// "Caches result of expensiveCalculation, only recalculating when data changes"
```

## Adaptive Response

- Skip obvious explanations
- Focus on the parts that matter
- Match explanation depth to code complexity
- Include only relevant sections

## Output Format

### For Simple Code
> [Brief explanation in 2-3 sentences]

### For Medium/Complex Code
```
## Overview
[What the code does]

## How It Works
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Key Points
- [Important detail 1]
- [Important detail 2]

## Edge Cases
- [Error handling or boundary conditions]
```
