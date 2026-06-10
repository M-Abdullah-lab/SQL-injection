# SQL Injection - Lab #2 SQL injection vulnerability allowing login bypass
## Video Overview
This video walks through Lab #2 of the PortSwigger Web Security Academy SQL Injection module. The lab focuses on a vulnerability in the login functionality that allows an attacker to bypass authentication and log in as the administrator without knowing the password. The video covers both the manual exploitation steps and the creation of a Python script to automate the attack.
## 1. The Scenario & Objective
* **Lab:** SQL injection vulnerability allowing login bypass.
* **Target:** A shopping application with a login page.
* **Vulnerability:** SQL injection in the login functionality.
* **Goal:** Perform a SQL injection attack to log in specifically as the administrator user.
## 2. Manual Exploitation Steps
### Step A: Mapping & Analysis
* **Input Vectors:** The login page accepts a username and password.
* **Initial Testing (Fuzzing):**
* Attempting to log in with admin / admin returns "Invalid username or password" (Generic error message, which is good security practice to prevent username enumeration).
* Injecting a SQL specific character (single quote ') into the username field (e.g., admin') results in an Internal Server Error (500).
* **Conclusion:** The 500 error suggests the single quote broke the backend SQL query syntax, confirming the vulnerability.
### Step B: Hypothesizing the Backend Query
Based on standard login logic, the backend query likely resembles:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SELECT * FROM users WHERE username = 'user_input' AND password = 'password_input'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Goal:** Manipulate this query so the database ignores the password check entirely.
### Step C: Crafting the Payload
* **Strategy:** Comment out the rest of the query after the username match.
* ***Payload Components:***
1. administrator : The target username.
2. ' : Closes the string literal for the username in the SQL query.
3. -- : The SQL comment indicator (for many SQL databases like PostgreSQL, SQLite, etc.). This tells the database to ignore everything that comes after it (i.e., the password check).
4. Final Payload: administrator' --
5. Resulting Query:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SELECT * FROM users WHERE username = 'administrator' --' AND password = '...'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The database executes only the part before the --. The password check is effectively removed.
### Step D: Execution
* Username Field: administrator' --
* Password Field: Any random text (it gets ignored).
* Outcome: The application logs you in as the administrator, and a "Log out" button appears, confirming success.
