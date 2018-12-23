from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from subprocess import call
from hashlib import md5
import os
import datetime
import ast


raiz = Tk() # Declaro la ventana

#Configuracion basica de la ventana
raiz.geometry("550x300")
raiz.resizable(False, False)
raiz.iconbitmap("imgs/icono.ico")
raiz.title("BackUp")
raiz.config(bg="#979AE8")
#Panel administrador

def solicitarContra():
	popup = Toplevel()
	popup.geometry("300x120")
	popup.resizable(False, False)
	popup.iconbitmap("imgs/icono.ico")
	popup.title("Contraseña Requerida")
	popup.config(bg="#979AE8")

	Label(popup, text="Ingrese la contraseña", font=10, bg="#979AE8").pack(pady=10)
	contra = Entry(popup, show='*')
	contra.pack(pady = 2)

	def panelAdmin():
		with open('archivos/hash.txt', 'r') as f:
			contramd5 = f.read()
		if str(md5(contra.get().encode()).digest()) != contramd5:
			popup.destroy()
			messagebox.showwarning("Advertencia", "La contraseña ingresada no es correcta")
		else:
			popup.destroy()
			panel = Toplevel()
			panel.resizable(True, False)
			panel.iconbitmap("imgs/icono.ico")
			panel.title("Panel de Administrador")
			panel.geometry("750x300")
			panel.config(bg="#979AE8")

			tkvar = StringVar()
			opciones = {'Escritorio', 'Documentos', 'Favoritos', 'Imagenes', 'Videos', 'Mail', 'Musica'}
			tkvar.set('-----------')
			scrolldown = OptionMenu(panel, tkvar, *opciones)
			scrolldown.pack(pady=30)

			f = open('archivos/rutas_dict.txt', 'r+')
			rutas = ast.literal_eval(f.read())
			f.close()
			def change_dropdown(*args):

				print(rutas[tkvar.get().lower()])
				origenlabel.config(text=rutas[tkvar.get().lower()][0])
				destinolabel.config(text=rutas[tkvar.get().lower()][1])


			tkvar.trace('w', change_dropdown)

			def cambiarOrigen():
				nuevo_origen = filedialog.askdirectory()
				rutas[tkvar.get().lower()][0] = nuevo_origen
				change_dropdown()
				panel.deiconify()

			def cambiarDestino():
				nuevo_destino = filedialog.askdirectory()
				rutas[tkvar.get().lower()][1] = nuevo_destino
				change_dropdown()
				panel.deiconify()

			def guardarCambios():
				file = open('archivos/rutas_dict.txt', 'w')
				file.write(str(rutas))
				file.close()
				messagebox.showwarning("Guardar", "Cambios guardados.")
				panel.deiconify()

			def Cancelar():
				respuesta = messagebox.askokcancel("Cancelar", "¿Seguro que desea descartar los cambios realizados?")
				if respuesta:
					panel.destroy()
				else:
					panel.deiconify()				

			frame = Frame(panel, bg="#979AE8")
			Label(frame, text="Origen: ", bg="#979AE8", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
			Label(frame, text="Destino: ", bg="#979AE8", font=('Arial', 10, 'bold')).grid(row=1, column=0, padx=5, pady=10)
			origenlabel = Label(frame, bg="#979AE8")
			origenlabel.grid(row=0, column=1, padx=5)
			destinolabel = Label(frame, bg="#979AE8")
			destinolabel.grid(row=1, column=1, padx=5, pady=10)
			Button(frame, text="Cambiar", command=cambiarOrigen, bg="#7B61E8", fg="white", font=('Arial', 10), cursor="hand2").grid(row=0, column=2, padx=5)
			Button(frame, text="Cambiar", command=cambiarDestino, bg="#7B61E8", fg="white", font=('Arial', 10), cursor="hand2").grid(row=1, column=2, padx=5, pady=10)
			frame.pack(pady=20, expand=True)
			frame2 = Frame(panel, bg="#979AE8")
			Button(frame2, text="Guardar cambios", command=guardarCambios, bg="green", fg="black", font=('Arial', 11), cursor="hand2").grid(row=0, column=0)
			Button(frame2, text="Cancelar", command=Cancelar, bg="red", fg="black", font=('Arial', 11), cursor="hand2").grid(row=0, column=1, padx=5)
			frame2.pack(anchor='s',side='right', padx=10, pady=10)


	Button(popup, text='Enviar', command=panelAdmin, bg="#7B61E8", fg="white", font=('Arial', 10), cursor="hand2").pack(pady = 15)


# Armo el Header
header=Frame()
header.config(bg="#7B61E8", pady=10)
Label(header, text="Applicación Back-up", font=("Georgia", 18),fg="white", bg="#7B61E8", padx=10).pack(side="left", anchor="n")
configuracionimg = PhotoImage(file="imgs/conf.png")
Button(header, image=configuracionimg, bg="#979AE8", command=solicitarContra, cursor="hand2").pack(side="right", anchor="n") # TODO: Pedir contraseña panel de admin
header.pack(fill='x', anchor='n')


#Armo el cuadro de opciones
escritorio = IntVar()
documentos = IntVar()
favoritos = IntVar()
videos = IntVar()
musica = IntVar()
imagenes = IntVar()
mail = IntVar()

#Funcion  que rescata las rutas del archivo de texto
rutasBk = {}
def obtenerRutas():
	f = open('archivos/rutas_dict.txt', 'r')
	rutas = ast.literal_eval(f.read())
	global rutasBk
	rutasBk = {}

	if escritorio.get() == 1:
		rutasBk['escritorio'] = rutas['escritorio']
	if documentos.get() == 1:
		rutasBk['documentos'] = rutas['documentos']
	if favoritos.get() == 1:
		rutasBk['favoritos'] = rutas['favoritos']
	if imagenes.get() == 1:
		rutasBk['imagenes'] = rutas['imagenes'] 
	if videos.get() == 1:
		rutasBk['videos'] = rutas['videos']
	if mail.get() == 1:
		rutasBk['mail'] = rutas['mail']
	if musica.get() == 1:
		rutasBk['musica'] = rutas['musica']

	f.close()

	


def realizarBackup():

	respuesta = messagebox.askokcancel("Back-up", "¿Desea apagar el equipo al finalizar?")
	raiz.withdraw()
	global rutasBk
	global ult_bk
	panel = Toplevel()
	panel.resizable(False, False)
	panel.iconbitmap("imgs/icono.ico")
	panel.title("Back-up en proceso")
	panel.geometry("300x85")
	panel.config(bg="#979AE8")

	Label(panel, text="Realizando Back-up...", font=12, bg="#979AE8").pack(pady=10)
	barra = ttk.Progressbar(panel, length=200, mode='determinate')
	barra.pack(pady=5)
	raiz.update_idletasks()
	barra['value'] = 0
	for categoria in rutasBk:
		call(["robocopy", rutasBk[categoria][0] ,  rutasBk[categoria][1] , "/S"])
		barra['value'] += (200 / len(rutasBk))
		raiz.update_idletasks()

	with open('archivos/ultimo.txt', 'w') as f:
		f.write(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

	panel.destroy()

	if respuesta:
		raiz.destroy()
		os.system("shutdown /s /t 1")
	else:
		messagebox.showinfo("Back-up", "Back-up finalizado.")
		raiz.deiconify()
	with open('archivos/ultimo.txt', 'r') as f:
		ultimo = f.read()
	ult_bk.config(text=ultimo)	
	raiz.update_idletasks()		


	

opciones = Frame()
opciones.config(bg = "#979AE8", pady=50)

#escimg = PhotoImage(file="imgs/escritoriono.png")
#docimg = PhotoImage(file="imgs/documentosno.png")
#favimg = PhotoImage(file="imgs/favoritosno.png")
#imgimg = PhotoImage(file="imgs/fotosno.png")
#vidimg = PhotoImage(file="imgs/videosno.png")
#mailimg = PhotoImage(file="imgs/correono.png")
#musimg = PhotoImage(file="imgs/musicano.png")

Checkbutton(opciones, text="Escritorio", variable=escritorio, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=0, column=0, sticky='w')
Checkbutton(opciones, text="Documentos", variable=documentos, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=1, column=0, sticky='w')
Checkbutton(opciones, text="Favoritos", variable=favoritos, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=2, column=0, sticky='w')
Checkbutton(opciones, text="Imagenes", variable=imagenes, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=0, column=1, sticky='w')
Checkbutton(opciones, text="Videos", variable=videos, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=1, column=1, sticky='w')
Checkbutton(opciones, text="Mail", variable=mail, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=2, column=1, sticky='w')
Checkbutton(opciones, text="Musica", variable=musica, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas, font=('Arial', 11, 'bold'), activebackground="#7B61E8").grid(row=3, column=0, sticky='w')
opciones.pack(anchor="center")


iniciarimg = PhotoImage(file="imgs/iniciar.png")
iniciar = Button(raiz, text="Comenzar", command=realizarBackup, image=iniciarimg, cursor="hand2")
iniciar.config(borderwidth=0)
iniciar.place(x=220, y=255)

#Ultimo back up
Label(raiz, text="Ultimo Back-up:", bg="#7B61E8", fg="white", width=18, font=('Arial', 10)).place(x=10, y=248)
with open('archivos/ultimo.txt', 'r') as f:
	ultimo = f.read()

ult_bk = Label(raiz)
ult_bk.config(text=ultimo, bg="#7B61E8", fg="white", width=18, font=('Arial', 10))
ult_bk.place(x=10, y=268)





raiz.mainloop()
