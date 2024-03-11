from flask import Flask,render_template,request,redirect,url_for,flash
from config import config



#GENERADOR DE TOKEN CSRF
from flask_wtf.csrf import CSRFProtect


#LOGIN VALIDATOR
from flask_login import LoginManager,login_user,logout_user, login_required,current_user


# DB CLIENT
from flask_mysqldb import MySQL

# Models
from models.ModelUser import ModelUser

#Entities
from models.ModelUser import User

app=Flask(__name__)



db=MySQL(app)
login_manager_app=LoginManager(app)
csrf=CSRFProtect()

#VISTA LOGIN LOADER
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User(0,request.form['username'],request.form['password'])
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid Password")
                return render_template('auth/login.html')
        else:
            flash("User not found")
            return render_template('auth/login.html')
        
    else:
        return render_template('auth/login.html')

@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        data={
            'nombre':current_user.username,
            'contrasenia':current_user.password,
            'nombrecompleto':current_user.fullname,
        }
    return render_template('home.html',data=data)

@app.route('/protect')
@login_required
def protect():
    return "Vista protejida"

#Otra forma de enrutar
@app.route('/register', methods=['GET','POST'])
def registrar_usuario():

    if request.method == 'POST':       
        new_user=User(0,request.form['username'],request.form['password'],request.form['fullname'])
        ModelUser.register(db,new_user)
        return redirect(url_for('login'))
    else:
        return render_template('auth/register.html')

def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "Pagina no encontrada", 404



if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()
    
    
    
