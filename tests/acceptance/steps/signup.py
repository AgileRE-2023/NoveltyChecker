from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import Client

@given('I am on SignUp Page')
def step_impl(context):
    context.browser = webdriver.Chrome()


@when("i fill username field with new username 'testuser'")
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/signup')
    username_input = context.browser.find_element(By.ID, 'username')
    username_input.send_keys('testuser')

@when("i fill email address field with 'testuser@gmail.com'")
def step_impl(context):
    email_input = context.browser.find_element(By.ID, 'email')
    email_input.send_keys('testuser@gmail.com')

@when("i fill password field with valid password 'testuser123'")
def step_impl(context):
    password_input = context.browser.find_element(By.ID, 'password')
    password_input.send_keys('testuser123')

@when("i fill confirm password field with matching password 'testuser123'")
def step_impl(context):
    confirmation_password_input = context.browser.find_element(By.ID, 'confirmation_password')
    confirmation_password_input.send_keys('testuser123')

@when("i fill confirm password field with non matching password 'testuser12345'")
def step_impl(context):
    confirmation_password_input = context.browser.find_element(By.ID, 'confirmation_password')
    confirmation_password_input.send_keys('testuser12345')

@when("i fill username field with existing username 'testuser'")
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/signup')
    username_input = context.browser.find_element(By.ID, 'username')
    username_input.send_keys('testuser')

@when("i fill username field with nothing ''")
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/accounts/signup')
    username_input = context.browser.find_element(By.ID, 'username')
    username_input.send_keys('')

# @when('I fill all field in SignUp Form with new username')
# def step_impl(context):
#     context.SignUn_data = {'username': 'Tiyono', 'email':'tiyono@gmail.com','password': 'adelinejulia','confirm_password':'adelinejulia'}
#     context.browser.get('http://127.0.0.1:8000/accounts/signup')

#     # Replace these values with actual form field names and desired username
#     username_input = context.browser.find_element(By.ID, 'username')
#     email_input = context.browser.find_element(By.ID, 'email')
#     password_input = context.browser.find_element(By.ID, 'password')
#     confirm_password_input = context.browser.find_element(By.ID, 'confirmation_password')

#     username_input.send_keys(context.SignUn_data['username'])
#     email_input.send_keys(context.SignUn_data['email'])
#     password_input.send_keys(context.SignUn_data['password'])
#     confirm_password_input.send_keys(context.SignUn_data['confirm_password'])

# @when('I fill in SignUp Form with already exist username')
# def step_impl(context):
#     # Replace 'existing_username' with the desired existing username for testing
#     context.SignUn_data = {'username': 'admin-chris', 'email':'Hans@gmail.com','password': 'adelinejulia','confirm_password':'adelinejulia'}
#     context.browser.get('http://127.0.0.1:8000/accounts/signup')
    
#     username_input = context.browser.find_element(By.ID, 'username')
#     email_input = context.browser.find_element(By.ID, 'email')
#     password_input = context.browser.find_element(By.ID, 'password')
#     confirm_password_input = context.browser.find_element(By.ID, 'confirmation_password')

#     username_input.send_keys(context.SignUn_data['username'])
#     email_input.send_keys(context.SignUn_data['email'])
#     password_input.send_keys(context.SignUn_data['password'])
#     confirm_password_input.send_keys(context.SignUn_data['confirm_password'])

# @when('I fill in SignUp Form with incomplete data')
# def step_impl(context):
#     # Simulate incomplete data by leaving some fields blank
#     context.SignUn_data = {'username': 'testr', 'email':'','password': 'adelinejulia','confirm_password':'adelinejulia'}
#     context.browser.get('http://127.0.0.1:8000/accounts/signup')
    
#     username_input = context.browser.find_element(By.ID, 'username')
#     email_input = context.browser.find_element(By.ID, 'email')
#     password_input = context.browser.find_element(By.ID, 'password')
#     confirm_password_input = context.browser.find_element(By.ID, 'confirmation_password')

#     username_input.send_keys(context.SignUn_data['username'])
#     email_input.send_keys(context.SignUn_data['email'])
#     password_input.send_keys(context.SignUn_data['password'])
#     confirm_password_input.send_keys(context.SignUn_data['confirm_password'])

# @when('I fill in SignUp Form with non matching password')
# def step_impl(context):
#     # Simulate non-matching passwords
#     context.SignUn_data = {'username': 'Jokowow', 'email':'Hans@gmail.com','password': 'adelinejulia','confirm_password':'adelineonly'}
#     context.browser.get('http://127.0.0.1:8000/accounts/signup')
    
#     username_input = context.browser.find_element(By.ID, 'username')
#     email_input = context.browser.find_element(By.ID, 'email')
#     password_input = context.browser.find_element(By.ID, 'password')
#     confirm_password_input = context.browser.find_element(By.ID, 'confirmation_password')

#     username_input.send_keys(context.SignUn_data['username'])
#     email_input.send_keys(context.SignUn_data['email'])
#     password_input.send_keys(context.SignUn_data['password'])
#     confirm_password_input.send_keys(context.SignUn_data['confirm_password'])

@when('I press SignUp button')
def step_impl(context):
    # Replace 'signup_button' with the actual name or identifier of your signup button
    signup_button = context.browser.find_element(By.ID, 'signup_button')
    signup_button.click()

@then('the response should contain Username already exist')
def step_impl(context):
    # Implement the assertion for the existence of the specified message in the response
    assert "Username already exist" in context.browser.page_source, f"Expected 'Username already exist' not in page source, but got {context.browser.page_source}"

@then('the response should contain Please fill all the fields')
def step_impl(context):
    # Implement the assertion for the existence of the specified message in the response
    assert "Please fill all the fields" in context.browser.page_source, f"Expected 'Please fill all the fields' not in page source, but got {context.browser.page_source}"

@then('the response should contain Passwords do not match')
def step_impl(context):
    # Implement the assertion for the existence of the specified message in the response
    assert "Passwords do not match" in context.browser.page_source, f"Expected 'Passwords do not match' not in page source, but got {context.browser.page_source}"

@then('I should be on SignIn')
def step_impl(context):
    # Implement the assertion for being on the SignIn page
    assert context.browser.current_url == 'http://127.0.0.1:8000/accounts/signin/', f"Expected SignIn page, but got {context.browser.current_url}"

@then('I should be on SignUp Page')
def step_impl(context):
    # Implement the assertion for being on the SignUp page
    assert context.browser.current_url == 'http://127.0.0.1:8000/accounts/signup/', f"Expected signup page, but got {context.browser.current_url}"

# @then('close the browser')
# def step_impl(context):
#     context.browser.quit()