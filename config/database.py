import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Indicamos el nombre de la base de datos
sqlite_file_name = "database.sqlite"
# Directorio donde estara la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__))

#nos conectamos a la base de datos, se usa join para unir las url
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
engine = create_engine(database_url, echo=True)

# Se crea la sesion para la base de datos, enlazada con bind.
Session = sessionmaker(bind=engine)

# Sirve para manipular las tablas de la base de datos
Base = declarative_base()