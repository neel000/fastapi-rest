import os
import shutil
from fastapi_rest.console import Console

class ManageControl:
    def __init__(self, command:list=[]):
        self.command = command
        self.system = os.system

    def help(self):
        for i in self.mapper().keys():
            Console.info(f"python manage.py {i} \n")
        
    
    def copy_file(self, app_dir):
        os.makedirs(app_dir)

        dir = os.path.join(os.path.dirname(__file__), 'templates/app')

        if not os.path.exists(dir):
            return Console.error(f"Error: directory '{dir}' not found.")

        for item in os.listdir(dir):
            source = os.path.join(dir, item)
            if app_dir:
                destination = os.path.join(app_dir, item)
            else:
                destination = item

            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
                
        Console.success(f"Common files and directories copied to {app_dir}.")

    def create_app(self):
        if len(self.command)!=2:
            return Console.error("Invalid Command!")
        app_name = self.command[1]

        if os.path.exists(app_name):
            return Console.error(
                f"Error: The directory '{app_name}' already exists."
            )
        
        return self.copy_file(app_name)
        
    def make_migrations(self):
        return self.system('alembic revision --autogenerate -m "Initial migration"')

    def migrate(self):
        return self.system('alembic upgrade head')

    def run_server(self):
        port = f"--port {self.command[1]}" if 1 < len(self.command) else ""
        cmd = f"uvicorn main:app --reload {port}"
        return self.system(cmd)

    def mapper(self):
        data = {
            "startapp":self.create_app,
            "makemigrations":self.make_migrations,
            "migrate":self.migrate,
            "runserver":self.run_server
        }
        return data

    def main(self):
        if not self.command or self.command[0] == "help":
            return self.help()
        
        mapper = self.mapper()
        arg = self.command[0]

        if arg in mapper.keys():
            return mapper[arg]()
        
        return Console.error("Command is not valid!")