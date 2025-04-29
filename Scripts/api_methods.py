import os, json, requests, platform
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

class API_Methods:
    # =============== CONSTRUCTOR ===============
    def __init__(self,location_path:str = os.path.dirname(os.path.abspath(__file__)),url:str = None):
        '''
        Inicializa una clase para interactuar con una API, proporcionando métodos para enviar solicitudes GET y POST.

        ### Args:
        * `location_path` (str, opcional): Espera la ruta del directorio en el cual se almacenarán los registros de errores.
        * `url` (str, opcional): La URL base de la API con la que interactuar. Por defecto es None.

        ### Atributos:
        * `location_path` (str): La ruta en la que se almacenarán los registros de errores.
        * `url` (str): La URL base de la API.

        ### Métodos:
        * `POST`: Envía una solicitud POST al endpoint especificado de la API con los datos proporcionados.
        * `GET`: Envía una solicitud GET al endpoint especificado de la API y devuelve el código de respuesta y los datos.
        
        ### Notas:
        * Todos los errores encontrados durante las interacciones con la API se registran en `location_path/Files/Errors/API.json`.
        * Si no se proporciona el argumento `url` durante la inicialización, debe especificarse en cada llamada `POST` o `GET`.
        '''

        self.location_path = location_path
        self.url = url if (str(url)[-1] == '/') else (f"{url}/" if url != None else url)

    # =============== METHODS ===============
    def POST(self,endpoint:str = None,data:dict = {}, headers:dict = {"Content-Type": "application/json; charset=utf-8"}):
        '''
        Envía una solicitud POST a un endpoint de la API.

        ### Args:
        * `endpoint` (str, opcional): El endpoint específico al cual enviar la solicitud. Por defecto es None.
        * `data` (dict, opcional): Los datos que se enviarán en el cuerpo de la solicitud. Por defecto es un diccionario vacío.
        * `headers` (dict, opcional): Los encabezados que se enviarán con la solicitud. Por defecto es `{"Content-Type": "application/json; charset=utf-8"}`.

        ### Devuelve:
        * tuple: Una tupla que contiene:
            * `requests.Response`: El objeto de respuesta de la llamada a la API.
            * dict: Los datos de respuesta JSON analizados (si tiene éxito).

        ### Excepciones:
        * Todos los errores encontrados durante las interacciones con la API se registran en `self.location_path/Files/Errors/API.json`.
        
        ### Notas:
        * Si `self.url` no se proporciona durante la inicialización, debe especificarse en cada llamada `POST`.
        '''
        if self.url and not(endpoint): endpoint = self.url
        elif not(self.url) and not(endpoint): raise AttributeError("Neither base URL nor endpoint given")
        elif self.url and endpoint: endpoint = f"{self.url}{endpoint[1:] if endpoint[0] == '/' else endpoint}"

        try:
            res = requests.post(endpoint, data=json.dumps(data), headers=headers)
            res.raise_for_status()
            nuevo = res.json()
            return res, nuevo
        except Exception as ex:
            os.makedirs(os.path.join(self.location_path,'Files','Errors'),exist_ok=True)
            errors_file_path = os.path.join(self.location_path,'Files','Errors','API.json')
            if os.path.exists(errors_file_path):
                file = json.loads(open(errors_file_path,'r').read())
                file.append({
                    "Datetime"          : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Method"            : "POST",
                    "Exception"         : str(ex),
                    "Data to be Posted" : data
                })
                json.dump(file,open(errors_file_path,'w'))
            else:
                file = open(errors_file_path,'w')
                json.dump([{
                    "Datetime"          : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Method"            : "POST",
                    "Exception"         : str(ex),
                    "Data to be Posted" : data
                }],file)
                file.close()
            
            return "Failure to post", ex

    def GET(self,endpoint:str = None, data:dict = {}, headers:dict = {"Content-Type": "application/json; charset=utf-8"}):
        '''
        Envía una solicitud GET a un endpoint de la API.

        ### Args:
        * `endpoint` (str): URL del endpoint de la API para obtener datos.

        ### Devuelve:
            * `Response code` (str | Literal['Failure to get data']):
                * En caso de éxito, el código de estado HTTP de la respuesta.
                * En caso de fallo, la cadena literal "Failure to get data".
            * `Data` (list[dict] | Exception):
                * En caso de éxito, una lista de diccionarios con información.
                * En caso de fallo, el objeto de excepción planteada.
        '''        
        if self.url and not(endpoint): endpoint = self.url
        elif not(self.url) and not(endpoint): raise AttributeError("Neither base URL nor endpoint given")
        elif self.url and endpoint: endpoint = f"{self.url}{endpoint[1:] if endpoint[0] == '/' else endpoint}"

        try:
            res = requests.get(endpoint, headers=headers, data=json.dumps(data))
            res.raise_for_status()
            dicts = res.json()
            return res, dicts
        except Exception as ex:
            return "Failure to get data", ex

    def PATCH(self,endpoint:str = None, data:dict = {}, headers:dict = {"Content-Type": "application/json; charset=utf-8"}):
        '''
        Envía una solicitud PATCH a un endpoint de la API.

        ### Args:
        * `endpoint` (str, opcional): El endpoint específico al cual enviar la solicitud. Por defecto es None.
        * `data` (dict, opcional): Los datos que se enviarán en el cuerpo de la solicitud. Por defecto es un diccionario vacío.
        * `headers` (dict, opcional): Los encabezados que se enviarán con la solicitud. Por defecto es `{"Content-Type": "application/json; charset=utf-8"}`.

        ### Devuelve:
        * tuple: Una tupla que contiene:
            * `requests.Response`: El objeto de respuesta de la llamada a la API.
            * dict: Los datos de respuesta JSON analizados (si tiene éxito).

        ### Excepciones:
        * Todos los errores encontrados durante las interacciones con la API se registran en `self.location_path/Files/Errors/API.json`.
        '''
        if self.url and not(endpoint): endpoint = self.url
        elif not(self.url) and not(endpoint): raise AttributeError("Neither base URL nor endpoint given")
        elif self.url and endpoint: endpoint = f"{self.url}{endpoint[1:] if endpoint[0] == '/' else endpoint}"

        try:
            res = requests.patch(endpoint, data=json.dumps(data), headers=headers)
            res.raise_for_status()
            nuevo = res.json()
            return res, nuevo
        except Exception as ex:
            os.makedirs(os.path.join(self.location_path,'Files','Errors'),exist_ok=True)
            errors_file_path = os.path.join(self.location_path,'Files','Errors','API.json')
            if os.path.exists(errors_file_path):
                file = json.loads(open(errors_file_path,'r').read())
                file.append({
                    "Datetime"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Method"    : "PATCH",
                    "Exception" : str(ex),
                    "Data Sent" : data
                })
                json.dump(file,open(errors_file_path,'w'))
            else:
                with open(errors_file_path,'w') as file:
                    json.dump([{ 
                        "Datetime"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Method"    : "PATCH",
                        "Exception" : str(ex),
                        "Data Sent" : data
                    }],file)

            return "Failure to patch", ex

    def PUT(self,endpoint:str = None, data:dict = {}, headers:dict = {"Content-Type": "application/json; charset=utf-8"}):
        '''
        Envía una solicitud PUT a un endpoint de la API.

        ### Args:
        * `endpoint` (str, opcional): El endpoint específico al cual enviar la solicitud. Por defecto es None.
        * `data` (dict, opcional): Los datos que se enviarán en el cuerpo de la solicitud. Por defecto es un diccionario vacío.
        * `headers` (dict, opcional): Los encabezados que se enviarán con la solicitud. Por defecto es `{"Content-Type": "application/json; charset=utf-8"}`.

        ### Devuelve:
        * tuple: Una tupla que contiene:
            * `requests.Response`: El objeto de respuesta de la llamada a la API.
            * dict: Los datos de respuesta JSON analizados (si tiene éxito).

        ### Excepciones:
        * Todos los errores encontrados durante las interacciones con la API se registran en `self.location_path/Files/Errors/API.json`.
        '''
        if self.url and not(endpoint): endpoint = self.url
        elif not(self.url) and not(endpoint): raise AttributeError("Neither base URL nor endpoint given")
        elif self.url and endpoint: endpoint = f"{self.url}{endpoint[1:] if endpoint[0] == '/' else endpoint}"

        try:
            res = requests.put(endpoint, data=json.dumps(data), headers=headers)
            res.raise_for_status()
            nuevo = res.json()
            return res, nuevo
        except Exception as ex:
            os.makedirs(os.path.join(self.location_path,'Files','Errors'),exist_ok=True)
            errors_file_path = os.path.join(self.location_path,'Files','Errors','API.json')
            if os.path.exists(errors_file_path):
                file = json.loads(open(errors_file_path,'r').read())
                file.append({
                    "Datetime"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Method"    : "PUT",
                    "Exception" : str(ex),
                    "Data Sent" : data
                })
                json.dump(file,open(errors_file_path,'w'))
            else:
                with open(errors_file_path,'w') as file:
                    json.dump([{ 
                        "Datetime"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Method"    : "PUT",
                        "Exception" : str(ex),
                        "Data Sent" : data
                    }],file)

            return "Failure to put", ex

    def DELETE(
        self,
        endpoint: str = None,
        data: dict = {},   # ← ahora acepta cuerpo JSON
        headers: dict = {"Content-Type": "application/json; charset=utf-8"}
    ):
        """
        Envía una solicitud DELETE a un endpoint de la API.

        Args:
            endpoint (str, opcional): Ruta relativa o absoluta del endpoint.
            data     (dict, opcional): Cuerpo JSON que se enviará.
            headers  (dict, opcional): Encabezados HTTP.

        Returns:
            tuple:
                - requests.Response | str : Objeto Response o "Failure to delete"
                - dict | Exception        : JSON de respuesta o excepción
        """
        if self.url and not endpoint:
            endpoint = self.url
        elif not self.url and not endpoint:
            raise AttributeError("Neither base URL nor endpoint given")
        elif self.url and endpoint:
            endpoint = f"{self.url}{endpoint[1:] if endpoint[0] == '/' else endpoint}"

        try:
            res = requests.delete(
                endpoint,
                data=json.dumps(data),   
                headers=headers
            )
            res.raise_for_status()
            return res, res.json()

        except Exception as ex:
            # --- registrar error ---
            os.makedirs(os.path.join(self.location_path, 'Files', 'Errors'), exist_ok=True)
            err_file = os.path.join(self.location_path, 'Files', 'Errors', 'API.json')
            registro = {
                "Datetime":  datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Method":    "DELETE",
                "Exception": str(ex),
                "Data Sent": data
            }
            if os.path.exists(err_file):
                historico = json.loads(open(err_file, 'r').read())
                historico.append(registro)
            else:
                historico = [registro]
            json.dump(historico, open(err_file, 'w'))

            return "Failure to delete", ex




if __name__ == '__main__':
    os.system('clear') if platform.system() == 'Linux' else os.system('cls')

    
    test = API_Methods(
        location_path = os.getcwd(),
        url           = os.getenv('API')
    )

    result = test.GET(
        endpoint = '/customerc1'
    )
    
    print(result)