from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from subprocess import call
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
	popup.geometry("300x100")
	popup.resizable(False, False)
	popup.iconbitmap("imgs/icono.ico")
	popup.title("Contraseña Requerida")
	popup.config(bg="#979AE8")

	contra = Entry(popup, show='*')
	contra.pack(pady = 10)

	def panelAdmin():
		if contra.get() != 'peto':
			popup.destroy()
			messagebox.showwarning("Advertencia", "La contraseña ingresada no es correcta")
		else:
			popup.destroy()
			panel = Toplevel()
			panel.resizable(True, True)
			panel.iconbitmap("imgs/icono.ico")
			panel.title("Panel de Administrador")
			panel.geometry("700x250")
			panel.config(bg="#979AE8")

			tkvar = StringVar()
			opciones = {'Escritorio', 'Documentos', 'Favoritos', 'Imagenes', 'Descargas', 'Mail'}
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
				file = open('archivos/rutas_dict.txt', 'w')
				nuevo_origen = filedialog.askdirectory()
				rutas[tkvar.get().lower()][0] = nuevo_origen
				file.write(str(rutas))
				file.close()
				change_dropdown()
				panel.deiconify()

			def cambiarDestino():
				file = open('archivos/rutas_dict.txt', 'w')
				nuevo_destino = filedialog.askdirectory()
				rutas[tkvar.get().lower()][1] = nuevo_destino
				file.write(str(rutas))
				file.close()
				change_dropdown()
				panel.deiconify()	

			frame = Frame(panel, bg="#979AE8")
			Label(frame, text="Origen: ", bg="#979AE8").grid(row=0, column=0, padx=5)
			Label(frame, text="Destino: ",bg="#979AE8").grid(row=1, column=0, padx=5, pady=10)
			origenlabel = Label(frame, bg="#979AE8")
			origenlabel.grid(row=0, column=1, padx=5)
			destinolabel = Label(frame, bg="#979AE8")
			destinolabel.grid(row=1, column=1, padx=5, pady=10)
			Button(frame, text="Cambiar", command=cambiarOrigen).grid(row=0, column=2, padx=5)
			Button(frame, text="Cambiar", command=cambiarDestino).grid(row=1, column=2, padx=5, pady=10)
			frame.pack(pady=20, expand=True)




	Button(popup, text='Enviar', command=panelAdmin).pack(pady = 15)


# Armo el Header
header=Frame()
header.config(bg="#979AE8", pady=10)
Label(header, text="Applicación Back-up", font=20, bg="#979AE8", padx=10).pack(side="left", anchor="n")
configuracionimg = PhotoImage(file="imgs/conf.png")
Button(header, image=configuracionimg, bg="#979AE8", command=solicitarContra).pack(side="right", anchor="n") # TODO: Pedir contraseña panel de admin
header.pack(fill='x', anchor='n')


#Armo el cuadro de opciones
escritorio = IntVar()
documentos = IntVar()
favoritos = IntVar()
descargas = IntVar()
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
	if descargas.get() == 1:
		rutasBk['descargas'] = rutas['descargas']
	if mail.get() == 1:
		rutasBk['mail'] = rutas['mail'] 

	f.close()

	


def realizarBackup():

	respuesta = messagebox.askokcancel("Back-up", "¿Desea apagar el equipo al finalizar?")
	raiz.withdraw()
	global rutasBk
	panel = Toplevel()
	panel.resizable(False, False)
	panel.iconbitmap("imgs/icono.ico")
	panel.title("Back-up en progreso")
	panel.geometry("300x50")
	panel.config(bg="#979AE8")

	barra = ttk.Progressbar(panel, length=200, mode='determinate')
	barra.pack(pady=15)
	raiz.update_idletasks()
	barra['value'] = 0
	for categoria in rutasBk:
		call(["robocopy", rutasBk[categoria][0] ,  rutasBk[categoria][1] , "/S"])
		barra['value'] += (200 / len(rutasBk))
		raiz.update_idletasks()

	with open('archivos/ultimo.txt', 'w') as f:
		f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	panel.destroy()

	if respuesta:
		raiz.destroy()
		os.system("shutdown /s /t 1")
	else:
		messagebox.showinfo("Back-up", "Back-up finalizado.")
		raiz.deiconify()	


	

opciones = Frame()
opciones.config(bg = "#979AE8", pady=50)
Checkbutton(opciones, text="Escritorio", variable=escritorio, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas).grid(row=0, column=0, sticky='w')
Checkbutton(opciones, text="Documentos", variable=documentos, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas).grid(row=1, column=0, sticky='w')
Checkbutton(opciones, text="Favoritos", variable=favoritos, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas).grid(row=2, column=0, sticky='w')
Checkbutton(opciones, text="Imagenes", variable=imagenes, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas).grid(row=0, column=1, sticky='w')
Checkbutton(opciones, text="Descargas", variable=descargas, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas).grid(row=1, column=1, sticky='w')
Checkbutton(opciones, text="Mail", variable=mail, onvalue=1, offvalue=0, bg = "#979AE8", command=obtenerRutas).grid(row=2, column=1, sticky='w')
opciones.pack(anchor="center")

Button(raiz, text="Comenzar", command=realizarBackup).pack()


print(rutasBk)







raiz.mainloop()
