# Django online shop 

This is an online shop API built using Django Rest Framework, with custom user accounts and JWT authentication.

## Users and authentication

-   Users' unique identifier is their phone number.
-   APIs are available for users to log in and sign up using an OTP mechanism.
-   Users can also log in and sign up using the normal sign-up process (phone number and password).
-   There is a "forgot password" functionality.
-   An API is provided for users to change their passwords.
-   Users can add and delete multiple addresses.
-   Users have an associated profile model that can be edited and updated.
## products
-   This platform allows you to create categories that have a hierarchical structure, meaning you can have multiple levels of categories nested within each other.
-   You have the ability to assign discounts to entire categories or specific products.
-   Each product can be customized with various options, such as different colors for a shirt.
-   Products can also include a "details table" that provides additional information.
-   There are APIs available that allow you to view the most popular products and products that are currently discounted.
-   Users have the ability to leave comments on products, providing their feedback and opinions.

## orders

- orders are made using product ids and counts which then the total price and discount is calculated
