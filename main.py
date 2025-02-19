import jinja2
import os
import logging
import sys
########################

from src.getEnv import getEnvs
from src.manageRepos import CreateRepo
from src.getData import getReposFromNexus

'''
Определение переменных окружения
'''
########################
getEnvs()

base_url = os.environ['NEXUS_BASE_URL']
username = os.environ['NEXUS_USERNAME']
password = os.environ['NEXUS_PASSWORD']
path_to_configs_repos = os.environ['PATH_TO_CONFIGS_REPO']
blob_storage = os.environ['BLOB_STORAGE']
log_level = os.environ['LOG_LEVEL']
vault_base_url = os.environ['VAULT_URL']
vault_token = os.environ['VAULT_TOKEN']
vault_path_secret = os.environ['VAULT_PATH_SECRET']

###########################

headers = {"Content-Type": "application/json"}

#Указание до директории с шаблонами
templates = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

'''
Названия шаблонов под рендер для запроса
'''
################
template_proxy = templates.get_template('common-proxy.json.j2')
template_group = templates.get_template('common-group.json.j2')
# template_user =  templates.get_template('common-users.json.j2')
################


if __name__ == '__main__':
    # Настройки логгирования
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # getUsersFromNexus(base_url=base_url+"/v1/security/users")
    list_repos_from_nexus = getReposFromNexus(base_url=base_url+"/v1/repositories/")
    print(list_repos_from_nexus)
    # Запуск по созданию proxy реп
    createProxyGroup = CreateRepo(
        path_to_configs_repos=path_to_configs_repos,
        base_url = base_url,
        list_repos_from_nexus = list_repos_from_nexus,
        template = template_proxy,
        username = username,
        password = password,
        headers = headers,
        blob_storage = blob_storage,
        vault_base_url= vault_base_url,
        vault_token=vault_token,
        vault_path_secret=vault_path_secret

    )
    # Запуск по созданию group реп
    createGroup = CreateRepo(
        path_to_configs_repos = path_to_configs_repos,
        base_url = base_url,
        list_repos_from_nexus = list_repos_from_nexus,
        template = template_group,
        username = username,
        password = password,
        headers = headers,
        blob_storage = blob_storage
    )
    createProxyGroup.ProxyRepo()
    createGroup.GroupRepo()
    CreateRepo(
        base_url = base_url,
        list_repos_from_nexus=list_repos_from_nexus,
        username = username,
        password = password,
        headers = headers
    ).delete_repos()