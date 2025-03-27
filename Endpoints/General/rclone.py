import os

def validar_rclone():
    ''' 
    '''
    file_path = os.path.join(os.getenv("HOME",os.path.dirname(__file__)),'.config','rclone','rclone.conf')
    if not(os.path.isfile(file_path)):
        os.makedirs(
            os.path.dirname(file_path),
            exist_ok = True
        )
        
        print(f"'rclone.conf' file does NOT exist...")
        name  = os.getenv('RCLONE_name')
        tipo  = os.getenv('RCLONE_type')
        scope = os.getenv('RCLONE_scope')
        token = os.getenv('RCLONE_token')

        file_content = f"[{name}]\n"
        file_content += f"type = {tipo}\n"
        file_content += f"scope = {scope}\n"
        file_content += f"token = {token}\n"
        file_content += f"team_drive = \n"

        with open(file_path,'w') as file: file.write(file_content)

        print(f"Archivos: {os.listdir(os.path.dirname(file_path))}")