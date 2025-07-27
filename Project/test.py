import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password='password', database="transaction_manager")

cursor = conn.cursor()

def create_user(username,email):
    try:
        cursor.execute(f"INSERT INTO users(name,email) VALUES ('{username}','{email}')")
        print("User added...............")
        conn.commit()
        
    except Exception as e:
        print("Error : ", e)
        print("User Already exists")
      
      
def add_member(membername,uid):
    try:
        cursor.execute(f"INSERT INTO members(name,uid) VALUES ('{membername}',{uid})")
        print("Member added...............")
        conn.commit()
        
    except Exception as e:
        print("Error : ", e)

def add_transaction(mid,uid,amount,ttype,note,transfered_at):
    try:
        cursor.execute(f"SELECT * FROM members WHERE mid = {mid} AND uid = {uid}")
        result = cursor.fetchone()
        
        if result:
            cursor.execute(f"INSERT INTO trans(mid,uid,amount,ttype,note,transfered_at) VALUES({mid},{uid},{amount},'{ttype}','{note}','{transfered_at}')")
            print("Transaction recorded...............")
            conn.commit()
        
        else:
            print("member notfound...........................")
        
    except Exception as e:
        print("Error : ", e)

def delete_transaction(tid,uid):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE tid = {tid} AND uid = {uid}") 
        result = cursor.fetchone()
        
        if result:
            cursor.execute(f"DELETE FROM trans WHERE tid = {tid}")
            print("Transaction deleted................. ")
            conn.commit()
            
        else:
            print("access denied...........................")   
    except Exception as e:
        print("Error : ", e)

def total_amount_menber(uid,mid):
    try:     
        cursor.execute(f"SELECT SUM(amount) FROM trans WHERE uid={uid} AND mid={mid} AND ttype='lend'")
        result1 = cursor.fetchone()
        cursor.execute(f"SELECT SUM(amount) FROM trans WHERE uid={uid} AND mid={mid} AND ttype='borrow'")
        result2 = cursor.fetchone()
        print(result1[0] - result2[0])
        
    except Exception as e:
        print("Error : ", e)

def show_all_transaction_member(uid,mid):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE uid={uid} AND mid={mid}")
        result = cursor.fetchall()
        
        for i in result:
            print(i[3:])
            
    except Exception as e:
        print("Error : ", e)
        
def show_all_transaction(uid):
    try:        
        cursor.execute(f"SELECT * FROM trans WHERE uid={uid}")
        result = cursor.fetchall()
        
        for i in result:
            print(i[3:])
            
    except Exception as e:
        print("Error : ", e)

def show_all_members(uid):
    try:        
        cursor.execute(f"SELECT * FROM members WHERE uid={uid}")
        result = cursor.fetchall()
        
        for i in result:
            print(i[:-1])
            
    except Exception as e:
        print("Error : ", e)

# create_user(username="43rand",email="124rand@gmail.com")
# add_member(membername="rand mem",uid=23)
# add_transaction(1,23,500,"lend","wafer 23","2024-07-27 14:42:43")
# delete_transaction(3,23)
# total_amount_menber(31,23)
# show_all_transaction_member(31,23)
# show_all_transaction(31)
# show_all_members(31)