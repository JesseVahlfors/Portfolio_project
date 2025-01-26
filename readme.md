# Portfolio Website

This project is a personal portfolio website built to showcase my past and current projects. It provides an accessible and easy-to-navigate platform where visitors can explore my work and understand my development skills.
It is heavily inspired by Ram Maheshwari's Dopefolio project. Check him out at https://www.rammaheshwari.com/

## Table of Contents

- [Technology Stack & Rationale](#technology-stack--rationale)
- [Development Process & Challenges](#development-process--challenges)
- [Key Features & Functionality](#key-features--functionality)
- [Future Enhancements](#future-enhancements)
- [Why This Project?](#why-this-project)
- [Installation](#installation)
- [Usage](#usage)

## Technology Stack & Rationale

For this project, I carefully selected the following technologies based on their ability to meet the project's needs in terms of scalability, performance, and ease of use:

- **Django**: After completing university courses on Python, I was eager to apply my growing proficiency with the language. Django was selected for its robust backend structure, which allows easy management of future projects and scaling. Django’s security features and admin panel also make it ideal for managing content.
- **Tailwind CSS**: I learned Tailwind specifically for this project. Its utility-first approach to styling allowed me to write concise, reusable classes directly within the HTML templates. This made it simple to rapidly develop and customize the layout.
- **PostgreSQL**: Chosen for its strong support for relational data and seamless integration with Django’s ORM, PostgreSQL allowed me to efficiently set up the backend for data storage and scalability.

## Development Process & Challenges

During the development of this project, I faced several challenges, each of which contributed to my growth as a developer:

1. **Database Setup & Permissions**: I had to learn about database structure and user permissions to effectively work with PostgreSQL and Django’s ORM. This involved reading extensive documentation and troubleshooting errors.
2. **Django-Tailwind Setup**: Setting up the integration between Django and Tailwind took time, particularly dealing with installation conflicts between Node.js and Python. Reinstalling Python and project dependencies resolved these issues.
3. **Email Contact Form**: Setting up the email form required troubleshooting missing configurations, such as form actions and redirects, along with configuring the email sending process.

These challenges helped me refine my problem-solving skills and gain a deeper understanding of Django’s systems.

## Key Features & Functionality

- Built with HTML, Tailwind CSS, and minimal JavaScript for optimal performance.
- Fully responsive design to provide seamless user experiences on both mobile and desktop.
- Database-driven backend using PostgreSQL to store and manage future projects and their data.

## Future Enhancements

While the current version of the portfolio is complete, I plan to add the following enhancements:

- **Expanded Project Display**: More projects will be added over time, with dynamic displays of each project stored in the database.
- **Restful API**: I plan to develop a Restful API to serve as the backend for future React frontend projects, providing greater flexibility and scalability.

## Why This Project?

I chose to work on this project because I needed a platform to showcase my work in a live environment. This portfolio serves as a central hub for displaying my full-stack development skills and provides a solid foundation for future projects.

## Installation

1. Clone this repository:

   git clone https://github.com/your-username/portfolio-website.git

2. Navigate to the project directory:

    cd portfolio-website

3. Install the required dependencies:

    pip install -r requirements.txt

4. Set up the database:

    python manage.py migrate

5. Start the development server:

    python manage.py runserver

6. Visit http://127.0.0.1:8000/ in your browser to view the portfolio.

Usage

This portfolio website will automatically display your projects in a grid layout, showcasing each project with basic descriptions. You can add or modify your projects through Django’s admin panel after setting up the database.

To add a new project, log into the admin panel at http://127.0.0.1:8000/admin/ and add the project details.