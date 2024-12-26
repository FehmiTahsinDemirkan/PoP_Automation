import threading
from onedrive_upload import upload_assets_folder_to_onedrive
import mindsitePrice
import gmail_api
import sharepoint


def run_gmail_api():
    output_folder = "assets"
    gmail_api.process_all_accounts(output_folder=output_folder)


def run_sharepoint():
    sharepoint.main()

def take_screenshot():
    mindsitePrice.main()

APP_ID = '4eeb88e1-1665-4527-bf2c-c0df55f25927'


if __name__ == '__main__':
    gmail_thread = threading.Thread(target=run_gmail_api)
    sharepoint_thread = threading.Thread(target=run_sharepoint)
    take_screenshot_thread = threading.Thread(target=take_screenshot)
    # Threadleri başlat
    gmail_thread.start()
    sharepoint_thread.start()
    take_screenshot_thread.start()

    # Threadlerin tamamlanmasını bekle
    gmail_thread.join()
    sharepoint_thread.join()
    take_screenshot_thread.join()
    upload_assets_folder_to_onedrive(APP_ID, folder_name='fehmimindsite', assets_folder_name='assets')


    print("Tamamlandi")
