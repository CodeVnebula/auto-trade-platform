# Car Marketplace Platform

Welcome to the **Car Marketplace Platform**! This web application is designed to facilitate seamless interactions between car buyers, sellers, and enthusiasts.

---

## Features

### For Sellers
- **Post Listings**: Easily create detailed car listings, including images, descriptions, pricing information...
- **Manage Listings**: Edit or delete your active listings at any time. (edit feature not supported yet).
- **Boost Visibility**: Use premium options to highlight your car and attract more buyers. (future plan).

### For Buyers
- **Advanced Search**: Find your ideal car using filters such as make, model, year, price range, mileage, and more.
- **Compare Listings**: View side-by-side comparisons of vehicles to make informed decisions.
- **Save Favorites**: Bookmark cars you're interested in for later review.

### For Enthusiasts
- **Car Specifications**: Explore in-depth details of different car models, including engine types, horsepower, dimensions, and other technical specifications. (future plan)
- **Community Reviews**: Read and leave reviews on cars and sellers. (future plan)
- **News and Updates**: Stay informed about automotive trends, new releases, and industry news. (future plan)

### General Features
- **User Authentication**: Secure login and registration system for buyers and sellers.
- **Mobile-Friendly Design**: Fully responsive interface for use on all devices.
- **API Integration**: The platform uses APIs to fetch real-time car data and updates.
- **Messaging**: Users can message each other to negotiate deals or ask questions about listings.

---

## Technology Stack

### Backend
- **Language & Framework**: Django (Python)
- **Database**: SQLite (development)
- **Authentication**: Django Rest Framework with JWT for secure token-based authentication.
- **Celery**: Used for parallel tasking such as sending emails, adding watermarks, and cropping uploaded images.

### Frontend
- **HTML/CSS/JavaScript**: Responsive templates with modern design.
- **Dynamic Interaction**: JavaScript modules for client-side functionality.

### API
- Integrates with external API for real-time car data, ensuring the platform stays updated with the latest information. (At the moment, the platform doesn't provide frontend functionality for pages like creating new listings, viewing car lists, or filtering cars.)

---

