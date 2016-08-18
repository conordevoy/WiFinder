from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.website.SQL_queries import *
from app.website.WiFinderApp import query

test = ['hello', 'aw', 'yis', 'motha', 'fuckin', 'breadcrumbs']


class test_form(Form):
    room = StringField('room', validators=[DataRequired()])
    date = StringField('date', validators=[DataRequired()])
    time = StringField('time', validators=[DataRequired()])


class time_date_room(Form):
    room = SelectField('room', choices=test, validators=[DataRequired()])