import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def lire_memoire():
    valeurs = {}

    with open("/proc/meminfo") as f:
        for ligne in f:
            cle, valeur = ligne.split(":", 1)
            valeurs[cle] = int(valeur.strip().split()[0])

    total = valeurs["MemTotal"]
    disponible = valeurs["MemAvailable"]

    return round((total - disponible) / total * 100, 1)


def lire_temperature():
    temperatures = []

    for nom in os.listdir("/sys/class/thermal"):
        if not nom.startswith("thermal_zone"):
            continue

        dossier = f"/sys/class/thermal/{nom}"

        try:
            with open(f"{dossier}/type") as f:
                type_capteur = f.read().strip()

            # Sélectionner uniquement les zones CPU
            if not type_capteur.startswith("cpu-"):
                continue

            with open(f"{dossier}/temp") as f:
                valeur = int(f.read().strip()) / 1000

            if 0 < valeur < 120:
                temperatures.append(valeur)

        except (OSError, ValueError):
            pass

    return round(max(temperatures), 1) if temperatures else None


class Serveur(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path != "/mesures":
            self.send_error(404)
            return

        donnees = {
            "temperature": lire_temperature(),
            "ram": lire_memoire(),
            "charge": round(os.getloadavg()[0], 2)
        }

        contenu = json.dumps(donnees).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(contenu)))
        self.end_headers()

        self.wfile.write(contenu)


serveur = HTTPServer(("0.0.0.0", 9000), Serveur)

print("Serveur actif sur le port 8000")
serveur.serve_forever()
