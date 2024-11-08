import argparse
import os
import shutil
import sys

class BaseCommand:

    def help(self):
        print("fastapi-rest startproject <project_name>\n")
        print("fastapi-rest createapp <project_name>")
        return 
    
    def no_app_name(self):
        print("APP Name is not found")

    def create_app(self, app_name:str):
        app_name = app_name if not app_name == "." else ""
      
        if app_name:
            if os.path.exists(app_name):
                return print(f"Error: The directory '{app_name}' already exists.")
            
            os.makedirs(app_name)

        return self.copy_common_files(app_name)

        
    
    def main(self):
        command = sys.argv
        length_command = len(command)

        if length_command == 1 or command[1] == "help":
            return self.help()
        elif command[1] in ["startproject", "createapp"]:
            if not length_command > 2:
                return self.no_app_name()
            return self.create_app(command[2])

        return print(f"Command is not found!")

    def copy_common_files(self, app_dir):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if not os.path.exists(template_dir):
            print(f"Error: Template directory '{template_dir}' not found.")
            return

        for item in os.listdir(template_dir):
            source = os.path.join(template_dir, item)
            if app_dir:
                destination = os.path.join(app_dir, item)
            else:
                destination = item

            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
                
        print(f"Common files and directories copied to {app_dir}.")


    
def main():
    return BaseCommand().main()

if __name__ == "__main__":
    main()
