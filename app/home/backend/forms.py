# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextField#, FileField
from wtforms.validators import InputRequired, Email, DataRequired


class AIcookForm(FlaskForm):
    detect_image = FileField ('Photo', id='detect_image') #, validators=[Regexp(u'^[^/\\]\.jpg$')])
    pair_ingredients = TextField    ('Ingredients', id='ingredients'   , validators=[])
    present_menu = TextField    ('Menu', id='menu'   , validators=[])
