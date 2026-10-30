from systemmonitor import SystemMonitor
from arduino.app_utils import App

monitor = SystemMonitor()

print(monitor.get_mesures())

App.run()