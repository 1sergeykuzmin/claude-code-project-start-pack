# Security Command

Conduct comprehensive security audits following OWASP guidelines.

## Audit Areas

### 1. Input Validation

**Check for:**
- [ ] Server-side validation (never trust client)
- [ ] Type validation (Zod, Yup, or similar)
- [ ] String length limits
- [ ] Format validation (email, URL, etc.)
- [ ] Sanitization of user input

**Example Fix:**
```typescript
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
});

// Validate before processing
const result = userSchema.safeParse(input);
if (!result.success) {
  throw new ValidationError(result.error);
}
```

### 2. Authentication & Authorization

**Check for:**
- [ ] Auth check on all protected routes
- [ ] Authorization checks (user can access resource)
- [ ] JWT verification with proper secret
- [ ] Session management (expiry, rotation)
- [ ] No hardcoded credentials

**Example Fix:**
```typescript
// Middleware to verify auth
export async function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const payload = verifyJWT(token, process.env.JWT_SECRET);
    req.user = payload;
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### 3. SQL Injection

**Check for:**
- [ ] Parameterized queries
- [ ] No string concatenation in queries
- [ ] ORM/Query builder usage
- [ ] Input sanitization

**Example Fix:**
```typescript
// BAD - SQL injection vulnerable
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD - Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// GOOD - ORM
const user = await prisma.user.findUnique({ where: { id: userId } });
```

### 4. XSS (Cross-Site Scripting)

**Check for:**
- [ ] No `dangerouslySetInnerHTML` with user data
- [ ] React auto-escaping utilized
- [ ] Safe markdown rendering
- [ ] No `eval()` or `Function()` with user input

**Example Fix:**
```typescript
// BAD
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// GOOD - Use sanitization library
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />

// BETTER - Avoid raw HTML
<div>{userContent}</div>
```

### 5. CSRF (Cross-Site Request Forgery)

**Check for:**
- [ ] CSRF tokens on state-changing operations
- [ ] SameSite cookie attribute
- [ ] Proper HTTP methods (POST for mutations)
- [ ] Origin/Referer header validation

**Example Fix:**
```typescript
// Next.js API route with CSRF protection
import { csrf } from '@/lib/csrf';

export default csrf(async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end();
  }
  // Handle request
});
```

### 6. Data Exposure

**Check for:**
- [ ] Secrets in `.env` files (not committed)
- [ ] `.gitignore` includes sensitive files
- [ ] Error messages don't leak implementation details
- [ ] Logs don't contain sensitive data
- [ ] API responses are minimal (no extra fields)

**Example Fix:**
```typescript
// BAD - Exposes internal error
catch (error) {
  res.status(500).json({ error: error.message, stack: error.stack });
}

// GOOD - Generic error
catch (error) {
  console.error('Internal error:', error); // Log for debugging
  res.status(500).json({ error: 'Internal server error' });
}
```

### 7. Rate Limiting

**Check for:**
- [ ] Rate limits on public endpoints
- [ ] Brute force protection on auth
- [ ] DoS mitigation

**Example Fix:**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);
```

### 8. HTTPS & Security Headers

**Check for:**
- [ ] HTTPS enforced
- [ ] HSTS header
- [ ] Content-Security-Policy
- [ ] X-Content-Type-Options
- [ ] X-Frame-Options

**Example Fix:**
```typescript
// next.config.js
module.exports = {
  async headers() {
    return [{
      source: '/(.*)',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-XSS-Protection', value: '1; mode=block' },
        { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' }
      ]
    }];
  }
};
```

### 9. Dependencies

**Check for:**
- [ ] No known vulnerabilities
- [ ] Packages up to date
- [ ] Trusted sources only

```bash
npm audit
npm audit fix
npx snyk test
```

### 10. Database Security (Supabase/etc.)

**Check for:**
- [ ] Row Level Security (RLS) enabled
- [ ] Proper RLS policies
- [ ] Data isolation between users
- [ ] Service role key not exposed to client

## Output Format

```markdown
## Security Audit Report

### Summary
- **Overall Risk**: [Critical/High/Medium/Low]
- **Issues Found**: [Count]
- **Critical Issues**: [Count]

### Findings

#### 1. [Vulnerability Name]
- **Severity**: [Critical/High/Medium/Low]
- **Location**: [file:line]
- **Description**: [What's wrong]
- **Recommendation**: [How to fix]
- **Code Example**:
```[language]
// Fixed code
```

### Top 5 Critical Issues
1. [Issue 1]
2. [Issue 2]
...

### Recommendations
1. [Action 1]
2. [Action 2]
...
```

## Quick Checklist

Before release:
- [ ] `npm audit` shows no critical vulnerabilities
- [ ] No secrets in codebase
- [ ] All endpoints have auth where needed
- [ ] Input validation on all user data
- [ ] Rate limiting in place
- [ ] Security headers configured
- [ ] HTTPS enforced
