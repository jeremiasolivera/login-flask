#import modulo1
from modulo1 import resta,suma,nombre
from mi_paquete.funciones import solucion_vacia,palabra
#alias
import mi_paquete.funciones as funciones

# Importar subpaquete
from mi_paquete.subpaquete.funciones_avanzadas import contar_letras 


print(resta(19,2))
print(solucion_vacia(19))
print(palabra)

"""
print(modulo1.resta(1,2))
print(modulo1.suma(1,2))
"""

print(nombre)
print(funciones.solucion_vacia(1))

print(contar_letras("Jeremias"))