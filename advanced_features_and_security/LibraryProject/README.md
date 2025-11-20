# Django Library Project - Security Best Practices

This task implements crucial security measures to protect the application against common vulnerabilities.

## Implemented Security Best Practices:

### 1. Configuration (`settings.py`)
* **DEBUG=False** and **ALLOWED_HOSTS='*'**: Set for production deployment readiness.
* **CSRF/Session Security**: `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True` enforce cookie transmission only over HTTPS.
* **Browser Protections**: Configured `SECURE_BROWSER_XSS_FILTER = True`, `SECURE_CONTENT_TYPE_NOSNIFF = True`, and `X_FRAME_OPTIONS = 'DENY'` to mitigate XSS and Clickjacking attacks.

### 2. Form Protection (CSRF)
* **`{% csrf_token %}`**: Explicitly added to form templates (`form_example.html`) to protect against Cross-Site Request Forgery (CSRF).

### 3. Data Access (SQL Injection)
* **ORM Usage**: Views handling user input (e.g., `book_search_secure`) strictly use the **Django ORM (Object-Relational Mapper)**, which automatically parameterizes database queries. This is the primary defense against **SQL Injection**.

### 4. Content Security Policy (CSP)
* **Manual CSP Header**: The `secure_csp_view` demonstrates setting the **Content-Security-Policy** header (`default-src 'self'`) in the response, preventing the browser from loading unauthorized scripts and resources, thus mitigating XSS risk.