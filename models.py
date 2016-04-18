"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. There are three entities used in this project, 
namely User, Game and Score."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    wins = ndb.IntegerProperty(default=0)
    total_games_played = ndb.IntegerProperty(default=0)

    """Adding an auto calculated field"""
    @classmethod
    def win_percentage(self):
        if self.total_games_played >0:
            return float(self.wins)/float(self.total_played)
        else:
            return 0
    def to_user_form(self):
        """Copy user information to form"""
        return UserForm(name=self.name,
                        email=self.email,
                        wins=self.wins,
                        total_games_played=self.total_played,
                        win_percentage=self.win_percentage)
    def add_win(self):
        """records the victory to the player"""
        self.wins += 1
        self.total_games_played +=1
        self.put()

    def add_loss(self):
        """ records a loss to the player"""
        self.total_games_played +=1
        self.put()


class Game(ndb.Model):
    """Game object"""
    word_to_guess = ndb.StringProperty(required=True)
    letters_guessed = ndb.StringProperty(required=True, default='')
    attempts_allowed = ndb.IntegerProperty(required=True, default=9)
    attempts_remaining = ndb.IntegerProperty(required=True, default=9)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    history = ndb.PickleProperty(required=True, default=[])

    @classmethod
    def new_game(cls,user,attempts):
        """Creates and returns a new game"""
        # List of words to choose ad the original word. This list can be external library or given words list.
        words_to_guess = ["beautiful","extraordinary","spectacular","mountain","fabulous","wonderful"]
        # pick a number to choose from the words
        number = random.randint(0,5)
        word_to_guess = str(words_to_guess[number])
        attempts_default = 9
        game = Game(user=user,
                    word_to_guess=word_to_guess,
                    letters_guessed='',
                    history=[],
                    attempts_allowed=attempts_default,
                    attempts_remaining=attempts_default,
                    game_over=False)
        game.put()
        return game
    def to_game_form(self,message):
        """Returns a GameForm representation of the Game"""
        return GameForm(urlsafe_key = self.key.urlsafe(),
			user_name = self.user.get().name,
			letters_guessed = self.letters_guessed,
			attempts_remaining = self.attempts_remaining,
			game_over = self.game_over,
			message = message)

    def end_game(self, won):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score board
        score = Score(user=self.user, date=date.today(), won=won,
                      guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()
        # Update the winner
        if won == True:
            self.user.get().add_win()
        elif won == False:
            self.user.get().add_loss()

class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    guesses = ndb.IntegerProperty(required=True)
    
    def to_score_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), guesses=self.guesses)


class GameForm(messages.Message):
    """Game form for game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    letters_guessed = messages.StringField(6, required=True)

class GameForms(messages.Message):
    """Return multiple game forms"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class NewGameForm(messages.Message):
    """Form used to create a new game"""
    user_name = messages.StringField(1, required=True)
    

class MakeMoveForm(messages.Message):
    """Form used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    guesses = messages.IntegerField(4, required=True)
   

class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

class UserForm(messages.Message):
    """User Form"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2)
    wins = messages.IntegerField(3, required=True)
    total_played = messages.IntegerField(4, required=True)
    win_percentage = messages.FloatField(5, required=True)

class UserForms(messages.Message):
    """Return multiple User Forms """
    items = messages.MessageField(UserForm, 1, repeated=True)
