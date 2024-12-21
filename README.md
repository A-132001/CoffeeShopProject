"# Django-coffee-shop" static/img/mycoffee.png
# Coffee Shop Website

This is a coffee shop website built with Django. It allows users to sign in, sign up, view their profiles, browse products, make orders, and proceed to checkout. The website also features product search and pagination to improve user experience. The project is developed using Django as the backend and Django templates for the frontend in a stateful way.

![Coffee Shop Logo](static/img/mycoffee.png) 

## Features

- **Sign Up & Sign In**: Users can register and log in to their accounts.
- **User Profiles**: Users can view and edit their profiles.
- **Product Search**: Users can search for products based on keywords.
- **Pagination**: Products are displayed in pages for easy navigation.
- **Order Management**: Users can create and view orders.
- **Checkout System**: Users can proceed to checkout and complete their orders.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: Django Templates (HTML, CSS, JavaScript)
- **Database**: PostgreSQL
- **Pagination**: Django Paginator

## Setup

Follow these steps to set up and run the project locally:

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
```
### 2. Create a Virtual Environment
Navigate to the project directory and create a virtual environment:
```bash
python3 -m venv venv
```
### 3. Activate the Virtual Environment
```bash
venv\Scripts\activate
```
### 4. Install Dependencies
Install the required dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```
### 5. Set Up PostgreSQL Database
Update your PostgreSQL database settings in the settings.py file.
In settings.py, configure the DATABASES section to use PostgreSQL:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

###6. Apply Migrations
Apply the database migrations to set up your PostgreSQL database:
```bash
python manage.py migrate
```

###7. Create a Superuser (Optional)
Create a superuser account to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to enter the superuser's username, email, and password.

###8. Run the Development Server
Start the development server:
```bash
python manage.py runserver
```
You can now access the website at http://127.0.0.1:8000.
