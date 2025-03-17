from os import environ
#функция по нахождению енва, если его нет, то переменные окружения будут браться из конфигов yaml
def getEnvs():
    if not "RUN_IN_K8S" in environ:
        from dotenv import load_dotenv
        load_dotenv()
