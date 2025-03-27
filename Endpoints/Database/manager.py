import sqlite3
import os, sys
import subprocess
from typing import List, Tuple, Any

class DatabaseManager:
    def __init__(self) -> None:
        """
        Inicializa la conexión con la base de datos y verifica la existencia de las tablas.
        """

        self.location_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.drive_remote = os.getenv("RCLONE_name")
        self.db_filename = "database.db"
        self.db_path = os.path.join(
            self.location_path,
            'Files',
            'Temp',
            self.db_filename
        )

        self.__download_db()
        self.__create_tables()

    # =============== MÉTODOS PRIVADOS ===============
    def __download_db(self) -> None:
        """
        Descarga la base de datos desde Google Drive si no existe localmente.
        """
        if not os.path.exists(self.db_path):
            print("Descargando la base de datos desde Google Drive...")
            try:
                subprocess.run(["rclone", "copy", f"{self.drive_remote}/{self.db_filename}", "./"], check=True)
                print("Base de datos descargada correctamente.")
            except Exception as e:
                print(f"No se pudo conectar con Rclone por: {e}.\nGenerando localmente...")
                with open(self.db_path,'w'): pass

    def __upload_db_to_drive(self) -> None:
        """
        Sube la base de datos a Google Drive después de cada modificación.
        """
        try:
            subprocess.run(["rclone", "copy", self.db_path, self.drive_remote], check=True)
            print("Base de datos subida a Google Drive correctamente.")
        except Exception as e:
            print(f"Error al subir la base de datos con Rclone, Saltando proceso: {e}")

    def __connect(self) -> sqlite3.Connection:
        """
        Crea y devuelve una conexión a la base de datos.
        """
        try:
            return sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def __create_tables(self) -> None:
        """
        Crea las tablas necesarias si no existen en la base de datos.
        """
        queries = [
            """CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );""",
            """CREATE TABLE IF NOT EXISTS chatbot_interacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                pregunta TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );""",
            """CREATE TABLE IF NOT EXISTS configuraciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clave TEXT UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                descripcion TEXT
            );"""
        ]

        conn = self.__connect()
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
        conn.close()


    # =============== MÉTODOS PUBLICOS ===============
    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE) y sube la BD a Google Drive.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        self.__upload_db_to_drive()

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        """
        Ejecuta una consulta SELECT y devuelve todos los resultados.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    