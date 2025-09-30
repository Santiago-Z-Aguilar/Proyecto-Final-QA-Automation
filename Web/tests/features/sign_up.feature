@web @sign_up
Feature: User Sign Up
  As a new or returning user
  I want to sign up with my credentials
  So that I can access my account

  # --- UI ELEMENTS ---
  Scenario: Sign Up button redirects correctly
    Given I am on the Home page
    When I click the Sign Up button
    Then I must be redirected to "/sign-up"

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
      | John      | Doe      | john.doe@mail.com   | 12345   | Pass123! | success  |
      | Alice     | Smith    | alice@mail.com      | 54321   | 123456   | success  |
      | John      | Doe      | already@mail.com    | 11111   | Pass123! | failure  |
      | 123       | 456      | numbername@mail.com | 22222   | Pass123! | failure  |
      | Bob       | Brown    |                     | 33333   | Pass123! | failure  |
      | Mary      | Stone    | mary@mail           | text    | Pass123! | failure  |
      | Eva       | Adams    | invalidemail        | 44444   | Pass123! | failure  |
      | Max       | Payne    | max@nodomain        | 55555   | Pass123! | failure  |
      |           |          |                     |         |          | failure  |
      | 123       | 456      | invalid@none        | abcd    | 123      | failure  |