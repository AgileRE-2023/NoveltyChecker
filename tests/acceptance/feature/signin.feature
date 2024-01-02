@order2
Feature: Sign In
    Scenario: Success SignIn
    Given i am on SignIn Page
    When i fill in username field with admin-chris
    And i fill in password field with adelinejulia
    And i press SignIn button
    Then i should be on Search

    Scenario: Incorrect username or Password
    Given i am on SignIn Page
    When i fill in username field with admin-chris
    And i fill in password field with jokowowkacaw
    And i press SignIn button
    Then the response should contain Invalid Credentials
    And i should be on SignIn Page   