class Base:
    def __init__(self, token):
        self.base_url = "https://cloud.lambdalabs.com/api"
        self.headers = {"Authorization": f"Bearer {token}"}
