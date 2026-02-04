# Test Command

Write comprehensive tests following best practices.

## Test Types

| Type | Purpose | Scope |
|------|---------|-------|
| Unit | Test individual functions/components | Single unit |
| Integration | Test component interactions | Multiple units |
| E2E | Test full user flows | Entire system |

## Process

### Step 1: Identify What to Test

- Happy path (normal usage)
- Edge cases (boundary values)
- Error scenarios (invalid input)
- Different input combinations

### Step 2: Set Up Test Environment

```typescript
// Mock external dependencies
jest.mock('@/lib/api');
jest.mock('@/lib/database');

// Set up test data
const mockUser = {
  id: '1',
  name: 'Test User',
  email: 'test@example.com'
};
```

### Step 3: Write Tests

Use Arrange-Act-Assert pattern:

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toMatchObject({
        id: expect.any(String),
        name: 'John',
        email: 'john@example.com'
      });
    });

    it('should throw error with invalid email', async () => {
      // Arrange
      const userData = { name: 'John', email: 'invalid' };

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow('Invalid email');
    });
  });
});
```

### Step 4: Ensure Coverage

Test coverage should include:
- All public functions
- All code branches
- Error handling paths
- Edge cases

## Test Patterns

### Unit Test (Function)
```typescript
describe('calculateDiscount', () => {
  it('returns 0 for non-premium users', () => {
    expect(calculateDiscount({ isPremium: false })).toBe(0);
  });

  it('returns 10% for premium users', () => {
    expect(calculateDiscount({ isPremium: true })).toBe(0.1);
  });

  it('returns 20% for premium users with 5+ years', () => {
    expect(calculateDiscount({ isPremium: true, yearsActive: 5 })).toBe(0.2);
  });
});
```

### Component Test (React)
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('renders email and password inputs', () => {
    render(<LoginForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it('calls onSubmit with form data', async () => {
    const mockSubmit = jest.fn();
    render(<LoginForm onSubmit={mockSubmit} />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(mockSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });

  it('shows validation error for invalid email', async () => {
    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'invalid' }
    });
    fireEvent.blur(screen.getByLabelText(/email/i));

    expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
  });
});
```

### API Test
```typescript
import { createMocks } from 'node-mocks-http';
import handler from '@/pages/api/users';

describe('/api/users', () => {
  it('returns users list for GET', async () => {
    const { req, res } = createMocks({ method: 'GET' });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    expect(JSON.parse(res._getData())).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ id: expect.any(String) })
      ])
    );
  });

  it('creates user for POST with valid data', async () => {
    const { req, res } = createMocks({
      method: 'POST',
      body: { name: 'John', email: 'john@example.com' }
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(201);
  });

  it('returns 400 for POST with invalid data', async () => {
    const { req, res } = createMocks({
      method: 'POST',
      body: { name: '' }
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(400);
  });
});
```

### Hook Test
```typescript
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('starts with initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## Test Naming Convention

```typescript
describe('[Unit/Component Name]', () => {
  describe('[method/feature]', () => {
    it('should [expected behavior] when [condition]', () => {
      // ...
    });
  });
});
```

## Best Practices

- **Test behavior, not implementation**
- **One assertion per test** (when practical)
- **Use descriptive test names**
- **Isolate tests** - no shared state
- **Mock external dependencies**
- **Test both success and failure cases**

## Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific file
npm test -- UserService.test.ts

# Run in watch mode
npm test -- --watch
```

## Coverage Targets

| Metric | Target |
|--------|--------|
| Statements | > 80% |
| Branches | > 75% |
| Functions | > 80% |
| Lines | > 80% |
