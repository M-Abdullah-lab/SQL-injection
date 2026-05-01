# SQL Injection - Lab #1 SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
## Video Overview
This video is a practical walkthrough of Lab #1 from the PortSwigger Web Security Academy. It focuses on identifying and exploiting a simple SQL Injection (SQLi) vulnerability in the WHERE clause of a database query to retrieve hidden data (unreleased products). The video covers both the manual exploitation method and how to write a Python script to automate the attack.

---
## 1. The Scenario & Objective
* **Lab**: SQL injection vulnerability in the product category filter.
* **Application Logic**: The application displays products based on a category selected by the user.
* **Backend Query (Revealed):**

> SELECT * FROM products WHERE category = 'Gifts' AND released = 1

* The application filters for the selected category and checks if the product is released (released = 1).
* Goal: Modify the query to display all products, including those that are unreleased (released = 0).

---
## 2. Manual Exploitation Steps
The video follows a standard penetration testing methodology:
### Step A: Map the Application
* Browse the application to understand its logic.
* Identify Input Vectors: Clicking on a category (e.g., `Gifts`) updates the URL parameter: `.../filter?category=Gifts`
* This confirms the category parameter interacts with the database.
### Step B: Fuzzing & Detection
* Test for Errors: Submit a single quote `'` in the category parameter.
* Result: `Internal Server Error.`
* Analysis: The quote likely broke the SQL syntax (unclosed string), indicating a potential vulnerability.
* Confirm Syntax: Submit a quote followed by a comment characters (--).
* Payload: ' --
* Result: No error, but no products displayed (because the category was empty).
* Analysis: The query syntax was fixed by the comment, confirming we have control over the query structure.
### Step C: Crafting the Payload
* Objective: We want the query to return TRUE for every row, ignoring the category and the released status.
* Logic:
1. Close the category string: `'`
2. Add a generic "always true" condition: `OR 1=1`
3. Comment out the rest of the query (specifically the AND released = 1 check): `--`
4. Final Payload:
`' OR 1=1 --`
5. Resulting Backend Query:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SELECT * FROM products WHERE category = '' OR 1=1 --' AND released = 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Since `1=1` is always true, the database returns every row in the table.
* Outcome: The application displays all products, including a hidden unreleased product (e.g., "Cat Grin").
---
## 3. Automated Exploitation (Python Scripting)
The instructor demonstrates how to script the attack using Python to prepare for more complex scenarios (like Blind SQLi).
**Script Structure**
1. Libraries: Uses requests for HTTP calls, sys for arguments, and urllib3 to handle SSL warnings.
2. Proxy Setup (Debugging):
   * Configures the script to route traffic through Burp Suite (localhost:8080).
   * Why? To debug the script by inspecting the exact raw requests/responses sent by Python.
   * Core Logic:
     * Takes two command-line arguments: URL and Payload.
     * Constructs the full URL by appending the malicious payload to the category parameter.
     * Sends a GET request.
* Verification:
* Checks if the response body contains the name of the hidden product (e.g., "Cat Grin").
  * If found -> "SQL Injection Successful"
  * If not found -> "SQL Injection Unsuccessful"

**1. Key Takeaways & Tips**
* Mapping is Critical: Don't rely solely on scanners. Understand how the application processes input (e.g., URL parameters).
* Use a Proxy (Burp Suite): Even when scripting, routing traffic through a proxy allows you to debug effectively and see exactly what your script is sending vs. what the browser sends.
* Comments are Powerful: In SQLi, the comment character (-- in SQL, # in MySQL, etc.) is essential to "cut off" the rest of the original query so your injected logic validates correctly.
