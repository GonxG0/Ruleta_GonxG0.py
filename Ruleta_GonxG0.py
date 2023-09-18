
from tkinter import *
from tkinter import ttk

import tkinter as tk
from PIL import ImageTk, Image

import math
import random

import functools

def monto(dato): # Sube o baja la intencion de la apuesta segun el boton seleccionado
	
	global apuesta
	
	apuesta = apuesta + int(dato)
	actualizar()
	print(dato)

def salir():
	
	exit()
	
def actualizar(): #Se encarga de actualizar el numero de la apuesta, asegurandose de no poner apuestas negativas o sobrepasar el saldo actual
	
	global apuesta
	if apuesta < 0:
		
		apuesta = 0
		
	if saldo < apuesta:
		
		apuesta = saldo
	
	tks["labels"]["apuesta"].config(text=f"{apuesta}")
	
def ingreso(): # Segun la cantidad de intencion de la apuesta y la jugada seleccionada, consume el saldo y carga la jugada a la lista, si ya esta la jugada suma a la misma
	
	global saldo, apuesta
	
	if not opcion.get() == "" and  apuesta != 0:
		
		saldo-= apuesta
		tks["labels"]["saldo"].config(text=str(saldo))
		
		if opcion.get() in jugadas:
			
			jugadas[opcion.get()] += apuesta 
		
		else:
			
			jugadas[opcion.get()] = apuesta
		dibujo()
		apuesta = 0
		tks["labels"]["saldo"].config(text=str(saldo)) 
		
		actualizar()
		
		opcion.set("")
		
def dibujo(): #Dibuja todas las jugadas a la izquierda de la ventana
		
	global borrame, jugadas
	print(borrame)
	if borrame == True:
		
		for k in tks["labels apuesta"].keys():
			
			tks["labels apuesta"][k].place_forget()
			tks["labels apuesta"][k].destroy()
			
		tks["labels apuesta"] = {}
		borrame = False	

	for n,k in enumerate(jugadas):
		
		
		if k in tks["labels apuesta"].keys():
			
			tks["labels apuesta"][k].place_forget()
		
		tks["labels apuesta"][k] = tk.Label(text= f"{jugadas[k]} a {k}",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
		tks["labels apuesta"][k].place(x = des, y = (des+grosor)*(3+n)+des, width=(des+grosor)*3,height= grosor)
		
def lanzar(): #Por cada jugada que realizo se verifica si es validad, de serlo se añade el saldo segun la apuesta, a su vez se pintan las jugadas para entender la resolucion
	
	global saldo, borrame, jugadas
	
	numero = random.randint(0,36) # Gira la ruleta
	print(numero)
	for j,v in jugadas.items(): # Recorre todas las jugadas
	
		gano = False
		
		if j == str(numero):
		
			saldo += v * multiplicadores["pleno"]
			gano = True

		if j in calles and j == str(j):
			
			calle = math.ceil(numero/3)
			
			if j == "TRASVERSAL "+str(calle):
			
				saldo += v * multiplicadores["calle"]
				gano = True
			
		if j in ("COLUMNA 1","COLUMNA 2","COLUMNA 3","DOCENA 1","DOCENA 2","DOCENA 3"):
			
			columna = numero % 3
			
			if columna == 0:
				
				columna = 3
			docena = math.ceil(numero/12)
			
			if j == "COLUMNA "+str(columna) or j == "DOCENA "+str(docena):
			
				saldo += v * multiplicadores["s simples"]
				gano = True
			
		if j in ("PAR","ROJO","NEGRO","IMPAR","PASA","FALTA"):
			
			if numero in (1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36) and j == "NEGRO":
				
				saldo += v * multiplicadores["simples"]
				gano = True
				
			elif j == "ROJO" and not numero in (1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36): 
				
				saldo += v * multiplicadores["simples"]
				gano = True
				
			if numero % 2 == 0  and j == "PAR" and not numero == 0:

				saldo += v * multiplicadores["simples"]
				gano = True
				
			elif numero % 2 == 1  and j == "IMPAR" and not numero == 0:
				
				saldo += v * multiplicadores["simples"]
				gano = True
				
			if math.ceil(numero/18) == 1 and j == "FALTA":
				
				saldo += v * multiplicadores["simples"]
				gano = True
				
			elif math.ceil(numero/18) == 2 and j == "PASA":
				
				saldo += v * multiplicadores["simples"]
				gano = True
					
		if gano == True:
			
			tks["labels apuesta"][j].config(bg = "green3")
			
		else:
			
			tks["labels apuesta"][j].config(bg = "red4")
			
	borrame = True 

	#Se prepara todo para la siguiente ronda

	jugadas = {}
	actualizar()
	tks["labels"]["saldo"].config(text=str(saldo))
	tks["labels"]["lanzar"].config(text=str(numero),font=("Courier", 24))

# Se preparan los parametros geometricos para todo el sistema

ancho = 725 #Ancho de ventana

alto = 940 #Alto de ventana

des = 5 #Desfase entre botones

grosor = 50 #Grosor de botones

xx = ancho/2-((grosor+des)*3-des)/2+des-4

yy = alto-(des+grosor)*13

tks = 	{
		"botones" : 		{},
		"labels" :			{}, 
		"labels apuesta" :	{},
		"cajas" :			{}
		}

multiplicadores = 	{
					"pleno" : 		36,
					"semipleno": 	18,
					"calle":		12,
					"cuadro":		9,
					"linea":		6,
					"s simples":	3,
					"simples":		2
					}


jugadas = {}
veredicto = {}

#Creacion de botones mediante for y geometria para reducir codigo

calles = []
for n in range(12): 
	
	calles.append("TRASVERSAL "+str(n))

monedas = [1,5,10,25,50,100,500,1000]
colores = ("gray","red4","dodger blue3","green","orange red4","black","purple","yellow3")
			
borrame = False
apuesta = 0
saldo = 10000


ventana = Tk()
ventana.title("")
ventana.config(bg = "gray")
ventana.geometry(f"{ancho}x{alto}")

opcion = tk.StringVar()
opcion.set("")


#Creacion de botones mediante for y geometria para reducir codigo

for a in range(36): # Numeros del 1 al 36
	
	tks["botones"][str(a+1)] = tk.Radiobutton( text=str(a+1), variable=opcion, value=str(a+1), indicatoron=0,bg = "red4", fg = "white", activebackground = "red4", selectcolor = "red4",activeforeground = "white")
	
	if a in (2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35):
		
		tks["botones"][str(a+1)].config(bg = "black", activebackground = "black", fg = "white", selectcolor = "black",activeforeground = "white")
	
	tks["botones"][str(a+1)].place(x = xx + math.floor(a % 3)*(grosor+des), y = yy + math.floor(a / 3)*(grosor+des), width = grosor, height = grosor )

# Numero 0
tks["botones"]["0"] = tk.Radiobutton( text="0", variable=opcion, value="0", indicatoron=0,bg = "green4", fg = "white", activebackground = "green4", selectcolor = "green4",activeforeground = "white")
tks["botones"]["0"].place(x = xx , y = yy -(grosor+des), width = (des+grosor)*3-des, height = grosor)

for e in range(3): # Columnas
	
	tks["botones"]["c"+str(e+1)] = tk.Radiobutton( text="C "+str(e+1), variable=opcion, value="COLUMNA "+str(e+1), indicatoron=0,bg = "yellow4", fg = "white", activebackground = "yellow4", selectcolor = "yellow4",activeforeground = "white")
	tks["botones"]["c"+str(e+1)].place(x = xx + math.floor(e % 3)*(grosor+des), y = yy + math.floor((a+1) / 3)*(grosor+des), width = grosor, height = grosor)
	
for i in range(12): # Transversal
	
	tks["botones"]["t"+str(i+1)] = tk.Radiobutton( text="T "+str(i+1), variable=opcion, value="TRASVERSAL "+str(i+1), indicatoron=0,bg = "purple", fg = "white", activebackground = "purple",selectcolor ="purple",activeforeground = "white")
	tks["botones"]["t"+str(i+1)].place(x = xx -(grosor+des), y = yy + (i)*(grosor+des), width = grosor, height = grosor)

for o in range(3): # Docenas
	
	tks["botones"]["d"+str(o+1)] = tk.Radiobutton( text="D\nO\nC\nE\nN\nA\n\n"+str(o+1), variable=opcion, value="DOCENA "+str(o+1), indicatoron=0,bg = "dodger blue3", fg = "white", activebackground = "dodger blue3",selectcolor ="dodger blue3",activeforeground = "white")
	tks["botones"]["d"+str(o+1)].place(x = xx + ((grosor+des)*3), y = yy + (o)*(grosor+des)*4, width = grosor, height = (grosor+des)*4-des)

palabra = ("PAR","ROJO","NEGRO","IMPAR")

for u in range(4): # ("Par","Rojo","Negro","Impar")
	
	tks["botones"][palabra[u]] = tk.Radiobutton(variable=opcion, value=palabra[u], indicatoron=0)
	
	final = palabra[u][0]
	
	for p in range(len(palabra[u])-1):
		
		final +="\n"+palabra[u][p+1]
	
	tks["botones"][palabra[u]].config(text = final)
	
	if palabra[u] in ("PAR","IMPAR"):
		
		tks["botones"][palabra[u]].config(bg = "sienna4", fg = "white", activebackground = "sienna4",selectcolor ="sienna4",activeforeground = "white")
		
	if palabra[u] == "ROJO":
		
		tks["botones"][palabra[u]].config(bg = "red4", fg = "white", activebackground = "red4",selectcolor ="red4",activeforeground = "white")
		
	if palabra[u] == "NEGRO":
		
		tks["botones"][palabra[u]].config(bg = "black", fg = "white", activebackground = "black",selectcolor ="black",activeforeground = "white")
	
	tks["botones"][palabra[u]].place(x = xx + ((grosor+des)*4), y = yy + (u)*(grosor+des)*3, width = grosor, height = (grosor+des)*3-des)


palabra = ("FALTA","PASA")	

for u in range(2): #("FALTA","PASA")	

	tks["botones"][palabra[u]] = tk.Radiobutton(variable=opcion, value=palabra[u], indicatoron=0,bg = "orange red4", fg = "white", activebackground = "orange red4",selectcolor ="orange red4",activeforeground = "white")

	final = palabra[u][0]
	
	for p in range(len(palabra[u])-1):
		
		final +="\n"+palabra[u][p+1]
	
	tks["botones"][palabra[u]].config(text = final)

	tks["botones"][palabra[u]].place(x = xx - ((grosor+des)*2), y = yy + (u)*(grosor+des)*6, width = grosor, height = (grosor+des)*6-des)

#################################################################################################
#################################################################################################
#################################################################################################

# Botones de apuestas

for c,n in enumerate(monedas): # Suma de apuestas

	tks["botones"]["+"+str(n)] = tk.Button(text="+"+str(n),command = functools.partial(monto,f"+{n}"))
	tks["botones"]["+"+str(n)].config(bg = colores[c], fg = "white", activebackground = colores[c],activeforeground = "white")
	tks["botones"]["+"+str(n)].place(x=des+ c*(des+grosor),y=des, width=grosor, height= grosor)
	
for c,n in enumerate(monedas):  # Resta de apuestas

	tks["botones"]["-"+str(n)] = tk.Button(text="-"+str(n),command = functools.partial(monto,f"-{n}"))
	tks["botones"]["-"+str(n)].config(bg = colores[c], fg = "white", activebackground = colores[c],activeforeground = "white")
	tks["botones"]["-"+str(n)].place(x=des+ c*(des+grosor),y=des*2+grosor, width=grosor, height= grosor)
	
	
tks["labels"]["saldo"] = tk.Label(text= str(saldo),bg = "antiquewhite2" ,activebackground= "antiquewhite2")
tks["labels"]["saldo"].place(x =des+(grosor+des)*len(monedas),y=des, width= (grosor+des)*3,height = (grosor))
	
tks["labels"]["apuesta"] = tk.Label(text= str(apuesta),bg = "antiquewhite2" ,activebackground= "antiquewhite2")
tks["labels"]["apuesta"].place(x =des+(grosor+des)*len(monedas),y=des*2+grosor, width= (grosor+des)*3,height = (grosor))

tks["botones"]["lanzar"] = tk.Button(text= "Lanzar",command= lanzar,bg = "antiquewhite2" ,activebackground= "antiquewhite2")
tks["botones"]["lanzar"].place(x =des*2+(grosor+des)*(len(monedas)+3),y=des, width= (grosor+des)*2-des,height = (grosor+des)*2-des)

tks["botones"]["ingreso"] = tk.Button(text= "Ingresar apuesta",command= ingreso,bg = "antiquewhite2" ,activebackground= "antiquewhite2")
tks["botones"]["ingreso"].place(x= des, y= (des+grosor)*2+des, width=ancho-des*2,height= grosor)

tks["labels"]["lanzar"] = tk.Label(text= "",bg = "antiquewhite2" ,activebackground= "antiquewhite2")
tks["labels"]["lanzar"].place(x = xx+ (des+grosor)*5,y=yy, width= (grosor+des)*3-des,height = (grosor+des)*3-des)

tks["botones"]["salir"] = tk.Button(text= "Salir",command= salir,bg = "antiquewhite2" ,activebackground= "antiquewhite2")
tks["botones"]["salir"].place(x =ancho-(grosor+des)*3,y=alto-(grosor+des), width= (grosor+des)*3-des, height = (grosor))

ventana.mainloop()



