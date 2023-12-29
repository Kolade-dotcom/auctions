# Django Auction Site

## Overview

This Django project is an auction site where users can create listings, place bids, add items to their watchlist, and interact with other users through comments. The project also includes an admin interface for site administrators to manage listings, comments, and bids.

## Features

### Models

The project includes the following models:

- **User Model:** Django's default User model.
- **Auction Listings Model:** Represents auction listings with fields for title, description, starting bid, image URL, category, and other details.
- **Bids Model:** Stores bid information, including the amount, timestamp, and the associated listing.
- **Comments Model:** Allows users to add comments to auction listings.

### Functionality

1. **Create Listing:**
   - Users can create new listings by providing a title, description, starting bid, optional image URL, and category.

2. **Active Listings Page:**
   - The default route displays all currently active auction listings with essential details.

3. **Listing Page:**
   - Clicking on a listing takes users to a specific page with details such as title, description, current price, and image (if available).
   - Signed-in users can add items to their watchlist, place bids, and close auctions if they are the listing creator.

4. **Watchlist:**
   - Users can view all listings they have added to their watchlist on a dedicated Watchlist page.

5. **Categories:**
   - A page displays a list of all listing categories.
   - Clicking on a category name shows all active listings in that category.

6. **Django Admin Interface:**
   - Site administrators can manage listings, comments, and bids through the Django admin interface.

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/django-auction-site.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Visit [http://localhost:8000/admin](http://localhost:8000/admin) to access the Django admin interface and manage the site.

## Contributing

Contributions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).
