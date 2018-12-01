# Se incia cada vez que levanta windows TODO

import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from subprocess import call
import ast
from tkinter import messagebox
import os

rutasBk = {}


def backupAutomatico():
	respuesta = messagebox.askokcancel("Back-up", "¿Desea apagar el equipo al finalizar?")

	global rutasBk
	panel = Tk()
	panel.resizable(False, False)
	panel.iconbitmap("imgs/icono.ico")
	panel.title("Back-up en progreso")
	panel.geometry("300x50")
	panel.config(bg="#979AE8")

	barra = ttk.Progressbar(panel, length=200, mode='determinate')
	barra.pack(pady=15)
	panel.update_idletasks()
	barra['value'] = 0
	for categoria in rutasBk:
		call(["robocopy", rutasBk[categoria][0] ,  rutasBk[categoria][1] , "/S"])
		barra['value'] += (200 / len(rutasBk))
		panel.update_idletasks()

	with open('archivos/ultimo.txt', 'w') as f:
		f.write(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

	panel.destroy()

	if respuesta:
		os.system("shutdown /s /t 1")
	else:
		messagebox.showinfo("Back-up", "Back-up finalizado.")	
	


actual = datetime.datetime.now() # Se actualiza con la fecha actual cada vez que es ejecutado

with open('archivos/ultimo.txt', 'r') as f:
	ult_bkup = f.read()

ult_bkup = datetime.datetime.strptime(ult_bkup, '%d/%m/%Y %H:%M:%S')

diferencia = actual - ult_bkup  # devuelve deltatime


with open('archivos/rutas_dict.txt') as f:
	rutasBk = ast.literal_eval(f.read())


if diferencia.days > 30 and diferencia.days < 60:
	raiz = Tk()
	raiz.iconbitmap("imgs/icono.ico")
	raiz.withdraw()
	respuesta = messagebox.askokcancel("Backup", "Se recomienda hacer Back-up. Desea realizarlo ahora?")
	if respuesta:
		backupAutomatico()
	raiz.destroy()
	raiz.mainloop()	

elif diferencia.days >= 60:
	raiz = Tk()
	raiz.iconbitmap("imgs/icono.ico")
	raiz.withdraw()
	backupAutomatico()		
	raiz.destroy()
	raiz.mainloop()	
		
