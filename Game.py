"""Game.py - This file contains the class definitions for Game, GameForm, GameForms. The class Game
has three methods, namely 'new_game', 'to_game_form' and 'end_game'."""

import random
from protorpc import messages
from google.appengine.ext import ndb
from User import *
from Score import *

class Game(ndb.Model):
    """Game object"""
    word_to_guess = ndb.StringProperty(required=True)
    letters_guessed = ndb.StringProperty(required=True, default='')
    attempts_allowed = ndb.IntegerProperty(required=True, default=9)
    attempts_remaining = ndb.IntegerProperty(required=True, default=9)
    letters_right_position = ndb.StringProperty(required=True, default='')
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
                    letters_right_position = '',
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
