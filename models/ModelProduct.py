

class Product():

    def __init__(self,id,nombre,imagen,owner):
        self.id=id
        self.nombre=nombre
        self.imagen=imagen
        self.owner=owner

    @classmethod
    def get_product(self, db, id_user):
        try:
            cursor=db.connection.cursor()
            sql="SELECT id,nombre,imagen,owner FROM productos WHERE owner='{}'".format(id_user)
            cursor.execute(sql)
            all_products=cursor.fetchall()
            db.connection.commit()
            cursor.close()
            return all_products
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def insert_product(self, db, product):
        try:
            cursor=db.connection.cursor()
            sql="INSERT INTO productos(id,nombre,imagen,owner) VALUES (NULL,'{}','{}','{}')".format(product.nombre,product.imagen,product.owner)
            cursor.execute(sql)
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def delete_product(self, db, id_product):
        try:
            cursor=db.connection.cursor()
            sql="DELETE FROM productos WHERE id='{}'".format(id_product)
            cursor.execute(sql)
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def update_product(self, db, product):
        try:
            cursor=db.connection.cursor()
            sql="UPDATE productos SET nombre = '{}', imagen = '{}' WHERE id='{}';".format(product.nombre,product.imagen,product.id)
            cursor.execute(sql)
            db.connection.commit()
            cursor.close()
            return True
        except Exception as ex:
            raise Exception(ex)