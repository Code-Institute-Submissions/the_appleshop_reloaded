# Compliance reports

* Compliance reports can be found in reports folder

https://github.com/poldi2018/the_appleshop_reloaded/tree/master/static/data/reports

* HTML code has been validated for errors and nesting mistakes

* CSS code has been checked.

* JSHint confirmed valid javascript code.

* Python code files are PEP8 conform


# Automatic Testing

* All methods have been tested by using Django Testkit, 98% coverage.

![Coverage overview](static/data/mockups/screens/coverage-ms5.jpg)


## A detailed coverage report is available here:

https://github.com/poldi2018/the_appleshop_reloaded/tree/master/htmlcov


* Tests can be run with following command:

```
coverage run --omit manage.py,appleshop/wsgi.py,appleshop/settings.py,env.py  --source=./ manage.py test

```


# Manual Testing

* All the functionality was also manually tested on physical devices, such as:

- Laptop, macbook pro 13"
- Iphone 8 plus
- Ipad Air
- Ipad mini


* On each device I confirmed proper functionality and page presentation by using Firefox, Safari and Chrome. For other devices, I used the preview in Chrome.



# Check for fullfillment of user requirements / goals

# User stories

* As a user I would like to have an overview of the variety of apples this shop has to offer.
*  As a user, I want to be able to register an account and to logon on from desktop or mobile device, so I can store my favourites list of apples and shopping cart for later review.
*  As a user, I expect that User preferences should list my user details and order history, User management
*  As a user, I would like to have the possibility to review products I have purchased.
*  As a user, I want to search for products based on entered search term.
*  As a user, I want to be able to pay by credit card.



# Shop features

* A user management has been implemented
* Products and reviews can be found by procuct name
* Shopping cart functionality, registered users can save cart to database.
* Checkout to finalise orders by paying with creditcard
* Review function for purchased items only
* Maintain a wish list for registered users
* User created cart and wishlist saved in database are merged with a possibly locally created list before being logged in. For the shopping cart, if a product is in server cart and local cart, the higher value is set on merged cart.
* free shipping above 50 EUR


I can confirm that all the user requirements and shop  features do work as expected. Field validators work fine.
