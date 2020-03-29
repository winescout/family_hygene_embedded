from main.monitor import monitor
from main.wifimgr import get_connection
from main.ota_updater import OTAUpdater

GITHUB_TOKEN_FILE="github_token.txt"
GITHUB_REPO="https://github.com/winescout/family_hygene_embedded"

def download_and_install_update_if_available(wlan):
    print("Checking for updates")
    with open(GITHUB_TOKEN_FILE) as f:
        token = f.readline()  
        o = OTAUpdater(GITHUB_REPO, headers={'User-Agent': 'winescout', 'Authorization': 'token {}'.format(token)})
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
