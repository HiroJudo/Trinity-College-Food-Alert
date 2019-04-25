from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mail import Mail
from flask_mail import Message
from hasMather import scrapefood

app = Flask(__name__)
mail = Mail(app)

# mysql://b8a30b72c2b3f4:17088485@us-cdbr-iron-east-02.cleardb.net/heroku_6c79d3633a7e6ba?reconnect=true
# Config MySQL
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-02.cleardb.net'
app.config['MYSQL_USER'] = 'b8a30b72c2b3f4'
app.config['MYSQL_PASSWORD'] = '17088485'
app.config['MYSQL_DB'] = 'heroku_6c79d3633a7e6ba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Config flask_mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bonjovi0904@gmail.com'
app.config['MAIL_PASSWORD'] = 'Fumi22812100904'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# init MYSQL
mysql = MySQL(app)
mail = Mail(app)

#Articles = Articles()

# Index
@app.route('/')
def index():
    """
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    message = "Hello"
    for customer in data:
        address = customer['email']
        msg = Message("Clamming season",sender="bonjovi0904@gmail.com",recipients=[address])
        msg.body = "Hello " +customer['name']+ ". Your favorite menu " + customer['fabfood'] + " is in mather dining hall"
        #if hasFood(customer['fabfood']) == 1:
        #   mail.send(msg)
    """
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            print(password)
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard',username=username))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    # Create cursor
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form['food_name'] != '':
            newfood = request.form['food_name']
            result = cur.execute("SELECT * FROM favfood WHERE username = %s AND food = %s", (username, newfood))
            #cur = mysql.connection.cursor()
            if result <= 0:
                cur.execute("INSERT INTO favfood(username, food) VALUES(%s, %s)", (username, newfood))
                mysql.connection.commit()
            #cur.close()
            redirect(url_for('dashboard',username=username))
    # Get user by username
    result = cur.execute("SELECT * FROM favfood WHERE username = %s", [username])
    food = cur.fetchall()

    return render_template('dashboard.html', food=food)


@app.route('/delete_food/<food>', methods=['GET', 'POST'])
def delete_food(food):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM favfood WHERE username=%s and food=%s", (session['username'], food))
    mysql.connection.commit()
    print(session['username'])
    return redirect(url_for('dashboard',username=session['username']))


app.secret_key='ftamada'
if __name__ == '__main__':
    #app.secret_key='ftamada'
    app.run(debug=True)
