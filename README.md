#Game-Design_Udacity
This is the fourth project for Full Nanodegree in which the game of hangman is designed.

In this project, the cloud-based APIs are developed to support a provided conference organization application that exists on the web as well as a native Android application. Google Cloud Endpoints with Python is used to realize the API backend on Google APP Engine.

The website is deployed on Google Cloud Platform:   https://hangman-1278.appspot.com/

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
2.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
3.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.
 
##Game Description:
Hangman is a simple traditional game where you are given 9 attempts to guess 
the secret letters in of the hidden word. Each time an attempt fails, another piece 
of the hanging body is drawn, each time you are correct you have one less letter to 
guess. The front end of the game using the backend would draw the relevant hangman 
picture and also show what blanks are filled in plus how many attempts left. 
The game has a simple dictionary for demo purposes of 9 words which could be scaled up 
or linked to another library to broaden the game's difficulty.
Many hangman games can be played by many different Users at any
given time. Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

[Full description of hangman- wikipaedia](https://en.wikipedia.org/wiki/Hangman_(game)

##Files Included:
 - application.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a user with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, min, max, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Min must be less than
    max. Also adds a task to a task queue to update the average moves remaining
    for active games.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new state of game.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.
    
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores saved in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the user does not exist.
    
 - **get_average_attempts_remaining**
    - Path: 'games/average_attempts'
    - Method: GET
    - Parameters: None
    - Returns: StringMessage
    - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.
    
 - **get_user_games**
    - Path: 'user/games'
    - Method :GET
    - Parameters: user_name
    - Returns : All games from one user that are active and not finished
    - This returns all of a user's active games.
    
 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}',
    - Method :DELETE
    - Parameters: urlsafe_game_key
    - Returns : All games from one user that are active and not finished
    - This endpoint allows users to cancel a game in progress, completed games cannot be removed.
    
 - **get_high_scores**
    - Path: 'high_scores'
    - Method :GET
    - Parameters: no of records to show (records) field
    - Returns : All scores graded out by wins first then graded by least amount of attempts to win.
    
 - **get_user_rankings**
    - Path: 'high_scores'
    - Method :GET
    - Parameters: none 
    - Returns : Players that have played games displayed by ranking (win ratio)
    - Come up with a method for ranking the performance of each player.
      
 - **get_game_history**
    - Path: game/{urlsafe_game_key}/history
    - Method :GET
    - Parameters: urlsafe_game_key
    - Returns : History of a game move by move 
   
##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name).
    **GameForms**
    - Multiple UserFrom container
 - **NewGameForm**
    - Used to create a new game (user_name, min, max, attempts)
 - **MakeMoveForm**
    - Inbound make move form (guess).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.
 - **UserForm**
    - Outbound user representation form
 - **UserForms**
    - Multiple UserFrom container

##Api Test Instruction
The endpoints function are tested using Api Explorer by visiting http://hangman-1278.appspot.com/_ah/api/explorer. The Backend Apis are:
![1](https://lh5.googleusercontent.com/-uy8zE_ubEbw/VxVUloWLyNI/AAAAAAAAAEo/4GWQo3aogOcD02KMVax0CXmn3NGrI6-SACL0B/w1832-h696-no/Backend%2BAPIs.tiff)

