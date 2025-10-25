# NixKart E-Commerce Platform

## Overview
NixKart is a modern, full-featured e-commerce platform built with Django. It features a dark-themed UI with advanced animations, product management, shopping cart functionality, user authentication, order processing, and Stripe payment integration.

## Project Information
- **Framework**: Django 5.2.7
- **Database**: SQLite (development), easily configurable for PostgreSQL in production
- **Payment Processing**: Stripe
- **Authentication**: Django Allauth (supports Google and GitHub OAuth)
- **UI Theme**: Dark modern design with animations and 3D product viewers

## Recent Changes
- **2025-10-25**: QR Code Integration
  - Added QR code generation for each product
  - Implemented automatic cart addition via QR code scanning
  - QR codes work in both development and production environments
  - Users can scan QR codes to instantly add products to their cart
  
- **2025-10-16**: Initial Replit setup
  - Configured Django settings for Replit environment
  - Added CORS and CSRF configuration for iframe compatibility
  - Configured WhiteNoise for static file serving
  - Set up development workflow on port 5000
  - Configured deployment with Gunicorn for production
  - Initialized database with sample data

## Project Architecture

### Key Components
1. **Store App** (`store/`)
   - Main e-commerce functionality
   - Product and category management
   - Shopping cart and wishlist
   - Order processing and tracking
   - User profiles and addresses

2. **Static Assets** (`static/`)
   - Custom CSS with animations
   - JavaScript for interactive features
   - Custom cursor, parallax scrolling, particle effects

3. **Templates** (`templates/store/`)
   - Django templates for all pages
   - Responsive design
   - Admin dashboard with charts

### Database Models
- **Category**: Product categories with images
- **Product**: Products with pricing, stock, images, and 3D models
- **Cart/CartItem**: Shopping cart functionality
- **Order/OrderItem**: Order management and tracking
- **UserProfile**: Extended user information
- **Wishlist**: User wishlist functionality
- **Address**: User shipping addresses

## Setup Instructions

### Development
The application is configured to run on port 5000:
```bash
python manage.py runserver 0.0.0.0:5000
```

### Default Users
Created by the startup script:
- **Admin**: username: `admin`, password: `admin123`
- **Staff**: username: `staff`, password: `staff123`
- **User**: username: `defaultuser`, password: `user123`

### Environment Variables
Required in `.env` file:
- `DEBUG`: Set to `True` for development
- `SECRET_KEY`: Django secret key
- `STRIPE_PUBLIC_KEY`: Stripe publishable key (optional)
- `STRIPE_SECRET_KEY`: Stripe secret key (optional)

## Deployment
The project is configured for Replit deployment using Gunicorn:
- **Build command**: Collects static files
- **Run command**: Gunicorn with 4 workers on port 5000
- **Static files**: Served by WhiteNoise middleware

## Features
- Product catalog with categories
- Advanced search and filtering
- Shopping cart with session support
- **QR Code Support**: Each product has a unique QR code that automatically adds the item to cart when scanned
- User authentication and profiles
- Order management and tracking
- Wishlist functionality
- Stripe payment integration
- Admin dashboard with analytics
- Responsive dark-themed UI
- Animated interactions and transitions
- 3D product viewer support

## Technical Notes
- CSRF and session cookies configured for iframe compatibility
- CORS enabled for development mode
- Static files served via WhiteNoise
- SQLite database for development (can be switched to PostgreSQL)
- Django Allauth for social authentication
- Crispy Forms for form rendering
- QR code generation using python-qrcode library with PIL support
- Environment-aware QR code URLs (works in both development and production)

## File Structure
```
ecommerce_project/          # Django project settings
store/                      # Main e-commerce app
templates/                  # HTML templates
static/                     # CSS, JS, images
media/                      # User-uploaded files
staticfiles/                # Collected static files
manage.py                   # Django management script
startup.py                  # Database initialization script
requirements.txt            # Python dependencies
```
