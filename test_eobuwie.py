import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with  # nowosc od 4.0
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# PARAMETRY TESTU
#caps = {}
#caps['browserName'] = 'edge'

#GRID_HUB_URL = "127.0.0.1"

# Dane wejsciowe
haslo = "haslo123"


class RejestracjaNowegoUzytkownika(unittest.TestCase):
    def setUp(self):
        #  WARUNKI WSTEPNE
        # 1. Otwarcie strony glownej
        self.driver = webdriver.Chrome() # obsluga-chrome
        #self.driver = webdriver.Edge() # obsluga-edge
        #self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.EDGE)
        self.driver.maximize_window()
        self.driver.get('https://eobuwie.com.pl')
        # 2. Uzytkownik niezalogowany (ok)
        # 3. Potwierdzenie zgoda - ciasteczek!
        element = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/div/div[2]/button[1]")
        element.click()
        # ponizej wersja By.Class_NAME - tez dziala
        #self.driver.find_element(By.CLASS_NAME,
        #                         "e-button--type-primary.e-button--color-brand.e-consents-alert__button.e-button").click()

    def testbrakPodaniaImienia(self):
        sleep(3) # ma byc - czeka na zaladowanie calej strony ! Ale nieprofesjonalne!
        # na code share na koniec 25 09 jest info jak to lepiej rozwiazac

        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zarejestruj").click()
        nazwisko = self.driver.find_element(By.ID, "lastname")
        nazwisko.send_keys("Nowak")

        adres_mail = self.driver.find_element(By.ID, "email_address")
        adres_mail.send_keys("jannowak12341234@gmail.com")

        password_input = self.driver.find_element(By.ID, "password")
        for litera in haslo:
            password_input.send_keys(litera) # a tak z ciekawosci wpisuje po 1 literce
            print(litera, end='_') # sprawdzenie co send_keys faktycznie wpisal
           # sleep(1)

        password_confirmation = password_input = self.driver.find_element(By.ID, "confirmation")
        password_confirmation.send_keys(haslo)

        # Zaznaczenie checkboxa zgody
        self.driver.find_element(By.XPATH, '(//div[@class="checkbox-wrapper"])[2]').click() #dziaa

        # 7. Kliknij „Załóż nowe konto” (tylko dla przypadków niegatywnych!)
        self.driver.find_element(By.XPATH, '//button[@data-testid="register-create-account-button"]').click()

        ### OCZEKIWANY REZULTAT ####
        ############################
        # Użytkownik otrzymuje informację „To pole jest wymagane” pod imieniem
        # 1. Szukam pola imię
        imie = self.driver.find_element(By.NAME, "firstname")
        # 2. Szukam spana z błędem obok pola imię (nad nazwiskiem) przy pomocy 2 metod
        error_span = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').near(imie))
        error_span2 = self.driver.find_element(locate_with(By.XPATH, '//span[@class="form-error"]').above(nazwisko))
        # Sprawdzam, czy obie metody wskazują na ten sam element
        self.assertEqual(error_span.id, error_span2.id)  # assertEqual
        # 3. Sprawdzam, czy jest tylko jeden taki span
        errory = self.driver.find_elements(By.XPATH, '//span[@class="form-error"]')
        liczba_errorow = len(errory)
        self.assertEqual(liczba_errorow, 1)
        # 4. Sprawdzam, czy treść tegoż spana brzmi "To pole jest wymagane"
        self.assertEqual(error_span.text, "To pole jest wymagane")


        sleep(2) # 2 sek.

    def tearDown(self):
        self.driver.quit() # bo inaczej bedzie ostrzezenie na czerwono

if __name__ == '__main__':
    unittest.main()
# to jest taka pythonowa blokada bo jakbysmy zrobili import tego test_obuwia to bez tego
# te wszystkie testy stad by sie zaczely uruchamiac wiec to jest to po to aby sie uruchamialy
# te testy tylko w przypadku kiedy odpalilismy ten plik a nie odpalil sie w innym pliku
# poprzez import test_obuwia
