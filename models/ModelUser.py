#from .entities import User
#from .entities.User import check_password_hash  # Corrige la importación
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self,id,username,password,fullname="") -> None:
        self.id=id
        self.username=username
        self.password=password
        self.fullname=fullname

    @classmethod
    def check_password(cls,hashed_password,password):
        return check_password_hash(hashed_password,password)


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3])
                
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1],None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self, db, user):
        try:
            cursor=db.connection.cursor()
            sql="INSERT INTO user(id,username,password,fullname) VALUES (null, '{}','{}','{}')".format(user.username,generate_password_hash(user.password,method='pbkdf2'),user.fullname)
            cursor.execute(sql)
            db.connection.commit()
            cursor.close()
        except Exception as ex:
            raise Exception(ex)


