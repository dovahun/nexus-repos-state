class manageUsers():
    def __init__(
            self,
            base_url = "",
            path_to_configs_repos="",
            list_repos_from_nexus = "",
            template = "",
            username="",
            password="",
            headers="",
            blob_storage="",
            vault_base_url="",
            vault_token="",
            vault_path_secret=""
    ):
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

    def createUsers(self):

        None

    def deleteUSers(self):
        None
