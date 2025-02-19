import json
import requests
from logging import info, error

########################
#Импорт локальных функций
from src.getData import getReposFromConfigs, getSecretFromVault
########################

'''
Класс по созданию репозиториев в nexus
'''

class CreateRepo:
    def __init__(self, base_url = "", path_to_configs_repos="", list_repos_from_nexus = "", template = "",username="", password="", headers="", blob_storage="", vault_base_url="", vault_token="", vault_path_secret=""):
        self.path_to_configs_repos = path_to_configs_repos
        self.base_url = base_url
        self.list_repos_from_nexus = list_repos_from_nexus
        self.template = template
        self.username = username
        self.password = password
        self.headers = headers
        self.blob_storage = blob_storage
        self.vault_base_url = vault_base_url
        self.vault_token = vault_token
        self.vault_path_secret = vault_path_secret

    #Метод для генерации url запроса
    def request_url(self, configs ,id, type):
        nexus_url = self.base_url + "/v1/repositories/" + id + "/" + type
        return nexus_url

    #Метод на удаление групп/репозиториев
    def delete_repos(self):
        local_repos = []
        #Прохождение циклом по конфигам и получение имен репозиториев
        for repo in getReposFromConfigs(path_to_configs_repos=self.path_to_configs_repos):
            for i in repo['repos']:
                local_repos.append(i['repo'])

        #Сравнение мап с репами из нексуса и локальных конфигов для получения репозитория которого нет в конфиге для последющего удаления
        repos_to_delete = list(set(self.list_repos_from_nexus).difference(local_repos))

        for repo in repos_to_delete:
            delete_repo_url =  self.base_url+repo
            response = requests.delete(url=delete_repo_url, auth=(self.username, self.password), headers=self.headers)
            if response.status_code == 204:
                info(f"✅ репозиторий: {repo} удален!")
            else:
                error(f"🚨 Ошибка: {response.status_code}, {response.reason}, {response.url}, {response.json()}, {response.text}")

    #Метод на запрос на создание и обновлении информации о группах/прокси-репозиториев
    def make_update_repos(self, data, repoName, url):
        dump_data = json.loads(self.template.render(data))
        url_with_repo_name = url + "/" + repoName
        #Запросы в nexus
        if repoName in self.list_repos_from_nexus:
            #Запрос на обновление репозиториев в nexus
            response = requests.put(url=url_with_repo_name, auth=(self.username, self.password), json=dump_data, headers=self.headers)
            if response.status_code == 204:
                info(f"✅ репозиторий: {repoName} успешно обновлен!")
            else:
                error(f"🚨 Ошибка: {response.status_code}, {response.reason}, {response.url}, {response.json()}, {response.text}")
        else:
            #Запрос на создание репозиториев в nexus
            response = requests.post(url=url, auth=(self.username, self.password), json=dump_data, headers=self.headers)
            if response.status_code == 201:
                info(f"✅ репозиторий: {repoName} успешно создан!")
            else:
                error(f"🚨 Ошибка: {response.status_code}, {response.reason}, {response.url}, {response.json()}, {response.text}")

    #Метод по рендеру информации для создания запроса на создание прокси-репозиториев
    def ProxyRepo(self):
        configs = getReposFromConfigs(path_to_configs_repos=self.path_to_configs_repos)
        for params in configs:
            if params["type"] == "proxy" :
                for repo in params["repos"]:
                    #Рендер конфига для запроса
                    data = {
                        "repo_name": repo["repo"],
                        "proxy_remote_url": repo["remote_url"],
                        "blob_storage": self.blob_storage,
                        "username": repo["username"],
                        "password": getSecretFromVault(vault_base_url=self.vault_base_url,vault_token=self.vault_token,vault_path_secret=self.vault_path_secret,mount_point=params["ris"], secret_user=repo["username"]),
                        "id": params["id"]
                    }

                    self.make_update_repos(
                        data=data,
                        repoName=repo["repo"],
                        url=self.request_url(configs=getReposFromConfigs(path_to_configs_repos=self.path_to_configs_repos), id=params["id"], type=params["type"])
                    )
    #Метод по рендеру информации для создания запроса на создание групп
    def GroupRepo(self):
        configs = getReposFromConfigs(path_to_configs_repos=self.path_to_configs_repos)
        for params in configs:
            if params["type"] == "group" :
                for repo in params["repos"]:
                    settings = repo["members"]
                    #Рендер конфига для запроса
                    data = {
                        "repo_name": repo["repo"],
                        "blob_storage": self.blob_storage,
                        "member_repo": json.dumps(settings)
                    }
                    self.make_update_repos(
                        data=data,
                        repoName=repo["repo"],
                        url=self.request_url(
                            configs=getReposFromConfigs(path_to_configs_repos=self.path_to_configs_repos),
                            id=params["id"], type=params["type"])
                    )