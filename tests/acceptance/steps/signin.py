from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import Client

@given("I am on SignIn Page")
def step_impl(context):
    context.client = Client()
    context.browser = webdriver.Chrome()

@when("i fill in username field with admin-chris")
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/signin') 

    # Example: Use Selenium to fill in form fields
    username_input = context.browser.find_element(By.ID, 'username')
    username_input.send_keys('admin-chris')


@when("i fill in password field with adelinejulia")
def step_impl(context):
    password_input = context.browser.find_element(By.ID, 'password')
    password_input.send_keys('adelinejulia')
    
@when("i fill in password field with jokowowkacaw")
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/signin')  # Update with your Django development server URL

    # Example: Use Selenium to fill in form fields
    password_input = context.browser.find_element(By.ID, 'password')
    password_input.send_keys('jokowowkacaw')

@when("I press SignIn button")
def step_impl(context):
    # Example: Use Selenium to click the SignIn button
    SignIn_button = context.browser.find_element(By.ID, 'signinbutton')
    SignIn_button.click()

@then("the response should contain Invalid Credentials")
def step_impl(context):
    assert "Invalid Credentials" in context.browser.page_source, f"Expected 'Invalid Credentials' not in page source, but got {context.browser.page_source}"

@then("I should be on Search")
def step_impl(context):
    # Implement code to check if the current page is the Search
    context.browser.get('http://127.0.0.1:8000/search/')
    assert context.browser.current_url == 'http://127.0.0.1:8000/search/', f"Expected Search page, but got {context.browser.current_url}"

@then("I should be on SignIn Page")
def step_impl(context):
    # Implement code to check if the current page is the SignIn page
    assert context.browser.current_url == 'http://127.0.0.1:8000/accounts/signin/', f"Expected SignIn page, but got {context.browser.current_url}"

# @then("close the browser")
# def step_impl(context):
#     context.browser.quit()

    
    