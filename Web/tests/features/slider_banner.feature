@web @slider
Feature: Banner Slider
  As a user
  I want to interact with the homepage banner slider
  So that I can navigate through slides and access promotions

  Background:
    Given I am on the home page with the banner slider

  @navigation
  Scenario: Slides move automatically with arrows
    When I click the next arrow
    Then the slide should change
    When I click the next arrow again
    Then another slide should be displayed
    When I click the previous arrow
    Then the slider should return to the previous slide

  @dots
  Scenario: Navigate using slider dots
    Then the first dot should be active
    When I click on the second dot
    Then the second dot should be active
    When I click on the third dot
    Then the third dot should be active

  @shop_now
  Scenario: Shop Now button redirects to Men Clothes
    When I click the "Shop Now" button on the first slide
    Then I will be redirected to the "men-clothes" category

  @explore
  Scenario: Explore button redirects to Electronics
    When I move to the second slide
    And I click the "Explore" button
    Then I should be redirected to the "electronics" category

  @order_now
  Scenario: Order Now button redirects to Groceries
    When I move to the third slide
    And I click the "Order Now" button
    Then I should be redirected to the "groceries" category