import json
import requests
from logging import info, error
import yaml
import glob
import os
import hvac

"""
Набор функций для получения информации из файлов/nexus/vault
"""

#Функция для получения информации из nexus

def getDataFromNexus(base_url, username, password, key):
    data_from_nexus = requests.get(url=base_url,auth=(username, password)).text
    print(base_url)
    list_data_from_nexus = []
    for repo in json.loads(data_from_nexus):
        list_data_from_nexus.append(repo[str(key)])
    return list_data_from_nexus

#Функция для получения информации из локальных конфигов yaml
def getDataFromConfigs(path_to_configs_repos):
    configs_files = glob.glob(os.path.join(path_to_configs_repos, "**/*.yaml"), recursive=True)
    configs = []
    for file_path in configs_files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                if config:
                    configs.append(config)
        except Exception as e:
            error(f"🚨 Ошибка при загрузке {file_path}: {e}")
    return configs

#Функция по получению секретов из vault
def getSecretFromVault(vault_base_url,vault_token,vault_path_secret,mount_point, secret_user):
    client = hvac.Client(url=vault_base_url, token=vault_token)
    secret = client.secrets.kv.v1.read_secret(
        mount_point=mount_point,
        path=vault_path_secret
    )
    secret_data = secret["data"]
    return secret_data[secret_user]