from main.monitor import monitor
from main.wifimgr import get_connection
from main.ota_update.main.ota_updater import OTAUpdater

def download_and_install_update_if_available(wlan):
    print("Checking for updates")
    token = "6f86eabc59d3034fd96736bc90b93c4c79124e06"
    o = OTAUpdater('https://github.com/winescout/family_hygene_embedded', headers={'Authorization': 'token {}'.format(token)})
    o.check_for_update_to_install_during_next_reboot()
    o.download_and_install_update_if_available(wlan)

def start():
     monitor()

def boot():
    wlan = get_connection()
    if wlan is None:
        print("Not connected to wifi.  Please unplug device, and try again.")
        while True:
            pass

    print("Wifi enabled.  Starting....")
    download_and_install_update_if_available(wlan)
    start()

boot()
