import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -- Attendre et cliquer sur un élément -- #
def cliquer(browser, xpath):
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

# -- Attendre, vider un champ, puis envoyer -- #
def saisir(browser, xpath, keys):
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    element.clear()
    element.send_keys(keys)

def charger_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def post_connexion(browser, code_activation):
    saisir(browser, "/html/body/default-styles/div/div/section/div/form/p[3]/input-password/input", code_activation)
    saisir(browser, "/html/body/default-styles/div/div/section/div/form/input-password/input", code_activation)
    cliquer(browser, "/html/body/default-styles/div/div/section/div/form/p[8]/input")
    cliquer(browser, "/html/body/default-styles/div/div/section/div/form/input[2]")


def connexion(browser, identifiant, mdp, etablissement):
    try:
        cliquer(browser, "/html/body/portal/header/section[2]/nav/a[4]")
        time.sleep(1)
    except:
        pass

    browser.get("https://simulent.partenaire.test-gar.education.fr/auth/login")

    saisir(browser, "/html/body/default-styles/div/div/div/section/div/div/form/p[1]/input", identifiant)
    saisir(browser, "/html/body/default-styles/div/div/div/section/div/div/form/p[2]/input-password/input", mdp)
    cliquer(browser, "/html/body/default-styles/div/div/div/section/div/div/form/div/button")
    time.sleep(1)

    if browser.current_url in ["https://simulent.partenaire.test-gar.education.fr/admin",
                               "https://simulent.partenaire.test-gar.education.fr/timeline/timeline"]:
        print(f"Redirection inattendue pour {identifiant} - {mdp} - {etablissement}")
        raise Exception("Redirection vers la page admin ou timeline")

    elif browser.current_url != "https://simulent.partenaire.test-gar.education.fr/auth/login":
        print(f"Mauvaise URL de redirection pour {identifiant} - {mdp} - {etablissement}")
        raise Exception("Mauvaise redirection")


def main():
    browser = webdriver.Chrome()
    data = charger_csv("bouton_non_trouve.csv")

    for row in data:
        identifiant = row["Login"]
        mdp = row["Code d'activation"]
        etablissement = row.get("Etablissement", "")

        if not mdp:
            print(f"Mot de passe vide pour {identifiant} - {etablissement}")
            continue

        try:
            connexion(browser, identifiant, mdp, etablissement)
            post_connexion(browser, mdp)
        except Exception as e:
            print(f"Erreur pour {identifiant} - {mdp} - {etablissement}: {str(e)}")
            continue
    browser.quit()

if __name__ == "__main__":
    main()
