import os
import shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def cliquer(browser, xpath):
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def saisir(browser, xpath, keys):
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.clear()
    element.send_keys(keys)

def connexion(browser):
    browser.get("https://simulent.partenaire.test-gar.education.fr/auth/login")
    saisir(browser, "/html/body/default-styles/div/div/div/section/div/div/form/p[1]/input", "matthieu.vacheron")
    saisir(browser, "/html/body/default-styles/div/div/div/section/div/div/form/p[2]/input-password/input",
           "Guizmo9174.")
    cliquer(browser, "/html/body/default-styles/div/div/div/section/div/div/form/div/button")

def aller_admin(browser):
    browser.get("https://simulent.partenaire.test-gar.education.fr/admin")
    cliquer(browser, "/html/body/admin-app/app-nav/portal/header/div[2]/a[1]")
    cliquer(browser, "/html/body/admin-portal/section/section/article/div/div[1]/a")
    acceder_listes(browser)

def acceder_listes(browser):
    cliquer(browser, "/html/body/admin-portal/section/section/article/div/div[2]")
    cliquer(browser, "/html/body/admin-portal/section/section/article/div[2]/div/div[1]/nav/ul/li")

    listes = [
        "/html/body/admin-portal/section/section/article/div[2]/div/div[1]/nav/ul/li/span/ul/li[1]",
        "/html/body/admin-portal/section/section/article/div[2]/div/div[1]/nav/ul/li/span/ul/li[2]",
        "/html/body/admin-portal/section/section/article/div[2]/div/div[1]/nav/ul/li/span/ul/li[3]",
        "/html/body/admin-portal/section/section/article/div[2]/div/div[1]/nav/ul/li/span/ul/li[4]"
    ]

    for idx, liste in enumerate(listes, 1):
        cliquer(browser, liste)
        traite_elements_liste(browser, idx)

def traite_elements_liste(browser, idx):
    x = 1
    while True:
        try:
            path = f"/html/body/admin-portal/section/section/article/div[2]/div/div[1]/nav/ul/li/span/ul/li[{idx}]/span/ul/li[{x}]"
            cliquer(browser, path)
            cliquer(browser, "/html/body/admin-portal/section/section/article/div[2]/article/div/button")
            sleep(5)
            download_file_path = wait_for_download(os.getcwd())
            title_path = "/html/body/admin-portal/section/section/article/div[2]/article/div/div[1]/h1"
            title = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, title_path))).text
            title = nommage_filename(title) + ".csv"
            list_dir = os.path.join(os.getcwd(), f"liste{idx}")
            if not os.path.exists(list_dir):
                os.makedirs(list_dir)
            shutil.move(download_file_path, os.path.join(list_dir, title))
            x += 1
        except:
            break

def wait_for_download(download_dir):
    while True:
        files = os.listdir(download_dir)
        if any(file.endswith('.crdownload') for file in files):
            continue
        csv_files = [file for file in files if file.endswith('.csv')]
        if csv_files:
            return os.path.join(download_dir, csv_files[0])
        sleep(1)

def nommage_filename(filename):
    return ''.join(c for c in filename if c.isalnum() or c in (' ', '.', '-', "'")).rstrip()


def main():
    download_dir = os.path.abspath(os.getcwd())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs',  {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
        }
    )
    browser = webdriver.Chrome(options=chrome_options)

    try:
        connexion(browser)
        aller_admin(browser)
        acceder_listes(browser)
    finally:
        browser.quit()

# -- Lancer le script -- #
if __name__ == "__main__":
    main()
