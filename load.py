app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-02.cleardb.net'
app.config['MYSQL_USER'] = 'b8a30b72c2b3f4'
app.config['MYSQL_PASSWORD'] = '17088485'
app.config['MYSQL_DB'] = 'heroku_6c79d3633a7e6ba'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

(name, email, username, password,fabfood)

cur = mysql.connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (
id MEDIUMINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL
    )")
