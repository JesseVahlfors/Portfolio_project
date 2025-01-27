# Journal

## Basic vision

- I am making a portfolio website with django that has portfolio projects as django apps
- I will also make a restful API that uses the same database
- Make some portfolio projects utilizing React and the API as well

## Journal Entry - 2025-01-10

    ### Tasks Done

    - Initialized the django project.

    - Setup postgres database.

    - Created Apps home and JSON_Parser.

    - Created first test for a basic view and made the view to pass.

    ### Challenges

    - During setup i took a lot of time to configure postgres. Had a hiccup with it when making the first test as well. Needed to find out how to make a test database for the tests.

    ### Next Steps

    - Now that i should have the project (as far as i know) ready. I should be able to start the next part.

    - I will implement a "walking skeleton" technique from TDD. To do that i will implement displaying my projects on the home page. That will include frontend-backend-database.

## Journal Entry - 2025-01-12

    ### Tasks Done

    - Added Main and Profile views

    - Added tests for both views including the walking skeleton end to end test

    - Added root template base.html for basic structure and home templates main_page and profile for their own views.

    - Added favicon

    - Added Profile model to admin and added my profile info to the database.

    ### Challenges
    
    - I had some issues with the file pathing the templates. I had to try a few times till i finally found the correct way to chain them together.

    ### Next Steps

    - Next i will implement the list view for portfolio projects and i need to figure out if i do a detail view or just a link to a new app...
    
    - I have a vision of making most projects an app that i can open from the portfolio website

## Journal Entry - 2025-01-13

    ### Tasks Done

    - Made project list page that includes tests, views, template, and a new model for projects

    - Added project to admin so i can easily add new ones.

    - populated profile and project objects with info and pictures so i can style the page after i bring in tailwind css    

    ### Challenges
    
    - Struggled a bit with images loading, because they didnt have correct settings defined and a missing character in a template
    
    - 6 tests also failed after, because i had an if conditional to check in the template if an image exists. 
    The condition was "if profile.image.url exists" which would error, because if there is no image you can't check the .url. 
    Taking out the .url fixed all the failed tests.

    ### Next Steps

    - I think i have the barebones now so i want to style the existing pages

    - With plain css i've had trouble making pages look decent so i want to try another angle

    - I will do a coursera tailwind css course and apply what i learn there after completion

## Journal Entry - 2025-01-19

    ### Tasks Done

    -Initialized Tailwind CSS for django with django-tailwind.

    -Started base.html template styling with header and footer styles including a nav dropdown menu for small screens

    ### Challenges
    
    - Installing and setting up django tailwind took a lot of time. A lot of setup and installing node.js for tailwind somehow messed with my python installation so i needed to reinstall it too and reinstall the project requirements from the requirements.txt.
    After initial struggles the actual styling with tailwind has been a breeze.

    ### Next Steps

    -Next i need to make basic styling to the home, projects and about me templates.

## Journal Entry - 2025-01-25

    ### Tasks Done

    - Styled the main_page

    - Implemented the email contact form 

    - Added a profile image resizing to reduce image size. Helps the page load faster not having a huge high resolution picture rendering in a small element.

    - Added some missing descriptions and aria labels to html elements to stisfy some lighthouse accessibility and SEO suggestions. 

    ### Challenges

    - While implementing the email form had some struggles on making it all work like it should. in the end it was mostly a missing action on the form html tag and the address i needed the page to return to after submitting the form.

    - Also styling has taken time exploring how to make eveything look fine.

    ### Next Steps

    - I need to think about if i want to improve the email contact form by making it asynchronous so it wouldnt trigger a full page reload. It would need a ajax implementation and a bunch of code. 
    I'll add it as a toDo and think about it after get the full website built.

    - I need to make the project detail page next. this should be the last view i need for now. I have a projectlist view as well, but i wont need that until i have more than 4 projects.
