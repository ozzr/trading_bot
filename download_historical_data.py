from constants import SSID, ASSETS
from pocket_option_tools.platforms.pocketoption.stable_api import PocketOption
from trading_tools.historical_data import download_assets_history

if __name__ == "__main__":
    api: PocketOption = PocketOption(SSID, True)
    api.connect()
    download_assets_history(ASSETS, api)