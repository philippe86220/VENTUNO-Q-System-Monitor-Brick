import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class SystemMonitor:

    def __init__(self, host="http://systemmonitor:9000"):
        self.host = host

    def get_mesures(self):
        try:
            with urlopen(self.host + "/mesures", timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))

        except HTTPError as e:
            return {"ok": False, "error": f"HTTP {e.code}"}

        except URLError as e:
            return {"ok": False, "error": str(e)}