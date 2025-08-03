import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password='password', database="transaction_manager")

cursor = conn.cursor()

def create_user(username,email,password):
    try:
        cursor.execute(f"INSERT INTO users(name,email,password) VALUES ('{username}','{email}','{password}')")
        conn.commit()
        return True
        
    except Exception as e:
        return e
      
      
def add_member(membername,uid):
    try:
        cursor.execute(f"INSERT INTO members(name,uid) VALUES ('{membername}',{uid})")
        conn.commit()
        
        return True
        
    except Exception as e:
        return e

def add_transaction(mid,uid,amount,ttype,note,transfered_at):
    try:
        cursor.execute(f"SELECT * FROM members WHERE mid = {mid} AND uid = {uid}")
        result = cursor.fetchone()
        
        if result:
            cursor.execute(f"INSERT INTO trans(mid,uid,amount,ttype,note,transfered_at) VALUES({mid},{uid},{amount},'{ttype}','{note}','{transfered_at}')")
            conn.commit()
            
            return True
        
        else:
            return False
        
    except Exception as e:
        return e

def delete_transaction(tid,uid):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE tid = {tid} AND uid = {uid}") 
        result = cursor.fetchone()
        
        if result:
            cursor.execute(f"DELETE FROM trans WHERE tid = {tid}")
            conn.commit()
            
            return True
            
        else:
            return False   
            
    except Exception as e:
        return e
    
def delete_member(mid,uid):
    try:        
        cursor.execute(f"SELECT * FROM members WHERE mid = {mid} AND uid = {uid}") 
        result = cursor.fetchone()
        
        if result:
            cursor.execute(f"DELETE FROM members WHERE mid = {mid}")
            conn.commit()
            
            return True 
            
    except Exception as e:
        return e
    

def total_amount_member(uid,mid):
    try:     
        cursor.execute(f"SELECT SUM(amount) FROM trans WHERE uid={uid} AND mid={mid} AND ttype='lend'")
        result1 = cursor.fetchone()
        cursor.execute(f"SELECT SUM(amount) FROM trans WHERE uid={uid} AND mid={mid} AND ttype='borrow'")
        result2 = cursor.fetchone()
        return result1[0] - result2[0]
        
    except Exception as e:
        return e

def show_all_transaction_member(uid,mid):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE uid={uid} AND mid={mid}")
        result = cursor.fetchall()
        
        return [i[3:] for i in result]
            
    except Exception as e:
        return e
        
def show_all_transaction(uid):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE uid={uid}")
        result = cursor.fetchall()
        
        return [i[3:] for i in result ]
    
    except Exception as e:
        return e

def show_all_members(uid):
    try:        
        cursor.execute(f"SELECT name FROM members WHERE uid={uid}")
        result = cursor.fetchall()
        
        return [i[0] for i in result]
              
    except Exception as e:
        return e
        
def show_user_id(username):
    try:        
        cursor.execute(f"SELECT id FROM users WHERE name='{username}'")
        result = cursor.fetchall()
        
        return [i[0] for i in result]
              
    except Exception as e:
        return e

def show_email(email):
    try:        
        cursor.execute(f"SELECT id FROM users WHERE email='{email}'")
        result = cursor.fetchall()
        
        return [i[0] for i in result]
              
    except Exception as e:
        return e

def show_member_id(membername):
    try:        
        cursor.execute(f"SELECT mid FROM members WHERE name='{membername}'")
        result = cursor.fetchall()
        
        return [i[0] for i in result]
              
    except Exception as e:
        return e
    
def show_member_id_user(membername,uid):
    try:        
        cursor.execute(f"SELECT mid FROM members WHERE name='{membername}' AND uid={uid}")
        result = cursor.fetchall()
        
        return [i[0] for i in result]
              
    except Exception as e:
        return e
    
def recent_transaction(username):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE uid={show_user_id(username)[0]} ORDER BY created_at")
        result = cursor.fetchall()
        
        return [i for i in result]
              
    except Exception as e:
        return e
    
def check_password(username,password):
    try:        
        cursor.execute(f"SELECT * FROM users WHERE id={show_user_id(username)[0]} AND password='{password}'")
        result = cursor.fetchall()
        
        return [i for i in result]
              
    except Exception as e:
        return e

# print(create_user(username="4rand",email="124rand@gmail.com",password="password12"))
# print(add_member(membername="rand mem",uid=23))
# print(add_transaction(1,23,500,"lend","wafer 23","2024-07-27 14:42:43"))
# print(delete_transaction(3,23))
# print(total_amount_member(31,23))
# print(show_all_transaction_member(31,23))
# print(show_all_transaction(32))
# print(show_all_members(31))
# print(show_user_id('Bob'))
# print(show_member_id('Member1'))
# print(recent_transaction('Bob'))
# print(check_password('Bob','password31'))
# print(delete_member(31,39))
