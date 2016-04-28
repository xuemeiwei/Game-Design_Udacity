"""User.py - This file contains the class definitions for User, UserForm and UserForms."""

from protorpc import messages
from google.appengine.ext import ndb

class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    wins = ndb.IntegerProperty(default=0)
    total_games_played = ndb.IntegerProperty(default=0)

    """Adding an auto calculated field"""
    @property
    def win_percentage(self):
        if self.total_games_played >0:
            return float(self.wins)/float(self.total_games_played)
        else:
            return 0
    def to_user_form(self):
        """Copy user information to form"""
        return UserForm(name=self.name,
                        email=self.email,
                        wins=self.wins,
                        total_games_played=self.total_games_played,
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

class UserForm(messages.Message):
    """User Form"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2)
    wins = messages.IntegerField(3, required=True)
    total_games_played = messages.IntegerField(4, required=True)
    win_percentage = messages.FloatField(5, required=True)

class UserForms(messages.Message):
    """Return multiple User Forms """
    items = messages.MessageField(UserForm, 1, repeated=True)
