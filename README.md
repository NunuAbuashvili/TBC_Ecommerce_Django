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
    - Advanced product filtering:
        - Category-based filtering (e.g., 'Christmas Tea')
        - Rating-based filtering (top-rated products).
    - Product image display.
- **User Interface**
    - Responsive design.
    - Intuitive navigation system.
    - Custom 404 error page.
    - Category-based browsing.
    - Dynamic content loading from database.
- **Shopping Experience**
    - Shopping cart system (in development)
    - Checkout process (in development)
    - Product ratings display.
- **User Features**
    - Contact form for customer inquiries (in development)
    - User authentication system (in development)


## Project Structure

### Apps
- `accounts`: Handles custom user implementation.
- `order`: Manages shopping cart and checkout process.
    - Models: Cart, CartItem
- `contact`: Handles customer inquiries.
- `store`: Manages products and categories.
    - Models: Tea, Category
- `main`: Handles main page functionality.

### Templates
templates/
├── 404.html
├── base.html
├── shop-base.html
├── partials/
│   ├── categories.html
│   ├── holiday-products.html
│   ├── related-products.html
│   ├── search-input.html
│   └── single-page-header.html
├── store/
│   ├── category-detail.html
│   ├── shop.html
│   └── shop-detail.html
├── order/
│   ├── cart.html
│   └── checkout.html
├── main/
│   └── home.html
└── contact/
    └── contact.html

### API Endpoints

### Main
- `GET /`: Home page

### Store
- `GET /category/`: Shop page with all products.
- `GET /category/<slug:slug>/`: Category detail page.
- `GET /category/product/<slug:slug>/`: Product detail page.

### Order
- `GET /order/cart/`: Shopping cart page.
- `GET /order/checkout/`: Checkout page.

### Contact
- `GET /contact`: Contact form page.

## Future Plans
- User authentication.
- Shopping cart functionality.
- Checkout functionality.
- Contact form update.
- Product search implementation.
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
├── contact/       # Contact form handling
└── main/          # Main page functionality
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

*Last updated: [21.10.2024]*