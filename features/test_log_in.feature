Feature: login on the shop

  Scenario: do a simple login
    Given  we are on the log in page
     When the user clicks on login button
     Then it should see his name in the top of the page
