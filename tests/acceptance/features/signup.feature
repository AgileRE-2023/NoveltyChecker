@order1
Feature: Sign Up
    Scenario: Success SignUp
    Given i am on SignUp Page
    When i fill all field in SignUp Form with new username
    And i press SignUp button
    Then i should be on SignIn

    Scenario: Username already exist
    Given i am on SignUp Page
    When i fill in SignUp Form with already exist username
    And i press SignUp button
    Then the response should contain Username already exist
    And i should be on SignUp Page

    Scenario: Incomplete SignUp
    Given i am on SignUp Page
    When i fill in SignUp Form with incomplete data
    And i press SignUp button
    Then the response should contain Please fill all the fields
    And i should be on SignUp Page  

    Scenario: Password not match
    Given i am on SignUp Page
    When i fill in SignUp Form with non matching password
    And i press SignUp button
    Then the response should contain Passwords do not match
    And i should be on SignUp Page   