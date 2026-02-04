# Refactor Command

Improve code quality while preserving functionality.

## Objectives

| Goal | Description |
|------|-------------|
| Readability | Clear naming, reduced complexity |
| Performance | Optimized operations, efficient algorithms |
| Type Safety | Strict TypeScript, proper typing |
| Architecture | Proper patterns, single responsibility |

## Process

### Step 1: Analyze Current Code

Identify improvement opportunities:
- Code duplication
- Complex conditionals
- Long functions
- Poor naming
- Missing types
- Performance bottlenecks
- Violation of design principles

### Step 2: Plan Refactoring

Break into small, testable steps:
1. [Step 1 - Description]
2. [Step 2 - Description]
3. [Step 3 - Description]

**Principles:**
- Change one thing at a time
- Maintain functionality after each step
- Run tests between steps

### Step 3: Execute Refactoring

Apply changes incrementally, validating each step.

### Step 4: Validate

- [ ] All tests pass
- [ ] Functionality unchanged
- [ ] No new linting errors
- [ ] Performance not degraded

## Refactoring Patterns

### Extract Function
```javascript
// Before
function processUser(user) {
  // validation logic
  if (!user.name || user.name.length < 2) {
    throw new Error('Invalid name');
  }
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email');
  }
  // processing logic
  return { ...user, processed: true };
}

// After
function validateUser(user) {
  if (!user.name || user.name.length < 2) {
    throw new Error('Invalid name');
  }
  if (!user.email || !user.email.includes('@')) {
    throw new Error('Invalid email');
  }
}

function processUser(user) {
  validateUser(user);
  return { ...user, processed: true };
}
```

### Extract Custom Hook
```javascript
// Before
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  // render...
}

// After
function useUser(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}

function UserProfile({ userId }) {
  const { user, loading, error } = useUser(userId);
  // render...
}
```

### Simplify Conditionals
```javascript
// Before
function getDiscount(user) {
  if (user.isPremium) {
    if (user.yearsActive > 5) {
      return 0.3;
    } else if (user.yearsActive > 2) {
      return 0.2;
    } else {
      return 0.1;
    }
  } else {
    if (user.yearsActive > 5) {
      return 0.15;
    } else {
      return 0.05;
    }
  }
}

// After
const DISCOUNTS = {
  premium: { senior: 0.3, regular: 0.2, new: 0.1 },
  standard: { senior: 0.15, regular: 0.05, new: 0.05 }
};

function getUserTier(yearsActive) {
  if (yearsActive > 5) return 'senior';
  if (yearsActive > 2) return 'regular';
  return 'new';
}

function getDiscount(user) {
  const plan = user.isPremium ? 'premium' : 'standard';
  const tier = getUserTier(user.yearsActive);
  return DISCOUNTS[plan][tier];
}
```

### Replace Magic Numbers
```javascript
// Before
if (password.length < 8) { /* ... */ }
setTimeout(retry, 3000);

// After
const MIN_PASSWORD_LENGTH = 8;
const RETRY_DELAY_MS = 3000;

if (password.length < MIN_PASSWORD_LENGTH) { /* ... */ }
setTimeout(retry, RETRY_DELAY_MS);
```

### Improve Types
```typescript
// Before
function processData(data: any): any {
  return data.map((item: any) => item.value);
}

// After
interface DataItem {
  id: string;
  value: number;
}

function processData(data: DataItem[]): number[] {
  return data.map(item => item.value);
}
```

## Design Principles

| Principle | Description |
|-----------|-------------|
| DRY | Don't Repeat Yourself |
| KISS | Keep It Simple |
| YAGNI | You Aren't Gonna Need It |
| SRP | Single Responsibility Principle |

## Anti-Patterns to Fix

- God objects/functions (do too much)
- Deep nesting (> 3 levels)
- Primitive obsession (use objects)
- Feature envy (method uses other class's data)
- Long parameter lists (use objects)

## Checklist

Before refactoring:
- [ ] Tests exist for code being refactored
- [ ] Understand current behavior

After refactoring:
- [ ] All tests pass
- [ ] No functionality changed
- [ ] Code is more readable
- [ ] Run `/codex-review`
