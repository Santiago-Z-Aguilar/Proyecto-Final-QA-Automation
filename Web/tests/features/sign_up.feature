@web @sign_up
Feature: User Sign Up
  As a new or returning user
  I want to sign up with my credentials
  So that I can access my account

  # --- UI ELEMENTS ---
  Scenario: Sign Up button redirects correctly
    Given I am on the Home page
    When I click the Sign Up button
    Then I must be redirected to "/signup"

  Scenario: Sign Up button is displayed
    Given I am on the Home page
    Then the Sign Up button should be visible on the page

  Scenario: Sign Up button should not redirect to /signup
    Given I am on the Home page
    When I click the Sign Up button
    Then I will not be redirected to "/signup"

  Scenario: Sign Up button should not redirect to cart
    Given I am on the Home page
    When I click the Sign Up button
    Then I will not be redirected to "/cart"

  # --- FORM VALIDATIONS ---
  Scenario Outline: Try to sign up with different credentials
    Given I am on the Sign Up page
    When I submit the form with firstname "<firstname>", lastname "<lastname>", email "<email>", zipcode "<zipcode>", password "<password>"
    Then the sign up should be "<result>"

    Examples:
      | firstname | lastname | email               | zipcode | password | result   |
      | Ana       | Garcia   | ana.garcia@gmail.com| 90210   | Ana2024! | success  |
      | Ana       | Garcia   | ana.garcia@gmail.com| 90210   | 1        | success  |
      | Ana       | Garcia   | ana.garcia@gmail.com| 90210   | Ana2024! | failure  |
      | 12345     | 67890    | numbername@mail.com | 90210   | Juan#123 | failure  |
      | Juan      | Lopez    |                     | 90210   | Juan#123 | failure  |
      | Juan      | Lopez    | juan.lopez@gmail.com| text    | Juan#123 | failure  |
      | Juan      | Lopez    | invalidemail        | 90210   | Juan#123 | failure  |
      | Juan      | Lopez    | nodomain@.com       | 90210   | Juan#123 | failure  |
      |           |          |                     |         |          | failure  |
      | 12345     | 67890    | invalid@none        | abcd    | 123      | failure  |

