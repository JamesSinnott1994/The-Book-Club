# The Book Club

The purpose of this project is to build a book review and recommendation site.

## Table of Contents
- [User Experience](#user-experience)
    - [Strategy](#strategy)
        - [User Stories](#user-stories)
        - [Project Goal](#project-goal)
        - [Strategy Tradeoffs](#strategy-tradeoffs)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Skeleton](#skeleton)
    - [Surface](#surface)
        - [Typography](#typography)
        - [Colour Scheme](#colour-scheme)
        - [Media](#media)
        - [Effects](#effects)
- [Technologies](#technologies)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

---
## User Experience

### Strategy

#### User Stories
As a **first-time visitor**, I want:

1. To see a visually appealing website.
2. The website to be intuitive and simple to use.
3. To be able to browse through the books on the site.
4. To be able to search for books by name.
5. To be able to purchase books from the site.
6. To be able to Register as a User on the site.
7. To be able to get visual feedback when an action is completed.
8. To be able to contact the Site Owner for any queries.


As a **returning signed-up user**, in addition to the above, I want:

1. To be able to login to the site.
2. To be able to add books and their details.
3. To be able to view books that you added.
4. To be able to write reviews about any book.
5. To be able to edit details of books and reviews you added.
6. To be able to delete details of books and reviews you added.


As the **site owner**, I want:

1. To earn money on each book purchased on the site via a link from the site.
2. To have the ability as Administrator to remove any books and reviews added by users of the site.
3. To create a website that looks well on different devices and screen sizes.
4. To provide a visually appealing and intuitive website for users.
5. To provide details for users to contact me if they need help with a query.

#### Project Goal
- Project goal:
    - The goal of this project is to build a Full-Stack website that allows users to manage a common dataset about a particular domain.

- Focus:
    - The main focus of this project is to create a visually appealing and intuitive Full-Stack website that allows users to find, review and upload books that they would like to read.

- Definition:
    - I am creating a Full-Stack web application, using HTML, CSS, JavaScript, Python, Flask & MongoDB.

- Value:
    - The value this project will provide, is that it will showcase to future employers my ability to piece together a Full-Stack website, demonstrating proficiency in using HTML, CSS, JavaScript, Python, Flask and MongoDB.
    - The value for users of the application is that it will allow them to search for books, and indeed it will allow them to contribute to and expand the website by adding books of their own.
    - The value for a possible site owner, is that it will allow them to earn money on each book purchased via a link from the site.

#### Strategy Tradeoffs

Opportunity/Problem | Importance (1-5) | Viability/Feasibility (1-5)
:-------- |:--------:|:--------:
Search Feature | 5 | 3
Add Book | 5 | 4
Edit Book | 4 | 4
Delete Book | 4 | 4
Add Review | 4 | 4
Edit Review | 3 | 4
Delete Review | 3 | 4
Register | 5 | 4
Log in | 5 | 4
Log out | 4 | 4
Contact | 3 | 5
Purchase | 4 | 5
Site Analytics | 1 | 1

### Scope
- Main features (For Minimal Viable Product)
    - Navigation Menu
    - Pagination for Books page
    - Search Functionality
    - Call to action Register area on landing page
    - Register
    - Log in
    - Log out
    - User Profile page 
    - User can Add/Edit/Delete Books
    - User can Add/Edit/Delete Reviews
    - Administrator can delete Users and their content
    - Contact Form
    - Visual feedback for users on their actions
    - Fully responsive website
    - Purchase
    - 404 Error page

- Secondary / Future Features:
    - Site Analytics Page
    - User Favourites Page
    - View most popular books
    - Username/Password retrieval
    - Chatbot Functionality

### Structure
A different website structure appears depending on whether a user is logged in or not.

#### Structure when not logged in
1. Home Page
- Will display a Navigation bar along the top of the screen (Common to all pages). This will contain the site Logo as well as the following link elements:
    - Home
    - Books
    - Contact
    - Search Icon
    - Login
    - Register
    
- Will contain a Search Area below the navigation bar.
- Will contain a Call-To-Action register button below the search area on the left.
- Will contain a "View Library" button below the search area on the right.
- Will show the most popular books.
- Will show some quotes about reading.
- Will display a footer on the bottom (which will be common across all pages) that contains copyright information, contact details, as well as links to the administrator's social media.
2. Books Page
- This page will display a list of all books on the site. Pagination will be used to control the number of books shown to the user.
- When user clicks on a particular book, it will bring them to a page which contains all the details for that book.
3. Book Page
- Display details for a particular book.
4. Search Page
- Returns results (if any) of books for the search query submitted by the user.
- Will be similar to the Books page.
5. Login Page
- Simple login form for the user.
6. Register Page
- Simple register form for the user.
7. Contact Page
- Form that will allow users to contact the site administrator for any queries.

#### Structure when logged in
1. Home Page
- Similar to above but with the following link elements for a logged in user:
    - Home
    - Profile
    - Add Book
    - Books
    - Contact
    - Search Icon
    - Logout
- Call-To-Action register button described above will be replaced by an "Add Book" button for logged in users.
2. Profile Page
- Displays information about the user.
- Shows books added by the user.
3. Add Book Page
- Will display a form that allows the user to enter information about a book they would like to add to the website.
4. Books Page
- Same as previously described.
5. Book Page
- Same as previously described.
6. Search Page
- Same as previously described.
7. Contact Page
- Same as previously described.