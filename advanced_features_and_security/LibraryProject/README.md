# Django Library Project - Security Best Practices

This project implements crucial security measures and advanced features as required by the module.

### 0. Custom User Model (Task 0)
* The default Django user model has been replaced with a **`CustomUser`** model located in the `users` application.
* Custom fields **`date_of_birth`** and **`profile_photo`** have been added to the user model.
* A custom manager (`CustomUserManager`) handles the creation of users and superusers.
* **`AUTH_USER_MODEL = 'users.CustomUser'`** is set in `settings.py`.

### 1. Permissions and Groups (Task 1)
* **Custom Permissions:** The `Book` model includes custom permissions: **`can_view`**, **`can_create`**, **`can_edit`**, and **`can_delete`**.
* **Enforcement in Views:** Views are protected using the **`@permission_required`** decorator to ensure only authorized users (e.g., those in the Editors group) can perform specific actions like creating or editing books.

### 2. Security Best Practices (Task 2)
* **SQL Injection:** Prevented by using the Django ORM (Object-Relational Mapper) for all database queries.
* **CSRF:** Forms are protected using **`{% csrf_token %}`**.
* **XSS/CSP:** A basic **`Content-Security-Policy`** is enforced in one view for demonstration.

### 3. HTTPS and Secure Redirects (Task 3)
* **HTTPS Enforcement:** **`SECURE_SSL_REDIRECT = True`** forces all HTTP requests to HTTPS.
* **HSTS:** **`SECURE_HSTS_SECONDS`** is set to enforce HTTPS usage by the browser.
* **Secure Cookies:** **`CSRF_COOKIE_SECURE`** and **`SESSION_COOKIE_SECURE`** are set to `True`.
* **Deployment Fix:** **`SECURE_PROXY_SSL_HEADER`** is configured to correctly identify HTTPS traffic behind a proxy/load balancer.