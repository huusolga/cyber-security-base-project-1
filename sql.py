"""
Fix 4: Identification and Authentication Failures

Import regular expressions

import re
"""

from sqlalchemy.sql import text

"""
Fix 2: Cryptographic Failures

Import hash function

from werkzeug.security import generate_password_hash
"""

from database import db

def add_user(username, password):
    """
    Fix 2: Cryptographic failures
    
    Commented code hashes password before storing in database

    
    password_hash = generate_password_hash(password)
    """

    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"

        """
        Fix 4: Identification and Authentication Failures

        Code below checks if password fills the requirements, otherwise it gives a message what is missing.

        if len(password) < 8:
           print("Password must contain at least 8 characters")
        elif re.search('[0-9]',password) is None:
            print("Password must contain at least one number")
        else:
            db.session.execute(text(sql), {"username":username, "password":password})
            db.session.commit()
        """

        db.session.execute(text(sql), {"username":username, "password":password})
        
        """
        Fix 2: Cryptographic Failures

        Code below stores the hashed password instead of the plaintext password and replaces the code above in a fixed version

        
        db.session.execute(text(sql), {"username":username, "password":password_hash})
        """
        
        db.session.commit()
    except:
        return False
    return username, password

def get_user(username):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchone()

def create_todo(content, username):
    sql = "INSERT INTO todos (content, username, created_at) VALUES ('" + content + "', '" + username + "', NOW()) RETURNING id"
    db.session.execute(text(sql))

    """
    Fix 3: Injection

    Code below uses input sanitization and should replace the code above

    sql = "INSERT INTO todos (content, username, created_at) VALUES (:content, :username, NOW()) RETURNING id"
    db.session.execute(text(sql), {"content":content, "username":username})
    """
    
    db.session.commit()

def get_todos(username):
    sql = "SELECT * FROM todos WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchall()

def remove_todo(id):
    sql = "DELETE FROM todos WHERE todos.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def remove_user(id):
    sql = "DELETE FROM users WHERE users.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def get_users():
    sql = "SELECT * FROM users"
    result = db.session.execute(text(sql))

    return result.fetchall()
