## 1. What is SQL Injection (SQLi)?

* **Definition:** SQL injection is a vulnerability where an attacker interferes with the SQL queries an application makes to its backend database.
* **Mechanism:** It occurs when user-supplied data is not validated or sanitized and is directly concatenated into a SQL query. This allows an attacker to inject SQL characters (like single quotes `'` or comments `--`) to alter the query's logic.

> **Example:**  An attacker enters `admin' --` into a username field. The resulting query becomes `SELECT * FROM users WHERE username = 'admin' --' AND password = '...'`. The database ignores the password check due to the comment, logging the attacker in as admin.

* **Impact (CIA Triad):**
    * **Confidentiality:** Attackers can view sensitive data (e.g., passwords, emails).
    * **Integrity:** Attackers can modify or delete data (e.g., changing a user's email to reset their password).
    * **Availability:** Attackers can delete data or deny access to accounts.
    * **RCE:** In severe cases, it can lead to Remote Code Execution (RCE) on the underlying server.
* **Prevalence:** It is consistently ranked as a critical risk (e.g., #1 in OWASP Top 10 for Injection).

---

## 2. Types of SQL Injection
The video classifies SQLi into three major categories:

### A. In-band (Classic) SQL Injection
The attacker uses the same communication channel to launch the attack and gather results. Results are visible directly in the application.
* **Error-based SQLi:** Forcing the database to generate an error that reveals information about the database structure, version, or even the full query.
* **Union-based SQLi:** Leveraging the `UNION` operator to combine the results of the original query with the results of an injected query, effectively dumping data from other tables.

### B. Inferential (Blind) SQL Injection
No data is transferred via the web application; the attacker cannot see the result of the query. They must reconstruct data by asking the database true/false questions.
* **Boolean-based SQLi:** The application returns a different result (e.g., a page loads vs. doesn't load) depending on whether the injected SQL query evaluates to `TRUE` or `FALSE`.
* **Time-based SQLi:** The attacker injects a payload that causes the database to pause (sleep) for a specific time if a condition is true. The "response time" indicates the truth of the statement.

### C. Out-of-band SQL Injection
Used when the attacker cannot use the same channel to retrieve results. It relies on triggering a network connection (e.g., DNS or HTTP request) from the database server to a machine controlled by the attacker.

---

## 3. Finding SQL Injection Vulnerabilities
The video outlines methodologies for finding vulnerabilities based on the testing perspective:

| Testing Method        | Perspective        | Key Actions                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| :-------------------- | :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Black Box Testing** | External           | **1. Map the Application:** Visit the URL, walk through all pages, and list all input vectors (URL parameters, forms, headers). *Do not just rely on scanners; understand the application logic.*<br>**2. Fuzzing:** Submit SQL-specific characters (`'`, `"`, `#`, `--`) to input vectors.<br>• Look for errors (Error-based).<br>• Inject Boolean conditions like `OR 1=1` (Boolean-based).<br>• Inject time delays like `pg_sleep` (Time-based).<br>• Trigger external network interactions (Out-of-band). |
| **White Box Testing** | Source Code Access | **1. Enable Logging:** Turn on web server and database logging to see exactly how inputs are processed.<br>**2. Code Review:** Map inputs to code paths. Use `grep` to search for SQL execution functions/Regex patterns and trace the data flow.<br>**3. Verification:** If a potential vulnerability is found in code, attempt to exploit it to confirm it is actually reachable.                                                                                                                           |

---

## 4. Exploiting SQL Injection
Detailed techniques for exploiting the specific types identified:

### Exploiting Error-based SQLi
* **Goal:** Distinct errors.
* **Method:** Submit characters like `'` or `"` and analyze the error message. It may reveal the database type (MySQL, PostgreSQL) or table names, simplifying further attacks.

### Exploiting Union-based SQLi
* **Goal:** Dump data from other tables.
* **Rules for UNION:**
    1. Same number of columns in both queries.
    2. Compatible data types in corresponding columns.
* **Steps:**
    1.  **Determine Column Count:** Use `ORDER BY x` (increment `x` until an error occurs) or `UNION SELECT NULL, NULL...` (add `NULL`s until the error disappears).
    2.  **Identify Data Types:** Replace `NULL`s with strings (e.g., `'a'`) one by one to see which columns accept text.
    3.  **Dump Data:** Use the valid string columns to select sensitive data (e.g., `UNION SELECT username, password FROM users`).

### Exploiting Blind SQLi (Boolean & Time-based)
* **Goal:** Extract data character by character.
* **Boolean Method:** Ask true/false questions. The payload uses `SUBSTRING()` logic. If the page loads normally (True), the letter is correct. If not (False), try the next letter in the alphabet.
* **Time-based Method:** Ask conditional time questions (e.g., "Is the first letter 'a'? If yes, sleep for 10 seconds."). If the response takes 10+ seconds, the letter is 'a'.
* **Automation:** These require scripting (e.g., Python) or tools like SQLMap or Burp Intruder because thousands of requests are needed.

### Exploiting Out-of-band SQLi
* **Method:** Inject payloads that use database features (like `xp_dirtree` in MS SQL) to initiate a DNS lookup to a domain you control (e.g., via Burp Collaborator).
* **Verification:** If you see the DNS request in your logs, the injection was successful.

---

## 5. Preventing SQL Injection
The video emphasizes specific defenses, prioritized by effectiveness.

> **Primary Defense: Prepared Statements (Parameterized Queries)**
> * **The "Correct" Way:** This is the most effective defense.
> * **How it works:** The SQL query structure is defined *before* user input is added. User input is treated strictly as data, not executable code.
> * **Example:** `SELECT * FROM users WHERE user = ?`. The `?` is a placeholder filled later by the database driver, ensuring inputs like `' OR 1=1` are treated as a literal string, not SQL logic.

### Partial/Secondary Options (Use with Caution)
* **Stored Procedures:** Can be safe if implemented correctly, but can still be vulnerable if they use string concatenation internally.
* **Allow-list Input Validation:** Strictly defining what input is allowed (e.g., "Table name must be 'users'"). Useful for inputs that cannot be parameterized, like table names.
* **Escaping User Input:** Converting special characters to safe versions. Should be a *last resort*.

### Defense in Depth (Additional Layers)
* **Least Privilege:** The database application account should have only the minimum permissions necessary. Do not run as `sa` or `root`. This limits the damage if an injection occurs (e.g., preventing RCE).
* **Remove Default Functionality:** Disable unnecessary stored procedures or functions (like those allowing system commands or network requests).
* **Apply Security Patches:** Keep the database software up to date.

---

### Recommended Resources
* **PortSwigger Web Security Academy:** For hands-on labs.
* **The Web Application Hacker's Handbook:** Specifically Chapter 9 (Attacking Data Stores).
* **OWASP:** Testing Guide and Cheatsheets.
* **Tools:** SQLMap (for automated exploitation).
