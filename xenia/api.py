import requests

class XeniaAPI:
    def __init__(self, ip):
        self.base = f"http://{ip}/api/v2"

    def overview(self):
        url = f"{self.base}/overview"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()

    def power(self, action: int):
        url = f"{self.base}/machine/control"
        r = requests.post(
            url,
            data={"action": action},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        r.raise_for_status()
        return r.text

    def execute_script(self, script_name: str, params: dict=None):
        url = f"{self.base}/execute_script"
        data = {'script': script_name}
        if params:
            data.update(params)
        r = requests.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10)
        r.raise_for_status()
        return r.text
