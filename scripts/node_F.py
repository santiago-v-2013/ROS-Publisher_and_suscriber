#!/usr/bin/env python
## asegura que se ejecute como codigo de python

## Nodo F, recibe de C y envia a H
#Los nodos E,F,G funcionan de manera parecida en la recepcion de los datos

#se importan las librerias
import rospy
from std_msgs.msg import String
# Por defecto se asigna un valor de Bajo al caracter publicado
charF = 'B'

#callback toma el dato string y lo separa para hallar el valor bajo medio y alto enviado mediante split()
def callback(datos):
    global charF
    cadena = datos.data
    rospy.loginfo(cadena)
    partes1= cadena.split('/')
    for i in [0,1,2]:
	partes2= partes1[i].split('=')
	tipo1=partes2[0]
	if tipo1=="bajo":
		bajo=int((partes2[1]))
	if tipo1=="medio":
		medio=int((partes2[1]))
	if tipo1=="alto":
		alto=int((partes2[1]))

    # condicionales para decidir el caracter a enviar
    if alto>bajo and alto>medio:
	charF = 'A'
    elif medio>bajo and medio>alto:
	charF = 'M'
    elif bajo>medio and bajo>alto:
	charF = 'B'
    elif alto>bajo and alto == medio:
	charF = 'A'
    elif medio>alto and medio == bajo:
	charF = 'M'

#funcion node_F, inicializa el nodo, el publicador, el subscriber y publica el caracter CharF
def node_F():
    pub = rospy.Publisher('charF', String, queue_size=10)
    rospy.init_node('node_F', anonymous=False)
    rospy.Subscriber('stringC', String, callback)
    rate = rospy.Rate(0.5) # 1hz
    while not rospy.is_shutdown():
        pub.publish(charF)
        rate.sleep()

if __name__ == '__main__':
    try:
        node_F()
    except rospy.ROSInterruptException:
        pass
