@web @logo
Feature: Logo visibility and redirection
  As a user
  I want to see the logo and use it for navigation
  So that I can return to the home page easily

  Background:
    Given I am on the home page

  Scenario: Logo redirects to home page
    When I navigate to the Books category
    And I click on the logo
    Then I should be redirected back to the home page

  Scenario: Logo is displayed
    Then the logo should be visible on the page

  Scenario: Logo is not displayed (negative case)
    Then the logo should not be visible on the page