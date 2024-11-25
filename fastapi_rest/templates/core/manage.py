import sys
from fastapi_rest.manage_command import ManageControl

def main():
    command = sys.argv
    return ManageControl(command[1:]).main()

if __name__ == "__main__":
    main()