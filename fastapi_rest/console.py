RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

class Console:
    @staticmethod
    def log(data, *args, **kwargs):
        output = "{}{}{}".format(YELLOW, data, RESET)
        print(output, *args, **kwargs)

    @staticmethod
    def info(data, *args, **kwargs):
        output = "{}{}{}".format(BLUE, data, RESET)
        print(output, *args, **kwargs)
    
    @staticmethod
    def error(data, *args, **kwargs):
        output = "{}{}{}".format(RED, data, RESET)
        print(output, *args, **kwargs)

    @staticmethod
    def success(data, *args, **kwargs):
        output = "{}{}{}".format(GREEN, data, RESET)
        print(output, *args, **kwargs)