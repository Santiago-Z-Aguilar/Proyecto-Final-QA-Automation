@web @search
Feature: Product search
  As a user
  I want to search for products
  So that I can find them quickly from the home page

  Background:
    Given I am on the home page

  Scenario: Search for Laptop does not redirect to expected product
    When I search for "Laptop"
    Then I will not be redirected to "https://shophub-commerce.vercel.app/product/22"
    And a screenshot is taken with name "search_laptop_redirect_fail"