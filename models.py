import db  # importamos el contenido de db.py para que podamos acceder a el
from sqlalchemy import Column, Integer, String, Boolean, Date

''' Creamos una clase llamada Tarea
Esta clase va a ser nuestro modelo de datos de la tarea (el cual nos servirá luego para la base de datos)
Esta clase va a almacenar toda la información referente a una tarea '''


class Tarea(db.Base):
    __tablename__ = "tarea"
    id = Column(Integer, primary_key=True)  # Identificador único de cada tarea
    # (no puede haber dos tareas con el mismo id, por eso es primary key)
    contenido = Column(String(200), nullable=False)  # Contenido de la tarea, un texto de máximo 200 caracteres
    hecha = Column(Boolean)  # Booleano que indica si una tarea ha sido hecha o no
    categoria = Column(String(50))  # El usuario indicará a que categoria esta la tarea
    fecha_limite = Column(Date)  # Fecha limite de una tarea
    check_date = Column(Boolean)  # Indica si la fecha limite ha expirado o no

    def __init__(self, contenido, hecha, categoria, fecha_limite, check_date):
        # Recordemos que el id no es necesario crearlo manualmente, lo añade la base de datos automaticamente
        self.contenido = contenido
        self.hecha = hecha
        self.categoria = categoria
        self.fecha_limite = fecha_limite
        self.check_date = check_date

    def repr(self):  # ? Copia de __str__
        return "Tarea {}: {} ({})".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha_limite,
                                          self.check_date)

    def __str__(self):
        return "Tarea {}: {} ({})".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha_limite,
                                          self.check_date)
