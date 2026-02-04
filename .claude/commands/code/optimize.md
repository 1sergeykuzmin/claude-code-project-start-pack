# Optimize Command

Improve code performance across multiple dimensions.

## Optimization Areas

### 1. React Performance

**Prevent Unnecessary Re-renders:**
```javascript
// Use React.memo for pure components
const Item = React.memo(({ data }) => <div>{data.name}</div>);

// Use useMemo for expensive calculations
const sorted = useMemo(() => items.sort(compareFn), [items]);

// Use useCallback for stable function references
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

**Avoid Inline Objects/Functions:**
```javascript
// Bad - creates new object every render
<Component style={{ color: 'red' }} />

// Good - stable reference
const style = useMemo(() => ({ color: 'red' }), []);
<Component style={style} />
```

**Proper Key Usage:**
```javascript
// Bad - index as key
{items.map((item, i) => <Item key={i} />)}

// Good - stable unique identifier
{items.map(item => <Item key={item.id} />)}
```

### 2. Database Queries

**Select Only Required Fields:**
```javascript
// Bad
const users = await db.user.findMany();

// Good
const users = await db.user.findMany({
  select: { id: true, name: true, email: true }
});
```

**Use Pagination:**
```javascript
const users = await db.user.findMany({
  skip: page * pageSize,
  take: pageSize
});
```

**Add Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

**Fix N+1 Queries:**
```javascript
// Bad - N+1 queries
const posts = await db.post.findMany();
for (const post of posts) {
  post.author = await db.user.findUnique({ where: { id: post.authorId }});
}

// Good - single query with include
const posts = await db.post.findMany({
  include: { author: true }
});
```

### 3. Bundle Size

**Dynamic Imports:**
```javascript
// Lazy load heavy components
const Chart = lazy(() => import('./Chart'));
const Editor = lazy(() => import('./Editor'));
```

**Analyze Bundle:**
```bash
npm run build -- --analyze
# or
npx webpack-bundle-analyzer
```

**Remove Unused Dependencies:**
```bash
npx depcheck
```

### 4. Caching

**React Cache:**
```javascript
import { cache } from 'react';

const getUser = cache(async (id) => {
  return await fetchUser(id);
});
```

**SWR/React Query:**
```javascript
const { data } = useSWR(`/api/user/${id}`, fetcher, {
  revalidateOnFocus: false,
  dedupingInterval: 60000
});
```

### 5. Network

**Batch Requests:**
```javascript
// Bad - multiple requests
const user = await fetch('/api/user');
const posts = await fetch('/api/posts');

// Good - parallel requests
const [user, posts] = await Promise.all([
  fetch('/api/user'),
  fetch('/api/posts')
]);
```

**Prefetch Data:**
```javascript
// Next.js prefetching
<Link href="/dashboard" prefetch>Dashboard</Link>
```

### 6. Images & Media

**Use Optimized Components:**
```javascript
// Next.js Image
import Image from 'next/image';
<Image src="/photo.jpg" width={800} height={600} />
```

**Lazy Load:**
```javascript
<img loading="lazy" src="..." />
```

**Use Modern Formats:**
```html
<picture>
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="...">
</picture>
```

## Optimization Workflow

### Step 1: Measure
```bash
# Performance profiling
npm run build
lighthouse https://your-site.com

# React DevTools Profiler
# - Record interaction
# - Identify slow components
```

### Step 2: Identify Bottlenecks

Key metrics:
| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.8s |
| Largest Contentful Paint | < 2.5s |
| Time to Interactive | < 3.8s |
| Cumulative Layout Shift | < 0.1 |
| Total Blocking Time | < 200ms |

### Step 3: Implement Changes

Prioritize by impact:
1. Critical path optimizations
2. Largest components
3. Most frequent operations

### Step 4: Verify Results

```bash
# Compare before/after
lighthouse https://your-site.com --output=json > after.json

# Run performance tests
npm run test:perf
```

## Output Format

When optimizing, provide:

```markdown
## Performance Issues Found

1. **Issue**: [Description]
   - **Impact**: [High/Medium/Low]
   - **Fix**: [Solution]
   - **Estimated Improvement**: [Metric improvement]

## Recommended Changes

### Priority 1: [Most impactful]
[Code changes]

### Priority 2: [Secondary]
[Code changes]

## Verification

[How to measure improvement]
```

## Checklist

- [ ] Measured baseline performance
- [ ] Identified specific bottlenecks
- [ ] Applied targeted optimizations
- [ ] Verified improvements
- [ ] No functionality broken
- [ ] Run `/codex-review`
