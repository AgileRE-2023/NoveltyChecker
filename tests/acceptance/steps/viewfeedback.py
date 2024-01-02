from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import Client

@given("i am on Admin Page")
def step_impl(context):
    context.client = Client()
    context.browser = webdriver.Chrome()

    context.SignIn_data = {'username': 'admin-chris', 'password': 'adelinejulia'}
    context.browser.get('http://127.0.0.1:8000/admin/login/?next=/admin/') 

    # Example: Use Selenium to fill in form fields
    username_input = context.browser.find_element(By.NAME, 'username')
    password_input = context.browser.find_element(By.NAME, 'password')

    username_input.send_keys(context.SignIn_data['username'])
    password_input.send_keys(context.SignIn_data['password'])

    SignIn_button = context.browser.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input')
    SignIn_button.click()


@when("i press View Feedback link")
def step_impl(context):
    # Example: Use Selenium to click the SignIn button
    feedbacks_link = context.browser.find_element(By.XPATH, '//*[@id="content-main"]/div[2]/table/tbody/tr/th/a')
    feedbacks_link.click()

@then("i should be on View Feedback Page")
def step_impl(context):
    assert "Select feedback to change" in context.browser.page_source, f"Expected 'Select feedback to change' not in page source, but got {context.browser.page_source}"

# @then("close the browser")
# def step_impl(context):
#     context.browser.quit()

    
    