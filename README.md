# movie-website
#### Note: Account data and comment data will be stored in JSON files, while movie details data will be stored in a CSV file.
<hr>
A movie website developed with React, Python, and FastAPI, storing data in JSON file format, and integrating AI for sentiment analysis of reviews and a movie recommendation system.

<br><hr><br>

## Here's the breakdown of the scope for designing or developing the program:
1. Account registration system (ID and password).
2. Login system (required for commenting or viewing movie details).
3. Commenting system, with analysis to determine whether comments are positive or negative.
4. Ability to delete or edit comments.
5. Data storage for accounts (passwords encrypted), movie details, and comments.
6. Upon logging in, when returning to the homepage (/), the recommended movies section will display movies similar to those previously viewed.
7. For users who haven't logged in or haven't viewed any movie details, the movie section will display based on popularity (number of views).
8. Logout system (after logging out, if logging back into the same account, comment and movie recommendation data remain).
9. Ability to edit and delete comments only by the account owner.
10. Option to filter and display only positive or negative comments.
11. Movie search system (users can log out to view search results).
12. Login time limit of 60 minutes. After this, users cannot comment or view movie details but can log in again (time limit can be adjusted in the code).
