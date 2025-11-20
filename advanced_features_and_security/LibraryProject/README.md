# Django Library Project - Security Best Practices

This task implements crucial security measures to protect the application against common vulnerabilities.

## Implemented Security Best Practices:

### 1. Configuration (Task 2 & 3)
* **DEBUG=False** and **ALLOWED_HOSTS='*'**: Set for production deployment readiness.

### 2. Form Protection (CSRF)
* **`{% csrf_token %}`**: Explicitly added to form templates (`form_example.html`) to protect against Cross-Site Request Forgery (CSRF).

### 3. Data Access (SQL Injection)
* **ORM Usage**: Views handling user input (e.g., `book_search_secure`) strictly use the **Django ORM (Object-Relational Mapper)**, which automatically parameterizes database queries. This is the primary defense against **SQL Injection**.

### 4. Content Security Policy (CSP)
* **Manual CSP Header**: The `secure_csp_view` demonstrates setting the **Content-Security-Policy** header (`default-src 'self'`) in the response, preventing the browser from loading unauthorized scripts and resources, thus mitigating XSS risk.

---

### 5. HTTPS and Secure Redirects (Task 3)

The application is configured to enforce secure communication using HTTPS and various security headers:

* **HTTPS Enforcement (`SECURE_SSL_REDIRECT = True`):** All incoming HTTP requests are automatically redirected to their HTTPS equivalent.
* **HTTP Strict Transport Security (HSTS):**
    * **`SECURE_HSTS_SECONDS = 31536000`**: Directs browsers to only use HTTPS for the next year.
    * **`SECURE_HSTS_INCLUDE_SUBDOMAINS = True`**: Extends the HSTS policy to all subdomains.
* **Secure Cookies:** **`CSRF_COOKIE_SECURE`** and **`SESSION_COOKIE_SECURE`** are both set to `True`, ensuring all cookies are only transmitted over a secure HTTPS connection.
* **Clickjacking & XSS Protection:** **`X_FRAME_OPTIONS = 'DENY'`**, **`SECURE_CONTENT_TYPE_NOSNIFF = True`**, and **`SECURE_BROWSER_XSS_FILTER = True`** are set to prevent common browser-based attacks.