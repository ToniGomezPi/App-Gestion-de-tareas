from flask import Flask, render_template, request, redirect, url_for
import db  # podremos acceder a las variables y parametros de la database
from models import Tarea
from datetime import datetime

# Tendremos acceso a la clase Tarea pero no podremos crear (db.Base.metadata.create_all(db.engine))

app = Flask(__name__)  # En app se encuentra nuestro servidor web de Flask


# La barra (el slash) se conoce como la página de inicio (página home).
# Vamos a definir para esta ruta, el comportamiento a seguir.


@app.route('/')
def home():
    todas_las_tareas = db.session.query(Tarea).all()  # Consultamos y almacenamos todas las tareas de la base de datos
    for tarea in todas_las_tareas:  # Comprueba en el listado de tareas si hay alguna expirada
        expirada(tarea.id)
    # Ahora en la variable todas_las_tareas se tienen almacenadas todas las tareas.
    # Vamos a entregar esta variable al template index.html
    return render_template("index.html", lista_de_tareas=todas_las_tareas)  # Se carga el template index.html


@app.route('/crear-tarea', methods=['POST'])
def crear():
    fecha = request.form['fecha_limite']
    fecha = datetime.strptime(fecha, "%Y-%m-%d")
    # tarea es un objeto de la clase Tarea (una instancia de la clase)
    tarea = Tarea(contenido=request.form['contenido_tarea'], hecha=False, categoria=request.form['categoria_tarea'],
                  fecha_limite=fecha, check_date=False)  # id no es necesario asignarlo manualmente,
    # porque la primary key se genera automaticamente

    db.session.add(tarea)  # Añadir el objeto de Tarea a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('home'))  # Esto nos redirecciona a la función home()


@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).delete()
    # Se busca dentro de la base de datos, aquel registro cuyo id coincida con el aportado por el parametro de la ruta.
    # Cuando se encuentra se elimina
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('home'))
    # Esto nos redirecciona a la función home() y si ha ido bien, al refrescar, la tarea eliminada ya no
    #  aparecera en el listado



@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()  # Se obtiene la tarea que se busca
    tarea.hecha = not (tarea.hecha)  # Guardamos en la variable booleana de la tarea, su contrario
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('home'))  # Esto nos redirecciona a la función home()


def expirada(id):  # funcion que comprobará nuestro HOME y ver si alguna fecha ha superado la fecha limite
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    todayDate = datetime.now()  # Fecha del sistema
    todayDate = int(todayDate.strftime("%Y%m%d"))  # convertimos las dos fechas a integers para compararlos
    fechaLimit = int(tarea.fecha_limite.strftime("%Y%m%d"))
    if fechaLimit < todayDate and tarea.check_date == False:  # si la fecha de hoy es mas grande que la fecha que escribio el
        # usuario quiere decir ya ha expirado la tarea
        tarea.check_date = not (tarea.check_date)
    db.session.commit()


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)  # Creamos el modelo de datos ( models )
    app.run(debug=True)  # El debug=True hace que cada vez que reiniciemos
    # el servidor o modifiquemos codigo, el servidor de Flask se reinicie solo
