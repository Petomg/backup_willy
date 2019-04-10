# Se incia cada vez que levanta windows TODO

import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from subprocess import call
import ast
from tkinter import messagebox
from time import sleep
import os

rutasBk = {}
respuesta = False

def backupAutomatico():
	global respuesta
	global rutasBk
	panel = Tk()
	panel.resizable(False, False)
	panel.iconbitmap("imgs/icono.ico")
	panel.title("Back-up en progreso")
	panel.overrideredirect(True)
	panel.geometry("300x85+500+300")
	panel.config(bg="#979AE8")

	Label(panel, text="Realizando Back-up...", font=12, bg="#979AE8").pack(pady=10)
	barra = ttk.Progressbar(panel, length=200, mode='determinate')
	barra.pack(pady=10)
	panel.update_idletasks()
	barra['value'] = 0
	error = False
	for categoria in rutasBk:
		logpath = os.path.abspath("logs/{}.txt".format(categoria))
		call(["robocopy", rutasBk[categoria][0] ,  rutasBk[categoria][1] , "/S", "/COPY:DAT", "/MIR", "/R:1", "/W:3", "/log:{}".format(logpath)], shell=True)
		barra['value'] += (200 / len(rutasBk))
		panel.update_idletasks()

		with open(logpath, 'r') as f:
			texto = f.read()
			if "ERROR 2" in texto or "ERROR 3" in texto:
				error = True

	if error:
		messagebox.showerror("Error", "Ocurrió un error durante el Back-up. Por favor reintente más tarde")
	else:	
		with open('archivos/ultimo.txt', 'w') as f:
			f.write(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

	panel.destroy()

	if respuesta:
		os.system("shutdown /s /t 1")
	else:
		if not error:
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
	respuesta2 = messagebox.askokcancel("Backup", "Se recomienda hacer Back-up. Desea realizarlo ahora?")
	if respuesta2:
		respuesta = messagebox.askokcancel("Back-up", "¿Desea apagar el equipo al finalizar?")
		backupAutomatico()
	
	raiz.destroy()

	raiz.mainloop()	

elif diferencia.days >= 60:
	raiz = Tk()
	raiz.geometry("300x50+500+300")
	raiz.overrideredirect(True)
	raiz.iconbitmap("imgs/icono.ico")
	raiz.title("Back-up en progreso")
	raiz.resizable(False, False)
	raiz.config(bg="#979AE8")
	mssg = Label(raiz, font=12, bg="#979AE8")
	mssg.pack(pady=10)
	raiz.update_idletasks()
	raiz.config(bg="#979AE8")
	for i in list(reversed(list(range(5)))):
		texto = "El Back-up se iniciara en {} segundos".format((i+1))
		mssg.config(text = texto)
		raiz.update_idletasks()	
		sleep(1)
	raiz.withdraw()
	backupAutomatico()		
	raiz.destroy()
	raiz.mainloop()	
		
