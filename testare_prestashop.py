from telnetlib import EC
import pymysql
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestPrestaShop():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost/ro/')
        self.driver.set_window_size(1936, 1056)

    def teardown_method(self, method):
        self.driver.quit()
        with pymysql.connect(host='localhost', user='root', password='', database='prestashop') as conection:
            with conection.cursor() as cursor:
                cursor.execute('truncate table prestashop.ps_customer_message')

    def test_titlu_pagina(self):
        self.driver.get("http://localhost/ro/")
        assert self.driver.title == 'BrainTech'

    def test_brownbear(self):
        self.driver.find_element(By.NAME, "s").click()
        self.driver.find_element(By.NAME, "s").send_keys("brown bear")
        self.driver.find_element(By.NAME, "s").send_keys(Keys.ENTER)
        section = self.driver.find_element(By.ID, "products")
        subsection = section.find_element(By.ID, "js-product-list")
        element = subsection.find_element(By.XPATH,
                                          '/html/body/main/section/div/div/section/section/div[3]/div[1]/div[1]')
        text = element.find_element(By.XPATH,
                                    "/html/body/main/section/div/div/section/section/div[3]/div[1]/div[1]/article/div/div[2]/h2")
        inner_text = text.find_element(By.TAG_NAME, 'a')
        exact_text = inner_text.get_attribute('innerText')
        assert 'Brown Bear Cushion' == exact_text

    def test_accesorii_stationary(self):
        self.driver.find_element(By.CSS_SELECTOR, "#category-6 > .dropdown-item").click()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) .replace-2x").click()
        assert 'mountain-fox-notebook' in self.driver.page_source
        assert self.driver.title == 'Stationery'

    def test_home_accesory(self):
        self.driver.find_element(By.CSS_SELECTOR, "#category-6 > .dropdown-item").click()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) .replace-2x").click()
        assert self.driver.title == 'Home Accessories'

    def test_personalizare_cana(self):
        self.driver.find_element(By.CSS_SELECTOR, "#category-6 > .dropdown-item").click()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) .replace-2x").click()
        self.driver.find_element(By.CSS_SELECTOR, ".js-product:nth-child(8) img").click()
        element = self.driver.find_element(By.ID, "field-textField1")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click_and_hold().perform()
        element = self.driver.find_element(By.ID, "field-textField1")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.ID, "field-textField1")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()
        self.driver.find_element(By.ID, "field-textField1").click()
        self.driver.find_element(By.ID, "field-textField1").send_keys("Cea mai Buna Mama")
        self.driver.find_element(By.NAME, "submitCustomizedData").click()
        self.driver.find_element(By.CSS_SELECTOR, ".customization-message > label").click()
        element = self.driver.find_element(By.CLASS_NAME, 'customization-message')
        text = element.find_element(By.TAG_NAME, 'label')
        innertext = text.get_attribute('innerText')
        assert 'Cea mai Buna Mama' == innertext

    def test_creare_user_cu_acelasi_email(self):
        self.driver.find_element(By.CSS_SELECTOR, "a > .hidden-sm-down").click()
        self.driver.find_element(By.LINK_TEXT, "Nu ai cont? Creeaza unul aici").click()
        self.driver.find_element(By.ID, "field-id_gender-1").click()
        self.driver.find_element(By.ID, "field-firstname").click()
        self.driver.find_element(By.ID, "field-firstname").send_keys("Carabelea")
        self.driver.find_element(By.ID, "field-lastname").send_keys("Radu")
        self.driver.find_element(By.ID, "field-email").send_keys("radu_138@yahoo.com")
        self.driver.find_element(By.ID, "field-password").send_keys("123456789")
        self.driver.find_element(By.ID, "field-birthday").click()
        self.driver.find_element(By.ID, "field-birthday").send_keys("1993-12-09")
        self.driver.find_element(By.NAME, "psgdpr").click()
        self.driver.find_element(By.NAME, "customer_privacy").click()
        self.driver.find_element(By.CSS_SELECTOR, ".form-control-submit").click()
        element = self.driver.find_element(By.CLASS_NAME, 'help-block')
        alerta =element.find_element(By.TAG_NAME,'li')
        text = alerta.get_attribute('innerText')
        assert 'Aceasta adresa de e-mail este deja utilizata, te rugam sa alegi alta ori sa te autentifici' == text

    def test_logare_credentiale_bune(self):
        self.driver.find_element(By.CSS_SELECTOR, "a > .hidden-sm-down").click()
        self.driver.find_element(By.ID, "field-email").click()
        self.driver.find_element(By.ID, "field-email").send_keys("radu_138@yahoo.com")
        self.driver.find_element(By.ID, "field-password").send_keys("123456789")
        self.driver.find_element(By.ID, "submit-login").click()
        element = self.driver.find_element(By.CLASS_NAME,'account')
        nume = element.find_element(By.CLASS_NAME,'hidden-sm-down')
        text = nume.get_attribute('innerText')
        assert 'Carabelea Radu' == text

    def test_logare_credentiale_gresite(self):
        self.driver.find_element(By.CSS_SELECTOR, "a > .hidden-sm-down").click()
        self.driver.find_element(By.ID, "field-email").click()
        self.driver.find_element(By.ID, "field-email").send_keys("radu_138@yahoo.com")
        self.driver.find_element(By.ID, "field-password").send_keys("12345678")
        self.driver.find_element(By.ID, "submit-login").click()
        element = self.driver.find_element(By.CLASS_NAME,'login-form')
        eroare = element.find_element(By.TAG_NAME,'li')
        text = eroare.get_attribute('innerText')
        assert 'Autentificare esuata.' == text

    def test_log_out(self):
        self.driver.find_element(By.CSS_SELECTOR, "a > .hidden-sm-down").click()
        self.driver.find_element(By.ID, "field-email").click()
        self.driver.find_element(By.ID, "field-email").send_keys("radu_138@yahoo.com")
        self.driver.find_element(By.ID, "field-password").send_keys("123456789")
        self.driver.find_element(By.ID, "submit-login").click()
        self.driver.find_element(By.CSS_SELECTOR, "a > .material-icons").click()
        assert 'Carabelea Radu' not in self.driver.page_source

    def test_contact_clienti(self):
        self.driver.find_element(By.LINK_TEXT, "Contacteaza-ne").click()
        self.driver.find_element(By.ID, "id_contact").click()
        self.driver.find_element(By.CSS_SELECTOR, "#id_contact > option:nth-child(1)").click()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("radu138@gmail.com")
        self.driver.find_element(By.ID, "contactform-message").click()
        self.driver.find_element(By.ID, "contactform-message").send_keys(
            "Buna ziua ,vreau o oferta pentru o cana personalizata.")
        self.driver.find_element(By.NAME, "submitMessage").click()
        self.driver.get("http://localhost/admin3562ca7yc")
        self.driver.find_element(By.ID, "email").send_keys("radu138@gmail.com")
        self.driver.find_element(By.ID, "passwd").send_keys("Prestashop1!")
        self.driver.find_element(By.ID, "submit_login").click()
        self.driver.set_window_size(1936, 1056)
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.CSS_SELECTOR, "#subtab-AdminParentCustomerThreads span").click()
        self.driver.find_element(By.LINK_TEXT, "Customer Service").click()
        table = self.driver.find_element(By.ID, 'table-customer_thread')
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        firs_row = tbody.find_element(By.TAG_NAME, 'tr')
        msg_cell = firs_row.find_element(By.CLASS_NAME, 'column-messages')
        span = msg_cell.find_element(By.TAG_NAME, 'span')
        text = span.get_attribute('title')
        assert "Buna ziua ,vreau o oferta pentru o cana personalizata." == text
