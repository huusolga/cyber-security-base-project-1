# Cyber security base - Project 1

This project is a part of the Cyber Security Base course. The Todo App is a simple application where users can create an account, log in, enter chores to the to do-list, and check them once finished. This project uses Flask instead of Django that was used in the course, but I've provided instruction for starting the application below. After the instruction, you'll also find the essay required in this assignment.

## Installing instructions

1. Open your terminal and clone the repository:
```bash
git clone https://github.com/huusolga/cyber-security-base-project-1
```
2. Move to the project’s directory:
```bash
cd csb-project1
```
3. Install PostgresSQL

If you’re using… 
- Linux: use [this installation script](https://github.com/hy-tsoha/local-pg)
- Windows: download the installation package from [Postgres website](https://www.postgresql.org/download/)
- Mac: use [Postgres.app](https://postgresapp.com/)
  
4. Create a new .env file
```bash
touch .env
```
Add this line to the file:

DATABASE_URL=address

where address is postgresql+psycopg2:// if Postgres was installed with Linux and otherwise postgresql:///user where “user” is the name of the database that shows up when opening the PostgreSQL interpreter.

5. Activate a virtual environment:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

6. Install the requirements:
```bash
pip install -r requirements.txt
```
7. Open an another terminal and start Postgres:
```bash
start-pg.sh
```
8. Define the database schema:
```bash
psql < schema.sql
```
9. Start the Todo App:
```bash
flask run
```
You'll find the Todo App by default at localhost:5000

## Essay 

I used the OWASP 2021 Top 10 list [1].

### Flaw 1: A01 Broken Access Control
Link to Flaw 1: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L106 

Broken Access Control risk means a vulnerability that allows users to have access to something that they aren’t permitted to. This could include things like sensitive information or the ability to perform certain functions outside their initial limits.
A Broken Access Control risk is implemented in the Todo App by allowing anyone to access the admin page. If you modify the url address by adding “/admin_page”, you’ll gain access to the admin page and can see each user’s username and password. This is an obvious security flaw since it is very easy to retrieve sensitive information.

To fix this vulnerability, it is checked whether the user is logged in as an admin or not before opening the admin page. If the user isn’t admin, they are directed to the index page. The fix is commented in the code and you can see it through the link below:

Link to Fix 1: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L109-115

## Flaw 2: A02 Cryptographic Failures
Link to Flaw 2: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L44

Cryptographic Failures focus on the most sensitive data such as passwords, credit card numbers and other such personal information. This kind of sensitive information should be handled with additional care. 

However, the Todo App stores passwords as they are given, without any encryption, which counts as a Cryptographic Failure. This is a security risk because in case of a data breach, attackers would see each user’s passwords immediately.

Instead, passwords should always be encrypted so even in case of a data breach, the passwords have an extra layer of protection since attackers won’t know which hashing technique was used. The weakness is fixed in the code by hashing the passwords before storing them. For this, the werkzeug.security library is imported in routes.py and sql.py. 

Fix in routes.py: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L69

Fixes in sql.py:

Creating hashed password: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L21-25

Storing the hashed password: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L47-51

## Flaw 3: A03 Injection
Link to Flaw 3: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L65

The input provided by the user should always be filtered or sanitized. Otherwise, if the input is formulated in a certain way, it is treated as code in the program. This allows for untrusted users to execute malicious code and as a result for example leak sensitive information or in turn, destroy them. This vulnerability risk is called an injection.

A common injection type is an SQL injection, which is also implemented in the Todo App. The vulnerability here is that username and password inputs are taken and put in the SQL command as is. 
The injection vulnerability is fixed simply by inserting a sanitized input in the command, so that the input is treated as a string.

Link to Fix 3: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L69-74

## Flaw 4: A07 Identification and Authentication Failures:
Link to Flaw 4: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L28-44

Confirming the user's identity, using strong authentication methods, and proper session management are crucial in withholding security and are at the core of Identification and Authentication Failures. When creating a user account in the Todo App, the username and password can be anything. However, this allows for the password to be something like “123” or the same as the username, which are very weak for example in a brute force attack where passwords are retrieved through trial and error. 

To fix this, an additional check for the password is included in the code. It checks whether it’s over eight characters long and if it has a number in it. If the password fails either of those requirements, the account isn’t created and the app prints what’s missing from the password.
Ideally there are even more requirements for a password, like having to contain both lower and upper case letters as well as symbols like the exclamation mark or parenthesis, but this is just a simple example how to improve this specific application.

Fix in HTML: https://github.com/huusolga/cyber-security-base-project-1/blob/main/templates/register.html#L28-30

Fix on sql.py: https://github.com/huusolga/cyber-security-base-project-1/blob/main/sql.py#L31-41

## Flaw 5: A09 Security Logging and Monitoring Failures:
Link to Flaw 5: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L51-96

Security Logging and Monitoring Failures refer to risks that occur during active breaches. An application should be equipped to detect and respond to breaches while they’re happening by noticing unusual activity. This can be achieved by logging and monitoring for example failed logins, errors or high-value transactions.

In the Todo App, there is no limit to how many times you try to log in. The risk here is that suspicious or malicious behaviour like brute force attacks cannot be detected since the number of attempted logins aren’t being counted. It is suspicious and should be looked into if someone’s tried to log in to an account an excessive amount of times.

The fix here is to set a limit to log in tries, after which you can’t attempt it anymore. The fix in the code is very simple and doesn’t give you more tries after a certain amount of time, like most applications. 

Links to Fix 5: 

Initializing the times the user has tried to login: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L83-85

Increasing the number of failed logins: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L91-93

Can't login if user has too many tries: https://github.com/huusolga/cyber-security-base-project-1/blob/main/routes.py#L54-59


### Sources

[1] https://owasp.org/Top10/ 




