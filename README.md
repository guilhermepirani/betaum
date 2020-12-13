<h1 style="text-align: center; font-weight: Bold">
    CS50 Final Project
</h1>


###### [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> This website was develloped as my final project for HarvardX CS50 class. 

## :dollar: **Betaum**

Betaum is a platform where friends can quickly set up bets, keep track of them and challange others. 

<h2 align="center">Used Technologies</h2>

- [Flask](https://flask.palletsprojects.com)
- [SQLite](https://www.sqlite.org/index.html)
- [HTML](https://html.com/)
- [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS)
- [Bootstrap](https://getbootstrap.com/)
- [Jinja](https://jinja.palletsprojects.com/)
- [JavaScript](https://www.javascript.com/)

### Login & Index:

<div style="text-align: justify">
<p> 
Pretty straight forward, as landing page you get prompted to login and then moved to the index page. There you can see a carousel with up to the closest 3 bets you have comming. If you have no bets to display, a template is displayed instead.
Your profile picture on the top right opens a nav menu to the other pages.
<p>
    
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/login%20page.png" width="25%" height="25%" alt="Login page"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/Index.png" width="25%" height="25%" alt="index page"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/navw%20menu.png" width="25%" height="25%" alt="nav menu"/>
</div>

### Profiles & Settings

<div style="text-align: justify">
<p>
When loading profile pages, the website renders some different options depending if you're seeing your profile, a friend's profile, or another random person's profile.
For your own profile, you're given the options to see your friend list, which is a default option in all profiles you enter, you have the Me! button here in place of Friend or Add Friend, and being exclusive to when seeing your own profile, the settings button.
Inside settings you have two options that open modals, you to change your password and other to change your profile picture, with a cool preview before uploading. When registering you're set with a default profile picture.
</p>

<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/my%20profile.png" width="23%" height="23%" alt="My profile"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/change%20pic.png" width="23%" height="23%" alt="Change pic"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/Seeing%20other%20Profile.png" width="23%" height="23%" alt="other's profile"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/Profile%20friend%20modal.png" width="23%" height="23%" alt="profile friend modal"/>
</div>

### Friends List & Friend Requests

<div style="text-align: justify">
<p>
Inside your friends page you have a list of all your added friends, in alphabetical order, and a session with all friend requests you received.
</p>

<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/friend%20list.png" width="25%" height="25%" alt="friend list"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/Friend%20requests.png" width="25%" height="25%" alt="friend request"/>
</div>

### Creating a Bet

<div style="text-align: justify">
<p>
As you can see, there's some fron-end checks to make sure the form is submitted correctly, most of the form is also checked in the back-end and the fields that allow blank input  have default options set for them. You can invite your friends here through the dropdown menu. You automatically join all bets that you start. If you don't upload a bet image there's a default one that will be shown.
</p>

<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/new%20bet%20blank.png" width="25%" height="25%" alt="new bet blank"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/new%20bet%20filled.png" width="25%" height="25%" alt="new bet filled"/>
</div>

### My Bets & Bet Pages

<div style="text-align: justify">
<p>
Clicking on My Bets you're sent to a page showing all bets you joined, ordered by nearest first. There's a search box that filter searchs by the bet title, and past bets are sent to the bottom, as a second list equally ordered, and colored dark red.
Inside the other menu option are listed all bet invites you received that are still running.
</p>

<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/my%20bets.png" width="25%" height="25%" alt="my bets page"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/my%20bets%20invites.png" width="25%" height="25%" alt="bet invites"/>
</div>

<div style="text-align: justify">
<p>
When you open a bet you can see all of it's information stored in the database. There are lists for user's that joined and where invited. You can jump to their profiles by clicking on their avatars. In this page if you're the bet owner you'll see the edit button, which opens a modal to edit or delete the bet's info. Other users will se a join or invite button depending if they were invited or joined the bet.
</p>

<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/bet%20page%20index.png" width="25%" height="25%" alt="new bet blank"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/bet%20page%20modal%20edit.png" width="25%" height="25%" alt="new bet filled"/>
<img src="https://github.com/guilhermepirani/betaum/blob/main/static/samples/bet%20page%20modal%20invite.png" width="25%" height="25%" alt="new bet filled"/>
</div>

<h2 align="center">Challenges and Learnings</h2>

<p>
This project was a blast! Working part time on it for three weeks I can say that it challanged me. Researching for every function that I thought to implement was a learning of its own. I have learned something new for each page that I built, if not many things for page. I tried to get the project as close to deployable that I could inside the timeline that I set for myself. That challanged me to think what could go wrong and what could function better in every entry that I did. For example, functions that delete unused images to save space or change file extension from images, several form input checks and understanding and formating returns from inbuilt functions that I had never used before and were not that straight forward.
</p>

<h2 align="center">Considerations</h2>

- Layout was based on mobile, but works fine on desktop browsers.
- I had many other ideas to implement, but considering the time needed to learn & apply I'm submitting it as it is. Maybe in the future I can get it to deploy stage.

<h2 align="center">How to Use</h2>

   ```
   - Clone this repository:
   $ git clone https://github.com/guilhermepirani/betaum.git

   - Navigate to repository and install requirements:
   $ pip install -r requirements.txt

   - Execute application:
   $ flask run

   ```

Thank you for reading!