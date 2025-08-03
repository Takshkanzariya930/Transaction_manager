from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, Email, NumberRange
import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username should not be EMPTY !!")])
    email = EmailField('Email', validators=[InputRequired(message="Email should not be EMPTY !!"), Email(message="Invalid email address")])
    password = PasswordField('New Password', validators=[InputRequired(message="Username should not be EMPTY !!"), EqualTo('confirm', message='Passwords must match'), Length(min=8, message="Password must be at least 8 characters")])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="Username should not be EMPTY !!")])
    password = PasswordField('password', validators=[InputRequired(message="Password should not be EMPTY !!"),Length(min=8, max=20, message="Password must be at least 8 characters")])
    submit = SubmitField('login')
    
class MembersForm(FlaskForm):
    membername = StringField('Member Name', validators=[InputRequired(message="Name can not be EMPTY !!")])
    submit = SubmitField('Add')
    
class TransactionForm(FlaskForm):
    member = SelectField('Select Member',choices=[])
    amount = FloatField("amount", validators=[InputRequired(message="Add amount !!"),NumberRange(min=0.0, message="Amount must be positive.")])
    ttype = SelectField('Type', choices=[('borrow', 'Borrow'), ('lend', 'Lend')])
    note = StringField('Note', validators=[InputRequired(message="Note should not be EMPTY !!")])
    date = DateField('Date & Time', format='%Y-%m-%d',  validators=[InputRequired(message="Date Required !!")])
    submit = SubmitField('Add')
    
class Selectmember(FlaskForm):
    member = SelectField('Select Member',choices=[])
    submit = SubmitField('Show')

class DeleteTransaction(FlaskForm):
    member = SelectField('Select Member',choices=[])
    tid = SelectField('Select Member',choices=[])
    submit = SubmitField('Delete')