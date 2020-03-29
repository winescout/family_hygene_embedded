import monitor
import wifimgr
from ota_update.main.ota_updater import OTAUpdater

def download_and_install_update_if_available(wlan):
    o = OTAUpdater('url-to-your-github-project')
    o.download_and_install_update_if_available(wlan)

def start():
     monitor.monitor()

def boot():
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Not connected to wifi.  Please unplug device, and try again.")
        while True:
            pass

    print("Wifi enabled.  Starting....")
    download_and_install_update_if_available(wlan)
    start()

boot()





