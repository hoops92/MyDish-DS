# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

import numpy as np 
import json

from tensorflow.keras.models import load_model

from flask import Flask, Blueprint
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

from .forms import API_test_form
from .nav import nav

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('MyDish - Ingredient Prediction API', '.index'),
    View('Home', '.index'),
    View('API Example', '.test_form'),
    View('Documentation', '.documentation')
    
    Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))

with open('ingr_int.json') as json_file:
    ingr_int = json.load(json_file)
with open('int_ingr.json') as json_file:
    int_ingr = json.load(json_file)

my_model = load_model('baseline_pred.h5')
max_pred_length = 10

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def pred_next_ingr(ingr_list):

    pred_next = []

    for diversity in [0.2, 0.6, 0.8, 1.2]:

        start_ingr = [ingr_int[x] for x in ingr_list]
        
        for i in range(10):
            x_pred = np.zeros((1, max_pred_length, len(ingr_int)))
            for t, ingr in enumerate(start_ingr):
                x_pred[0, t, ingr] = 1

            preds = my_model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_ingredient = int_ingr[str(next_index)]

            pred_next.append(next_ingredient)

    return list(set(pred_next))

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/test-form/', methods=('GET', 'POST'))
def test_form():
    form = API_test_form()

    if form.validate_on_submit():
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        if request.method == 'POST':
            
            ingr_inputs = request.form.to_dict(flat=True)

            ingr_inputs.update((x, y) for x, y in ingr_inputs.items())

            ingr_list = list(ingr_inputs.values())
            pred_input = ingr_list[-10:]
            next_preds = pred_next_ingr(pred_input)

            next_preds = (set(next_preds) - set(ingr_list))
            
            return render_template("result.html",result = next_preds)
    
        flash('Hello, {}. You have successfully signed up'
              .format(escape(form.name.data)))

        # In a real application, you may wish to avoid this tedious redirect.
        return redirect(url_for('.index'))

    return render_template('signup.html', form=form)
