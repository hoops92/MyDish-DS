from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import Required, Email


class API_test_form(Form):
    ingr01 = TextField(u'Ingredient 01', validators=[Required()])
    ingr02 = TextField(u'Ingredient 02', validators=[Required()])
    ingr03 = TextField(u'Ingredient 03', validators=[Required()])
    ingr04 = TextField(u'Ingredient 04')
    ingr05 = TextField(u'Ingredient 05')
    ingr06 = TextField(u'Ingredient 06')
    ingr07 = TextField(u'Ingredient 07')
    ingr08 = TextField(u'Ingredient 08')
    ingr09 = TextField(u'Ingredient 09')
    ingr10 = TextField(u'Ingredient 10')

    submit = SubmitField(u'Signup')