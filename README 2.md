Curious Cook: Recipe Web Application

Project Description:
Cookbook is a personal recipe application I built to share my creations and experiment with new dishes. As a passionate cook, I wanted to create a platform where users can explore, save, and vote on their favorite recipes. The app lets users browse recipes, search by category. Users can also create accounts to save their favorite recipes to a personal collection. Also, the site features a dynamic "Top 5" list of trending recipes, which updates based on user votes.

Distinctiveness and Complexity:
This project stands out because it combines Django, Python and JavaScript to make a dynamic, interactive app. Unlike static pages, social networks, or e-commerce sites, Curious Cook is a personal recipe blog with unique features.

Although the app allows users to save and vote on recipes, it is not an e-commerce platform. There are no monetary transactions involved, and users do not buy or sell anything. The main focus is on recipe exploration and interaction, not purchasing or commercial exchanges. This makes it distinct from e-commerce projects, which often require payment functionality or product transactions.

One of the main challenges was making the app interactive. For example, when users save or vote for a recipe, the page updates without reloading. I used JavaScript’s fetch API to send data to the backend, update the database, and change the save/vote button images—in real-time. This required connecting the frontend and backend smoothly, which was tricky.

Another big challenge was linking recipe cards to their specific recipe pages. I created a connection where each recipe has a filename in the database that matches its template file. When a user clicks on a recipe, the app automatically loads the right page. It makes adding new recipes easy because all I need to do is add the new recipe data, and the app knows where to put it.
Also, I used the mailto: link in the contact form so that when users submit it, it opens their email app to send me a message. This way, instead of using a POST method, users can easily email me directly.

These challenges made the project more complex than the others in the course. It’s not just a basic app, but a system where the frontend and backend work together, making the experience dynamic and easy to expand.


Project Files and Structure
layout.html: Basic structure of the website.
index.html: Homepage displays recipe cards from the database, with recipe title, image, and vote count.
login.html: User login page.
register.html: User registration page.
recipe.html: Template that displays the structure of a recipe, list of top 5, and buttons to save or vote.
Various recipe pages: These extend the recipe.html template and display the content of each recipe.
category.html: Displays recipe cards of a specific category, similar to the homepage but filtered.
saved.html: Displays saved recipes for logged-in users.
top.html: Shows the "Top 5" recipes, dynamically updated based on user votes.
search.html: Displays search results based on user input.
models.py: Contains the database models for users, categories, and cards.
views.py: Contains the functions that control the logic for each page.
urls.py: Contains the PATHs for the app, linking pages and actions.
static: Contains static files like images and CSS


How to Run the Application
I used Python3 and Django, just like in the course projects. There are no special configurations — set up the environment, run migrations to create the database, and create a superuser for admin access. After that, start the server, and it will run locally,

Additional Information
I’ve used Django’s built-in User model for authentication and created custom models for categories and recipes. I also implemented JavaScript’s fetch API to save and vote on recipes without reloading the page, keeping the app interactive. The navbar stays at the top while scrolling, and the design is mobile-friendly to ensure a smooth experience on any device.
This project showcases the integration of both backend and frontend technologies to create a functional and dynamic recipe platform.

