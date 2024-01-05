@order4
Feature: Feedback
    Scenario: Give Feedback
    Given i am on Feedback Page
    When i fill feedback score with 2
    And i fill feedback comment with 'This is a test comment'
    And i press Submit Feedback button
    Then i should be on Search  

    Scenario: Incomplete Feedback
    Given i am on Feedback Page
    When i fill feedback score with 2
    And i fill feedback comment with ''
    And i press Submit Feedback button
    Then the response should contain Give a rating or Proceed without feedback
    And i should be on Feedback Page  

    Scenario: Not Giving Feedback
    Given i am on Feedback Page
    When i press Skip Feedback button
    Then i should be on Search  