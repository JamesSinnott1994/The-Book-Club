## Testing

Back to [Readme file.](README.md)

## Table of Contents
- [Functionality Testing](#functionality-testing)
- [Browser Compatability](#browser-compatability)
- [Code Validation](#code-validation)
- [Performance Testing](#performance-testing)
- [User Stories Testing](#user-stories-testing)
- [Bugs](#bugs)

---
### Browser Compatability

- I tested the appearance and responsiveness of the website across many different devices and browsers. Generally, the appearance and responsiveness looks quite good on the different devices, and there is no difference between the browsers.

- Browsers tested:
    - Brave
    - Chrome
    - Firefox
    - Microsoft Edge
- Devices tested:
    - Windows laptop
    - iPad
    - Android Phone
- Devices tested in DevTools:
    - Moto G4
    - iPhone 6/7/8
    - iPad
- Custom responsive viewport sizes created for testing on larger screens than my laptop:
    - 1280px x 802px (Larger laptop)
    - 1600px x 992px (Desktop)

---
### Code Validation

#### 1. Testing HTML with [The W3C Markup Validation Service](https://validator.w3.org/)

- Home page:
    - No errors. Two minor warnings about sections lacking a heading. These are warning are not an issue and can be safely ignored.

- Add Book page:
    - No errors. 1 similar warning to above.

- Book page:
    - No errors. 2 warnings similar to above.

- Books page:
    - ![Books Validator](readme-images/books-validator.png)
    - 8 errors were discovered as I forgot to add the "alt" attribute to the img element.

- Edit Book page:
    - ![Edit Book Validator](readme-images/edit-book-validator.png)

    - The error above was given when this page was put through the validator.
    - Solution was to remove the following line of unneccesary code from the page:
        - `<option value="" disabled selected>Choose your genre</option>`

- Contact/Login/Register page:
    - No errors on the three pages. 1 Section lacking a heading warning for each.

#### 2. Testing CSS with the [Jigsaw CSS Validation Service ](https://jigsaw.w3.org/css-validator/)
- There was 1 error relating to the value for the font-weight:
![CSS Error](readme-images/css-error.png)

- Warnings were also discovered, but these relate mainly to "unknown vendor extensions", which can be safely ignored.

#### 3. Testing JavaScript with [JSHint](https://jshint.com/)

- When I Initially put my app.js code into JSHint, I was given 17 warnings:

![JSHint-Warning-One](readme-images/jshint-warnings.png)

- As can be seen from the image above, most of the warnings related to ES6's `let` keywords.
    - This is a minor warning. The solution to get rid of the warning was to add the following comment to the top of the app.js file:
        - /*jshint esversion: 6 */
    - This had the affect of reducing the warnings from 17 to 1.

- The remaining warning was about a missing semi-colon, which was easily fixed.

- JSHint also had an issue with undefined variable '$', used for jQuery. The solution was to put the following at the top of the app.js file:
    - /*globals $:false */

#### 4. Testing Python with [PEP8 online](http://pep8online.com/)

- When I initially put my app.py code into the PEP8 validator, I was given 2 minor issues:

![PEP8-Issues](readme-images/pep8-issues.png)

- This was in relation to the following code:

    - "$skip": (
            pagination_data["BOOKS_PER_PAGE"]
            * (pagination_data["offset"] + int(page))
        )

- Solution was simply to move the multiply operator '*' back to the first line:

    - "$skip": (
            pagination_data["BOOKS_PER_PAGE"] *
            (pagination_data["offset"] + int(page))
        )

---
### Performance Testing

Testing page with Lighthouse in Chrome Dev Tools to optimise performance, accessibility, best practices and SEO

#### Desktop Performance

- **Lighthouse Desktop Home page report**:
    - As can be seen from the image below, performance was excellent.
    - Accessibiltiy was improved from it's original score of 84 by the following actions: 
        - Adding an aria-label to the button element which contained the search icon. It needed a name.
        - Adding aria-labels to the social media links.
    - Best Practices was improved from it's original score of 87 by:
        - Adding the 'rel="noopener"' to the external links i.e. Buy & Social media buttons.
    - SEO was improved by:
        - Adding a `<meta name="description">` element, which describes what the website is all about.

![Lighthouse Desktop Home Page Report](readme-images/performance-screenshots/home-desktop.JPG)

- **Lighthouse Desktop Home page report Improvements**:

    - As can be seen from the image below, the solutions above led to major improvements for the Home page and indeed for every page on the website.

![Lighthouse Desktop Home Page Improvement Report](readme-images/performance-screenshots/home-desktop-improvement.JPG)

- **Lighthouse Desktop report for the Books, Book, Contact, Login, Register pages** had roughly the same scores as for the Home page and therefore solutions were the same.
    - Performance was slightly worse on Books because of more Book images being shown.

- **Lighthouse Desktop Profile page report**:
    - As can be seen from image below, Best Practices was 80. This was because when a user logs in to the app, it can sometimes disable the HTTPS.

![Lighthouse Desktop Profile Page Report](readme-images/performance-screenshots/profile-desktop.JPG)

#### Mobile Performance

- **Lighthouse Mobile Home page report**:

    - Performance and Best practices was improved on mobile by re-sizing the images for George RR Martin and Mark Twain i.e making them smaller.
    - Unfortunately nothing could be done about the book images as they are taken from other sources on the internet and therefore I could not make them smaller myself before they are resized and loaded on the website.

![Lighthouse Mobile Home Page Report](readme-images/performance-screenshots/home-mobile.JPG)

- **Lighthouse Mobile report for the Books, Book, Contact, Login, Register** pages had roughly the same scores as for the Home page and therefore solutions were the same.
    - Performance was slightly worse on Books because of more Book images being shown.

- **Lighthouse Mobile Profile page report**:
    - Images affected performance worse on mobile.

![Lighthouse Mobile Profile Page Report](readme-images/performance-screenshots/profile-mobile.JPG)

---
### User Stories Testing

As a **first-time player**, I want:
1. To see a visually appealing website.

- The website looks visually appealing, with attractive book covers, author images, colour contrasts, and a nice colour scheme. The main purple background colour exudes feelings of royalty, high quality, and intrigue.

![Visual Appeal](readme-images/user-story-screenshots/visual-appeal.png)

2. The website to be intuitive and simple to use.

- The main navigation bar makes the website intuitive and easy to use.

![Intuitive](readme-images/user-story-screenshots/intuitive.png)

3. To be able to browse through the books on the site.

- User can browse through books on the Books page.

![Browse](readme-images/user-story-screenshots/browse.png)

4. To be able to search for books by name.

- User can search for books by name through the search bar on the home page and also through the search bar in the navigation bar.

![Search](readme-images/user-story-screenshots/search.png)

5. To be able to purchase books from the site.

- "Buy" button on a Book page would enable user to buy a book (Directs to Amazon).

![Purchase](readme-images/user-story-screenshots/purchase.png)

6. To be able to Register as a User on the site.

- User can register an account through the Register form

![Register](readme-images/user-story-screenshots/register.png)

7. To be able to get visual feedback when an action is completed.

- Flash message give user visual feedback on their actions.

![Flash](readme-images/user-story-screenshots/flash.png)

8. To be able to contact the Site Owner for any queries.

- Users can contact site owner through the form on the Contact page.

![Contact](readme-images/user-story-screenshots/contact.png)

As a **returning signed-up user**, in addition to the above, I want:

1. To be able to login to the site.

- User can login through the form on the Login page.

![Login](readme-images/user-story-screenshots/login.png)

2. To be able to add books and their details.

- This can be done from the form on the Add Book page.

![Add Book](readme-images/user-story-screenshots/add-book.png)

3. To be able to view books that you added.

- User can see their books from the Profile page.

![Profile](readme-images/user-story-screenshots/profile.png)

4. To be able to write reviews about any book.

- Can be done from the Add Review form on a Book's page.

![Add Review](readme-images/user-story-screenshots/add-review.png)

5. To be able to edit details of books and reviews you added.

- Can edit book details by clicking the "Edit" button located beside the "Buy" button. This brings user to the Edit Book page.

![Edit Book](readme-images/user-story-screenshots/edit-book.png)

- Can edit review by clicking the "Edit" button beside your review. Brings you up to the Edit Review form.

![Edit Review](readme-images/user-story-screenshots/edit-review.png)
 
6. To be able to delete details of books and reviews you added.

- User can delete books and reviews that belong to them by clicking the "Delete" button and then clicking "Yes" in the modal window.

![Delete](readme-images/user-story-screenshots/delete.png)

As the **site owner**, I want:

1. To earn money on each book purchased on the site via a link from the site.

- See image containing "Buy" button above.

2. To have the ability as Administrator to remove any books and reviews added by users of the site.

- Administrator has the right to delete all books and reviews on the site. (For image below I am logged in as Administrator and as can be seen can delete both reviews by different users).

![Admin](readme-images/user-story-screenshots/admin.png)

3. To create a website that looks well on different devices and screen sizes.

- The website is responsive and looks well on different devices and screen sizes.

![IPAD](readme-images/user-story-screenshots/ipad.png)

![Mobile](readme-images/user-story-screenshots/mobile.png)

4. To provide a visually appealing and intuitive website for users.

- See visually appealing image mentioned above.

5. To provide details for users to contact me if they need help with a query.

- See Contact form image above.

---
## Bugs

**Bug:** There was an issue whereby books were not displaying in the correct order on the Books page. For example, if there were five books displayed from left to right (with 4 books per line), then the 5th book would not appear in the left-most position of it's line.

**Fix:** The reason for this was because of the different heights of the Book divs. The solution was to use JavaScript to make each book div equal to the height of the longest div.

Aside from the above, there were no more real bugs. Mainly there was just a lot of refactoring.