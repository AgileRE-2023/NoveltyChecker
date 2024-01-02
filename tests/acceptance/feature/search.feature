@order3
Feature: Search
    Scenario: Success Search
    Given i am on Search Page
    When i fill all field in Search Form with title and abstract
    And i press Search button
    Then i should be on Search Report Page

    Scenario: Success Search with List Recommendation
    Given i am on Search Page
    When i fill all field in Search Form with title and abstract
    And i press Search button
    Then i should be on Search Report Page
    When i press List Recommendation button
    Then i should be on List Recommendation Page

    Scenario: Incomplete Data Search
    Given i am on Search Page
    When i fill Search Form with title only
    And i press Search button
    Then the response should contain Please fill both title and abstract
    And i should be on Search Page