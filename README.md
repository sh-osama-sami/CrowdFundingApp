# CrowdFunding WebApp

Welcome to the CrowdFunding WebApp project! This README file provides an extensive overview of the project, including its features, technologies used, installation instructions, usage guidelines, project structure, contribution guidelines, and licensing information.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
   - [User Features](#user-features)
   - [Admin Features](#admin-features)
3. [Technologies Used](#technologies-used)
   - [Backend Technologies](#backend-technologies)
   - [Frontend Technologies](#frontend-technologies)
   - [Database](#database)
4. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
   - [User Actions](#user-actions)
   - [Admin Actions](#admin-actions)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
   - [Getting Started](#getting-started)
   - [Submitting Changes](#submitting-changes)
8. [Project Team](#project-team)
9. [License](#license)


## Introduction

CrowdFunding WebApp is a full-stack web application developed using the Django framework, Python, Bootstrap, HTML/CSS, and JavaScript. It provides a platform for users to create, explore, and support crowdfunding projects across various categories. The primary aim of this project is to facilitate crowdfunding activities while offering a seamless user experience and robust administrative capabilities.

## Features

### User Features:

1. **Registration and Authentication:**
   - Users can register new accounts by providing basic information such as username, mobile phonne number, profile picture, email, and password.
   - Email verification is implemented to ensure the security and validity of user accounts.

2. **Project Creation and Management:**
   - Registered users can create crowdfunding projects by adding detailed descriptions, images, target, start/end dates, and tags.
   - Project creators have full control over their projects, including updating project information and deleting projects if needed.

3. **Project Discovery and Support:**
   - Projects are categorized based on themes or topics, making it easy for users to discover projects of interest.
   - Users can support projects by making donations. Project progress and funding updates are displayed in real-time.

4. **User Profiles and Activity Tracking:**
   - Each user has a profile showcasing their created projects, supported projects, contribution history, and account details.
   - User profiles provide insights into user activity, project involvement, and overall impact within the crowdfunding community.

5. **Search and Filtering:**
   - Robust search functionality enables users to find projects based on title, category, or a tag.
   - Advanced filtering options allow users to refine search results and explore projects efficiently.

### Admin Features:

1. **Administrative Dashboard:**
   - Admins have access to a dedicated administrative dashboard for managing categories, projects, and user accounts.
   - The dashboard provides comprehensive tools for content moderation, user verification, and data analysis.

2. **Content Moderation and Review:**
   - Admins can review and moderate user-generated content, including project submissions, comments, and user profiles.
   - Content moderation ensures compliance with community guidelines, quality standards, and legal requirements.

3. **User Management:**
   - Admins can manage user accounts, including user roles, permissions, account status, and password resets.
   - User management tools enable admins to maintain a secure and organized user database.

4. **Analytics and Reporting:**
   - The admin dashboard includes analytics and reporting features for tracking project performance, user engagement, and financial metrics.
   - Data visualization tools provide insights into crowdfunding trends, campaign success rates, and user behavior patterns.

## Technologies Used

### Backend Technologies:

- **Django:** A high-level Python web framework for rapid development, clean design, and scalability.
- **Python:** The primary programming language used for backend logic, data processing, and server-side operations.
- **SQLite:** A lightweight relational database management system used for storing project data, user information, and session management.
- **Django REST Framework (DRF):** Used for building RESTful APIs to support frontend interactions, data retrieval, and AJAX requests.
- **Celery:** An asynchronous task queue for handling background tasks, scheduled jobs, and processing heavy computations.
- **Redis:** In-memory data structure store used as a message broker for Celery and caching system for performance optimization.

### Frontend Technologies:

- **HTML/CSS:** Markup and styling languages for creating structured web pages, responsive layouts, and custom UI components.
- **Bootstrap:** Frontend framework for CSS styling, responsive design, grid system, and pre-built components like modals, forms, and navigation bars.
- **JavaScript:** Client-side scripting language for dynamic content, interactive features, form validation, and AJAX functionality.
- **jQuery:** JavaScript library used for DOM manipulation, event handling, animation effects, and AJAX interactions.
- **Chart.js:** A JavaScript charting library for creating interactive and customizable charts, graphs, and data visualizations.

### Database:

- **SQLite:** Lightweight, serverless, and easy-to-use relational database management system suitable for development and small-scale applications.

## Installation

Follow these steps to set up and run the CrowdFunding WebApp project on your local machine.

### Prerequisites:

- Python (version 3.7 or higher)
- Pip (Python package manager)
- Virtualenv (optional but recommended for environment isolation)
- Git (version control system)

### Setup Instructions:

1. Clone the repository to your local machine using Git:
   ```bash
   https://github.com/sh-osama-sami/CrowdFundingApp.git
   ```

2. Navigate to the project directory:
   ```bash
   cd crowdfunding-webapp
   ```

3. Create and activate a virtual environment (optional but recommended):
   ```bash
   virtualenv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate  # For Windows
   ```

4. Install project dependencies using Pip:
   ```bash
   pip install -r requirements.txt
   ```

5. Perform database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser for admin access

:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application in your web browser at `http://localhost:8000/`.

## Usage

### User Actions:

1. **Registration:**
   - Navigate to the registration page and create a new user account.
   - Verify your email address to activate your account.

2. **Login:**
   - Enter your credentials to log in to your account.

3. **Project Creation:**
   - As a logged-in user, access the project creation form to submit a new crowdfunding project.

4. **Project Support:**
   - Explore existing projects, select a project of interest, and support it by making a donation.

5. **Profile Management:**
   - View and update your profile information, including account details and project contributions.

### Admin Actions:

1. **Administrative Access:**
   - Log in with the superuser credentials to access the admin dashboard.

2. **Content Management:**
   - Manage categories, tags, projects, user accounts, and content moderation activities.

3. **Analytics and Reporting:**
   - Analyze project data, user engagement metrics, financial reports, and crowdfunding trends.

## Project Structure

The project directory structure is organized as follows:

- **crowdfunding_webapp:** Main project directory containing Django settings, URLs, and configuration files.
- **users:** App for user authentication, profile management, and user-related functionalities.
- **projects:** App for managing crowdfunding projects, project listings, support actions, and project-related features.
- **categories:** App for managing project categories, tags, and category-specific functionalities.
- **templates:** HTML templates for rendering frontend views and user interfaces.
- **static:** Static files such as CSS stylesheets, JavaScript scripts, images, and media assets.

## Contributing

Contributions to the CrowdFunding WebApp project are highly encouraged and appreciated! Here's how you can contribute:

### Getting Started:

1. Fork the project repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your changes (`git checkout -b feature/new-feature`).
4. Make your modifications, add new features, fix bugs, or improve documentation.

### Submitting Changes:

1. Commit your changes to the new branch (`git commit -am 'Add new feature'`).
2. Push your changes to your forked repository on GitHub (`git push origin feature/new-feature`).
3. Create a new Pull Request (PR) from your branch to the main project repository.


## Project Team

The CrowdFunding WebApp project was developed by a team of five members, each contributing to different aspects of the project:

1. 
2. 
3. 
4. 
5. 

## License

The CrowdFunding WebApp project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
