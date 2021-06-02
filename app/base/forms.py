# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, FileField
from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])

class AIcookForm(FlaskForm):
    detect_image = FileField ('Photo', id='detectimage_photo') #, validators=[Regexp(u'^[^/\\]\.jpg$')])
    pair_ingredients = TextField    ('Ingredients', id='ingredients'   , validators=[])
    present_menu = TextField    ('Menu', id='menu'   , validators=[])
