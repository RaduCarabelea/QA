from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


@given('we are on the log in page')
def step_impl(context):
    driver.get('http://localhost/ro/')
    driver.set_window_size(1936, 1056)
    driver.find_element(By.CSS_SELECTOR, "a > .hidden-sm-down").click()
    driver.find_element(By.ID, "field-email").send_keys("radu_138@yahoo.com")
    driver.find_element(By.ID, "field-password").send_keys("123456789")


@when('the user clicks on login button')
def step_impl(context):
    driver.find_element(By.ID, "submit-login").click()


@then('it should see his name in the top of the page')
def step_impl(context):
    account = driver.find_element(By.CLASS_NAME, 'account')
    span = account.find_element(By.CLASS_NAME, 'hidden-sm-down')
    inner_text = span.get_attribute('innerText')
    driver.quit()
    assert 'Carabelea Radu' == inner_text
