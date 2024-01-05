@order1
Feature: Sign Up
    Scenario: Success SignUp
    Given i am on SignUp Page
    When i fill username field with new username 'testuser'
    And i fill email address field with 'testuser@gmail.com'
    And i fill password field with valid password 'testuser123'
    And i fill confirm password field with matching password 'testuser123'
    And i press SignUp button
    Then i should be on SignIn

    Scenario: Username already exist
    Given i am on SignUp Page
    When i fill username field with existing username 'testuser'
    And i fill email address field with 'testuser@gmail.com'
    And i fill password field with valid password 'testuser123'
    And i fill confirm password field with matching password 'testuser123'
    And i press SignUp button
    Then the response should contain Username already exist
    And i should be on SignUp Page

    Scenario: Incomplete SignUp
    Given i am on SignUp Page
    When i fill username field with nothing ''
    And i fill email address field with 'testuser@gmail.com'
    And i fill password field with valid password 'testuser123'
    And i fill confirm password field with matching password 'testuser123'
    And i press SignUp button
    Then the response should contain Please fill all the fields
    And i should be on SignUp Page  

    Scenario: Password not match
    Given i am on SignUp Page
    When i fill username field with new username 'testuser'
    And i fill email address field with 'testuser@gmail.com'
    And i fill password field with valid password 'testuser123'
    And i fill confirm password field with non matching password 'testuser12345'
    And i press SignUp button
    Then the response should contain Passwords do not match
    And i should be on SignUp Page   