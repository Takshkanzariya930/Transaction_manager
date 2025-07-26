import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password='password', database="transaction_manager")

cursor = conn.cursor()

def create_user(id,username,email):
    try:
        cursor.execute(f"INSERT INTO users(id,name,email) VALUES ({id},'{username}','{email}')")
        print("User added...............")
        conn.commit()
        
    except Exception as e:
        print("Error : ", e)
        print("User Already exists")
      
      
def add_member(id,membername,uid):
    try:
        cursor.execute(f"INSERT INTO members(mid,name,uid) VALUES ({id},'{membername}',{uid})")
        print("Memberr added...............")
        conn.commit()
        
    except Exception as e:
        print("Error : ", e)

def add_transaction():
    pass

# create_user(id=1,username="rand",email="rand@gmail.com")
# add_member(id=1,membername="rand mem",uid=23)