from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import time

BOUTON_TROUVE = "bouton_trouve.csv"
BOUTON_NON_TROUVE = "bouton_non_trouve.csv"

def cliquer(browser, xpath):
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def saisir(browser, xpath, keys):
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.clear()
    element.send_keys(keys)


def element_exists(browser, xpath):
    try:
        WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return True
    except:
        return False

def connexion(browser):
    browser.get("https://simulent.partenaire.test-gar.education.fr/auth/login")
    saisir(browser, "/html/body/default-styles/div/div/div/section/div/div/form/p[1]/input", "matthieu.vacheron")
    saisir(browser, "/html/body/default-styles/div/div/div/section/div/div/form/p[2]/input-password/input",
           "Guizmo9174.")
    cliquer(browser, "/html/body/default-styles/div/div/div/section/div/div/form/div/button")


def aller_admin(browser):
    browser.get("https://simulent.partenaire.test-gar.education.fr/admin")


def manipuler_csv(browser, dossier, fichier_csv):
    chemin = os.path.join(dossier, fichier_csv)
    etablissement = fichier_csv.replace('.csv', '')

    with open(chemin, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')

        # Récupérer le premier nom et prénom pour la recherche initiale
        first_row = next(reader)
        nom_complet_initial = first_row['Nom'] + " " + first_row['Prénom']

        saisir(browser, "/html/body/admin-app/app-nav/portal/section/div/div/structure/structure-home/div/div/user-search-card/div[2]/search-input/input", nom_complet_initial)
        cliquer(browser, "/html/body/admin-app/app-nav/portal/section/div/div/structure/structure-home/div/div/user-search-card/div[2]/div/ul/li/a")
        time.sleep(1)

        # Traiter le nom de la première ligne à nouveau pour le processus de vérification du bouton, avant de traiter les autres noms
        for row in [first_row] + list(reader):
            nom_complet = row['Nom'] + " " + row['Prénom']
            saisir(browser, "/html/body/admin-app/app-nav/portal/section/div/div/structure/users-root/side-layout/div/div[1]/div/user-list/list/search-input/input", nom_complet)
            cliquer(browser, "/html/body/admin-app/app-nav/portal/section/div/div/structure/users-root/side-layout/div/div[1]/div/user-list/list/div[2]/ul/li")
            time.sleep(1)

            # Vérification de la présence du bouton
            if element_exists(browser,
                              "/html/body/admin-app/app-nav/portal/section/div/div/structure/users-root/side-layout/div/div[2]/div/user-detail/div[2]/user-info-section/panel-section/section/div[2]/form[3]/fieldset/form-field[2]/div/div/button"):
                cliquer(browser,
                        "/html/body/admin-app/app-nav/portal/section/div/div/structure/users-root/side-layout/div/div[2]/div/user-detail/div[2]/user-info-section/panel-section/section/div[2]/form[3]/fieldset/form-field[2]/div/div/button")
                time.sleep(1)

                # Attendre que l'élément contenant le mot de passe apparaisse
                xpath_mot_de_passe = "/html/body/admin-app/app-nav/portal/section/div/div/structure/users-root/side-layout/div/div[2]/div/user-detail/div[2]/user-info-section/panel-section/section/div[2]/form[3]/fieldset/form-field[2]/div/div/span"
                mot_de_passe = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_mot_de_passe))).text
                mot_de_passe = mot_de_passe.replace("Code généré : ", "")

                # Écrire dans le CSV bouton_trouve.csv
                with open(BOUTON_TROUVE, mode='a', newline='', encoding='utf-8') as output:
                    writer = csv.writer(output)
                    writer.writerow([row['Nom'], row['Prénom'], row['Login'], etablissement, mot_de_passe])

            else:
                with open(BOUTON_NON_TROUVE, mode='a', newline='', encoding='utf-8') as output:
                    writer = csv.writer(output)
                    writer.writerow([row['Nom'], row['Prénom'], row['Login'],etablissement, row["Code d'activation"]])

def main():
    browser = webdriver.Chrome()

    connexion(browser)

    dossiers = ["liste1", "liste2", "liste3", "liste4"]
    for dossier in dossiers:
        for fichier_csv in os.listdir(dossier):
            if fichier_csv.endswith('.csv'):
                aller_admin(browser)
                cliquer(browser, "/html/body/admin-app/app-nav/portal/header/div[1]/i")
                saisir(browser, "/html/body/admin-app/app-nav/portal/section/div/side-panel/div/div/search-input/input", fichier_csv.replace('.csv', ''))
                time.sleep(1)
                cliquer(browser, "/html/body/admin-app/app-nav/portal/section/div/side-panel/div/item-tree/ul/li/a")
                manipuler_csv(browser, dossier, fichier_csv)

    browser.quit()


if __name__ == "__main__":
    with open(BOUTON_TROUVE, mode='w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(["Nom", "Prénom", "Login", "Etablissement", "Mot de Passe"])
    with open(BOUTON_NON_TROUVE, mode='w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(["Nom", "Prénom", "Login", "Etablissement", "Code d'activation"])
    main()

