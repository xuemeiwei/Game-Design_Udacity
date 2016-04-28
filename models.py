"""models.py - This file contains all the entities used in this project, 
namely User, Game and Score and also all the forms."""

from User import *
from Game import *
from Score import *

class NewGameForm(messages.Message):
    """Form used to create a new game"""
    user_name = messages.StringField(1, required=True)
    
class MakeMoveForm(messages.Message):
    """Form used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

