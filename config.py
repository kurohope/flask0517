HOST = "localhost"
PORT = "3306"
DB = "new_info"
USER = "root"
PASS = "password"
CHARSET = "utf8"
DB_URI = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SECRET_KEY = "THIS-A-SECRET-KEY"

