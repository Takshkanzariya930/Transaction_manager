from flask import Flask, render_template, request, redirect, url_for, session, flash
import forms , db

app = Flask(__name__,template_folder="templates")
app.secret_key = "my_secret_key"


@app.route('/', methods=['GET','POST'])
def login():
    
    form = forms.LoginForm()
    
    if request.method == "POST" and form.validate_on_submit():
        
        session['username'] = form.username.data
        session['password'] = form.password.data
        if not db.show_user_id(session["username"]):
            flash("Username Not Found")
            
        if db.check_password(session['username'],session['password']):
            return redirect(url_for("home"))
        else:
            flash("Password Incorrect")
            
    return render_template("login.html",form=form)

@app.route('/registration',methods=['GET','POST'])
def registration():

    form = forms.RegistrationForm()
    
    if request.method == "POST" and form.validate_on_submit():
        
        session['username'] = form.username.data
        session['email'] = form.email.data
        session['password'] = form.password.data
        
        if db.show_user_id(session["username"]):
           flash("Username already exists")
           
        if db.show_email(session['email']):
            flash("Email is already linked")
        
        if db.create_user(session['username'], session['email'], session['password']) == True:
            flash("Registration complete")
            return redirect(url_for("login"))
                
    return render_template("register.html", form=form)

@app.route('/home')
def home():
    
    if not session.get('username'):
        flash("You must log in first.", "warning")
        return redirect(url_for('login'))
    
    transactions = db.recent_transaction(session["username"])
    return render_template("home.html",transactions=transactions)

@app.route('/add_member', methods=['GET','POST'])
def add_member():
    
    if not session.get('username'):
        flash("You must log in first.", "warning")
        return redirect(url_for('login'))
    
    form = forms.MembersForm()
    members = db.show_all_members(db.show_user_id(session['username'])[0])
    
    if request.method == "POST" and form.validate_on_submit():
        
        session['membername'] = form.membername.data
        
        if not db.show_member_id_user(session['membername'],db.show_user_id(session['username'])[0]):
            db.add_member(session['membername'], db.show_user_id(session['username'])[0])
        else:
            flash("Member already exists")
            
        return redirect(url_for('add_member'))
    
    return render_template("addmember.html", form=form, members=members)

@app.route('/add_transaction',methods=['GET','POST'])
def add_transaction():
    
    if not session.get('username'):
        flash("You must log in first.", "warning")
        return redirect(url_for('login'))
    
    form = forms.TransactionForm()
    form.member.choices = [(x,x) for x in db.show_all_members(db.show_user_id(session['username'])[0])]
    transactions = db.recent_transaction(session["username"])
    
    if request.method == "POST" and form.validate_on_submit():
        session['membername'] = form.member.data
        
        if db.add_transaction(db.show_member_id(session['membername'])[0],db.show_user_id(session["username"])[0],form.amount.data,form.ttype.data,form.note.data,form.date.data) == True:
            flash("Transaction Added successfully")
        
        else:
            flash("Transaction Failed ")
            
        return redirect(url_for('add_transaction'))
        
    return render_template("transaction.html", form=form, transactions=transactions)

@app.route('/view_transactions',methods=['GET','POST'])
def view_transactions():
    
    lend = 0
    borrowed = 0
    
    if not session.get('username'):
        flash("You must log in first.", "warning")
        return redirect(url_for('login'))
    
    form = forms.Selectmember()
    form.member.choices = [(x,x) for x in db.show_all_members(db.show_user_id(session['username'])[0])]
    transactions = db.recent_transaction(session["username"])
    
    if request.method == 'POST' and form.validate_on_submit():
        session['membername'] = form.member.data
        transactions = db.show_all_transaction_member(db.show_user_id(session["username"])[0],db.show_member_id(session["membername"])[0])
        
        lend,borrowed = db.total_amount_member(db.show_user_id(session['username'])[0],db.show_member_id(session['membername'])[0])
    
    return render_template("viewtransaction.html",form=form,transactions=transactions,lend=lend,borrowed=borrowed)

@app.route('/delete/member',methods=['GET','POST'])
def deletem():
    
    if not session.get('username'):
        flash("You must log in first.", "warning")
        return redirect(url_for('login'))
    
    form = forms.DeleteMember()
    members = db.show_all_members(db.show_user_id(session['username'])[0])
    form.member.choices = [(x,x) for x in db.show_all_members(db.show_user_id(session['username'])[0])]   
    
    if request.method == 'POST' and form.validate_on_submit():
        session['memberid'] = db.show_user_id(form.member.data)[0]
        
        if db.delete_member(session['memberid'], db.show_user_id(session['username'])[0]) == True :
            flash("Member Deleted")
        else:
            flash("Member was NOT deleted")
        
    return render_template("deletionm.html", form=form, members=members)

@app.route('/delete/transaction',methods=['GET','POST'])
def deletet():
    
    if not session.get('username'):
        flash("You must log in first.", "warning")
        return redirect(url_for('login'))
    
    form = forms.DeleteTransaction()
    form.tid.choices = [(x[0],x[0]) for x in db.show_all_transaction(db.show_user_id(session['username'])[0])]
    transactions = db.recent_transaction(session["username"])
    
    if request.method == 'POST' and form.validate_on_submit():
        session['transactionid'] = form.tid.data
        # Ensure correct index for user id
        user_id_list = db.show_user_id(session['username'])
        if user_id_list:
            if db.delete_transaction(session['transactionid'], user_id_list[0]) == True:
                flash("Transaction Deleted Successfully")
            else:
                flash("Transaction is not deleted")
        else:
            flash("User not found.")

    return render_template("deletiont.html", form=form, transactions=transactions)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)