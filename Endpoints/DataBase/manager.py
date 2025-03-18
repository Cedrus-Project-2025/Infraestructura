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
        self.drive_remote = os.getenv("RCLONE_name", "drive:")
        self.db_filename = "database.db"
        self.db_path = os.path.join(
            self.location_path,
            '__pycache__',
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
            except subprocess.CalledProcessError as e:
                print(f"Error al descargar la base de datos: {e}")

    def __upload_db_to_drive(self) -> None:
        """
        Sube la base de datos a Google Drive después de cada modificación.
        """
        try:
            subprocess.run(["rclone", "copy", self.db_path, self.drive_remote], check=True)
            print("Base de datos subida a Google Drive correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al subir la base de datos: {e}")

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
            """CREATE TABLE IF NOT EXISTS rain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rain_detected BOOLEAN NOT NULL,
                intensity REAL NOT NULL,
                timestamp TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS temperature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                timestamp TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS motion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                motion_detected BOOLEAN NOT NULL,
                timestamp TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS pressure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pressure REAL NOT NULL,
                altitude REAL NOT NULL,
                timestamp TEXT NOT NULL
            )"""
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
    