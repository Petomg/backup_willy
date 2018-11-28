# Se incia cada vez que levanta windows TODO

import datetime

actual = datetime.datetime.now() # Se actualiza con la fecha actual cada vez que es ejecutado

# actual.strftime('%Y-%m-%d %H:%M:%S') Es lo que se guarda en el archivo luego de hacer el bkup
# ult_bkup rescata de los registros el string del date
# ult_bkup = datetime.datetime.strptime(ult_bkup, '%Y-%m-%d %H:%M:%S')
# diferencia = actual - ult_bkup  ----> devuelve deltatime
# Lo que tengo que evaluar es diferncia.days