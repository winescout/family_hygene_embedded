import monitor
import wifimgr


wlan = wifimgr.get_connection()
if wlan is None:
    print("Not connected to wifi.  Please unplug device, and try again.")
    while True:
        pass

print("Wifi enabled.  Starting....")
monitor.monitor()
