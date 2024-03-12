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
from models.ModelProduct import Product
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


"""
    PRODUCT SECCION
"""

@app.route('/get_product')
@login_required
def get_product():
    productos=[]
    owner=current_user.id
    row=Product.get_product(db,owner)
    for p in row:
        productos.append([p[0],p[1],p[2],current_user.fullname])
    return render_template('products/get_products.html', productos=productos)

@app.route('/insert_product', methods=['GET','POST'])
@login_required
def insert_product():
    if request.method=='POST':
        try:
            nombre_producto=request.form['nombre']
            imagen_producto=request.form['imagen']
            owner=current_user.id

            mi_producto=Product(0,nombre_producto,imagen_producto,owner)
            Product.insert_product(db,mi_producto)
            #print(nombre_producto,imagen_producto)
            flash("Producto agregado correctamente")
            return(redirect(url_for('insert_product')))
        except Exception as ex:
            raise Exception(ex)

    return render_template('products/insert_products.html')



@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    p_eliminado=Product.delete_product(db,id)
    if p_eliminado == True:
        flash("Producto elimnado correctamente")
        return redirect(url_for('get_product'))
    else:
        flash("Algo salió mal")
        return redirect(url_for('get_product'))

@app.route('/update_product/<int:id>', methods=['GET','POST'])
@login_required
def update_product(id):
    cursor=db.connection.cursor()
    sql="SELECT id,nombre,imagen,owner FROM productos WHERE id='{}'".format(id)
    cursor.execute(sql)
    product=cursor.fetchone()
    db.connection.commit()
    cursor.close()
    if request.method=='POST':
        new_product=Product(id,request.form['nombre'],request.form['imagen'],current_user.id)
        Product.update_product(db,new_product)
        flash("Producto actualizado correctamente")
        return redirect(url_for('get_product'))
    else:
        return render_template('products/update_products.html', product=product)
   




if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()
    
    
    
