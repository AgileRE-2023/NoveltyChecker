from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import Client

@given("i am on Search Page")
def step_impl(context):
    context.client = Client()
    context.browser = webdriver.Chrome()

    context.SignIn_data = {'username': 'admin-chris', 'password': 'adelinejulia'}
    context.browser.get('http://127.0.0.1:8000/accounts/signin') 

    # Example: Use Selenium to fill in form fields
    username_input = context.browser.find_element(By.ID, 'username')
    password_input = context.browser.find_element(By.ID, 'password')

    username_input.send_keys(context.SignIn_data['username'])
    password_input.send_keys(context.SignIn_data['password'])

    SignIn_button = context.browser.find_element(By.ID, 'signinbutton')
    SignIn_button.click()

@when("i fill all field in Search Form with title and abstract")
def step_impl(context):
    context.Search_data = {'title': 'admin-chris', 'abstract': 'adelinejulia'}
    context.browser.get('http://127.0.0.1:8000/search') 

    # Example: Use Selenium to fill in form fields
    title_input = context.browser.find_element(By.ID, 'titlefield')
    abstract_input = context.browser.find_element(By.ID, 'abstractfield')

    title_input.send_keys(context.Search_data['title'])
    abstract_input.send_keys(context.Search_data['abstract'])
    
@when("i fill Search Form with title only")
def step_impl(context):
    context.Search_data = {'title': '', 'abstract': 'noteditor123'}  # Update with your test data
    context.browser.get('http://127.0.0.1:8000/search')  # Update with your Django development server URL

    # Example: Use Selenium to fill in form fields
    title_input = context.browser.find_element(By.ID, 'titlefield')
    abstract_input = context.browser.find_element(By.ID, 'abstractfield')

    title_input.send_keys(context.Search_data['title'])
    abstract_input.send_keys(context.Search_data['abstract'])

@when("i press Search button")
def step_impl(context):
    # Example: Use Selenium to click the SignIn button
    search_button = context.browser.find_element(By.ID, 'search_button')
    search_button.click()

@when("i press List Recommendation button")
def step_impl(context):
    list_button = context.browser.find_element(By.ID, 'list_button')
    list_button.click()

@then("the response should contain Please fill both title and abstract")
def step_impl(context):
    assert "Please fill all the fields" in context.browser.page_source, f"Expected 'Please fill all the fields' not in page source, but got {context.browser.page_source}"

@then("i should be on Search Page")
def step_impl(context):
    # Implement code to check if the current page is the Search
    context.browser.get('http://127.0.0.1:8000/search/')
    assert context.browser.current_url == 'http://127.0.0.1:8000/search/', f"Expected Search page, but got {context.browser.current_url}"

@then("i should be on List Recommendation Page")
def step_impl(context):
    context.browser.get('http://127.0.0.1:8000/search/list')
    assert context.browser.current_url == 'http://127.0.0.1:8000/search/list/', f"Expected Search page, but got {context.browser.current_url}"


@then("i should be on Search Report Page")
def step_impl(context):
    # Implement code to check if the current page is the SignIn page
    assert "NOVELTY GRADE" in context.browser.page_source, f"Expected 'Novelty Grade' not in page source, but got {context.browser.page_source}"

@then("close the browser")
def step_impl(context):
    context.browser.quit()

    
    