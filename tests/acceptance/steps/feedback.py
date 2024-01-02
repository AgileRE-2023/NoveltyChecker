from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import Client

@given("I am on Feedback Page")
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

    context.Search_data = {'title': 'admin-chris', 'abstract': 'adelinejulia'}
    context.browser.get('http://127.0.0.1:8000/search') 

    # Example: Use Selenium to fill in form fields
    title_input = context.browser.find_element(By.ID, 'titlefield')
    abstract_input = context.browser.find_element(By.ID, 'abstractfield')

    title_input.send_keys(context.Search_data['title'])
    abstract_input.send_keys(context.Search_data['abstract'])

    search_button = context.browser.find_element(By.ID, 'search_button')
    search_button.click()

    new_search_button = context.browser.find_element(By.ID, 'new_search_button')
    new_search_button.click()


@when("i fill in Feedback Form with feedback score and comment")
def step_impl(context):
    context.feedback_data = {'comment': 'adelinejulia'}

    # Example: Use Selenium to fill in form fields
    comment_input = context.browser.find_element(By.ID, 'content')
    rate_input = context.browser.find_element(By.XPATH, "//input[@id='star2']")
    context.browser.execute_script("arguments[0].checked = true;",rate_input)

    comment_input.send_keys(context.feedback_data['comment'])

@when("I press Submit Feedback button")
def step_impl(context):
    # Example: Use Selenium to click the SignIn button
    submit_button = context.browser.find_element(By.ID, 'feedback')
    submit_button.click()

@when("I press Skip Feedback button")
def step_impl(context):
    # Example: Use Selenium to click the SignIn button
    skip_button = context.browser.find_element(By.ID, 'no_feedback')
    skip_button.click()

@then("the response should contain Give a rating or Proceed without feedback")
def step_impl(context):
    assert "Give a rating or Proceed without feedback" in context.browser.page_source, f"Expected 'Give a rating or Proceed without feedback' not in page source, but got {context.browser.page_source}"

# @then("I should be on Search")
# def step_impl(context):
#     # Implement code to check if the current page is the Search
#     context.browser.get('http://127.0.0.1:8000/search/')
#     assert context.browser.current_url == 'http://127.0.0.1:8000/search/', f"Expected Search page, but got {context.browser.current_url}"

@then("I should be on Feedback Page")
def step_impl(context):
    # Implement code to check if the current page is the SignIn page
    assert "Give Us Your Feedback" in context.browser.page_source, f"Expected 'Give Us Your Feedback' not in page source, but got {context.browser.page_source}"

# @then("close the browser")
# def step_impl(context):
#     context.browser.quit()

    
    