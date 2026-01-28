# PicMe - Photo Gallery App

A clean and simple photo gallery application where you can discover, share, and interact with photos from the community.

## What is PicMe?

PicMe is a web-based photo gallery platform built with Django. Browse a collection of beautiful photos organized by tags, search for specific images, and engage with the community by liking or disliking photos. Create an account to manage your profile and contribute to the gallery.

## Features

- **Discover Photos** - Browse a beautiful gallery of photos with responsive grid layout
- **Search & Filter** - Find photos by title, description, or tags
- **Social Interactions** - Like and dislike photos to engage with the community
- **User Accounts** - Create an account, manage your profile, and upload a profile picture
- **Secure Authentication** - Email-based login with password reset functionality
- **User Profiles** - Customize your profile with bio and profile picture
- **Tag Organization** - Photos organized with tags for easy discovery

## Quick Start

### Prerequisites
- Python 3.14+
- PostgreSQL
- pip



## Usage

### User Registration & Login

1. Navigate to the register page
2. Create an account with email and password
3. Log in with your credentials
4. Access the password reset feature if needed

### Profile Management

1. Navigate to your profile page
2. Update your bio and upload a profile picture
3. Changes are saved to your account

### Photo Gallery

1. Browse the photo gallery on the home page
2. Search for photos by title or description
3. Filter photos by tags
4. Like or dislike photos to engage with the community

### Admin Panel

Access the Django admin panel at `/admin/` with your superuser credentials to:
- Manage users and profiles
- Add, edit, or delete photos
- Manage tags
- View user interactions


## Models

### CustomUser
- **Fields**: email, username, first_name, last_name, password, date_joined
- Custom user model with email-based authentication

### UserProfile
- **Fields**: user (OneToOne), bio, profile_picture, created_at, updated_at
- Extended user profile created automatically on user registration

### Photo
- **Fields**: title, description, image, uploaded_by (ForeignKey to User), tags (ManyToMany), created_at, updated_at
- Main model for photo gallery entries

### PhotoInteraction
- **Fields**: user (ForeignKey), photo (ForeignKey), interaction_type (like/dislike), created_at
- Tracks user interactions with photos

### Tag
- **Fields**: name, slug
- Used to categorize and organize photos

## API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /register/` - User registration
- `GET /password-reset/` - Request password reset
- `POST /password-reset-confirm/<uidb64>/<token>/` - Confirm password reset

### Photo Gallery
- `GET /` - View all photos (home page)
- `GET /photo/<id>/` - View photo details
- `POST /photo/<id>/interact/` - Like/dislike a photo

### User
- `GET /profile/` - View user profile
- `POST /profile/` - Update profile



## Technologies Used

- **Backend**: Django 6.0.1
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in auth system (customized)
- **Image Processing**: Pillow


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Authors

Created with Alvin Sarisar



**Last Updated**: January 28, 2026




