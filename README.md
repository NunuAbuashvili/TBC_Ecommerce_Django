# Tea Shop E-commerce Platform

## Overview

A Django-based e-commerce platform specialized in tea products. 
This project features a responsive design converted from a fruit/vegetable template
into a dedicated tea shopping experience.
It is currently in the initial stage and will be expanded over time with more features.

## Features

- **Product Management**
    - Dynamic product catalog with detailed product pages.
    - Category-based product organization.
    - Case-insensitive search.
    - Advanced product filtering:
        - Category-based filtering (e.g., 'Christmas Tea').
        - Rating-based filtering (top-rated products).
        - Product sorting (by rating, price, upload date, and name).
        - Filtering by tags (Holiday Specials, Caffeine-free, Contains Cinnamon, Gift Box, and Only Few Items Left).
        - Filtering by price range.
    - Product image display.
- **User Interface**
    - Responsive design.
    - Intuitive navigation system.
    - Custom 404 error page.
    - Category-based browsing.
    - Dynamic content loading from database.
- **Shopping Experience**
    - Shopping cart system (in development):
        - Registered users are able to add products to their cart.
        - Total prices are calculated automatically.
        - The length of the cart is updated dynamically. 
    - Checkout process (in development)
    - Product ratings display.
- **User Features**
    - Contact form for customer inquiries (in development).
    - User registration form.
    - User authentication system.
    - User logout.
    - User profile (in development).
- **Class-based Views**


## Project Structure

### Apps
- `accounts`: Handles custom user implementation.
- `order`: Manages shopping cart and checkout process.
    - Models: Cart, CartItem
- `store`: Manages products and categories.
    - Models: Tea, Category, Tag
- `main`: Handles main page functionality.

### Templates
templates/
├── 404.html
├── base.html
├── partials/
│   ├── categories.html
│   ├── holiday-products.html
│   ├── related-products.html
│   ├── search.html
│   └── single-page-header.html
├── store/
│   ├── category-detail.html
│   ├── contact.html
│   ├── home.html
│   ├── shop.html
│   └── shop-detail.html
├── order/
│    ├── cart.html
│    └── checkout.html
├── accounts/
│   ├── login.html
│   ├── logout.html
    └── register.html


### API Endpoints

### Store
- `GET /`: Home page
- `GET /category`: Shop page with all products.
- `GET /category/<slug:slug>`: Category detail page.
- `GET /product/<slug:slug>`: Product detail page.
- `GET /search`: Search product.
- `GET /contact`: PContact form page.

### Order
- `GET /order/cart`: Shopping cart page.
- `POST /cart/add/<int:product_id>`: Add product to the cart.
- `POST /cart/update`: Update the quantity of the product in the cart.
- `POST /cart/remove`: Remove a product from the cart.
- `GET /order/checkout`: Checkout page.

### Accounts
- `POST /accounts/register`: Register new user.
- `GET /accounts/login`: User login.
- `GET /accounts/logout`: User logout.


## Future Plans
- Checkout functionality.
- Contact form update.
- Rating system implementation.


## Setup

1. Clone the repository.
2. Install the required packages:
    ```bash
   pip install -r requirements.txt
3. Run migrations: 
    ```bash
    python manage.py migrate
4. Create a superuser for accessing the admin panel: 
   ```bash
   python manage.py createsuperuser
5. Run the development server: 
   ```bash
   python manage.py runserver


## Directory Structure

ecommerce_platform/
├── accounts/       # Custom user authentication
├── media/          # User-uploaded content
├── order/         # Cart and checkout functionality
├── static/         # Static files (CSS, JS, images)
├── store/         # Product and category management
├── templates/      # HTML templates

## Technical Stack
- Backend: Django
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Additional libraries: Bootstrap

## Contributing
This project is part of a learning process. While contributions are welcome, 
please note that major changes may be implemented as part of the learning journey.

## Acknowledgements
- Original template source: [Template Source](https://themewagon.github.io/fruitables/index.html)

## Note
This README is in its initial state and will be updated regularly as the project evolves. 
Check back for the latest information on features and usage.

*Last updated: [31.10.2024]*