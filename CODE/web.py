import mcutils as mc
from flask import Flask
from flaskwebgui import FlaskUI   # get the FlaskUI class
from flask import render_template, request
import utilities
import google_api as ga
from pprint import pprint

app = Flask(__name__)
ui = FlaskUI(app, width=850, height=440)


mc.activate_mc_logger('info')
utilities.initialize()

config = mc.get_dict_from_json(utilities.SETTINGS_PATH)
game_list = list(config.keys())

@app.route("/")
def index():
    return render_template('index.html',
                           email=ga.get_user_info(),
                           games=game_list,
                           len=len(game_list))

@app.route('/games', methods=['GET'])
def games():
    if request.method == 'GET':
        game_name = request.args.get('gameName')
        if game_name in list(config.keys()):
            return_dict = config[game_name]
            return_dict['game_name'] = game_name
            return return_dict
        else:
            return {'nice': False}
    return {'nice': None}


@app.route('/upload_cloud', methods=['GET'])
def upload_cloud():
    print('wiwi')
    if request.method == 'GET':
        print(request.args)
        game_name = request.args.get('gameName')
        print(game_name)
        if game_name in list(config.keys()):
            utilities.update_game(game_id=game_name,
                                  menu=False)
            return {'response': 'Ok'}
        else:
            return {'nice': False}
    return {'nice': None}


@app.route('/download_cloud', methods=['GET'])
def download_cloud():
    if request.method == 'GET':
        print(request.args)
        game_name = request.args.get('gameName')
        print(game_name)
        if game_name in list(config.keys()):
            utilities.restore_game(game_id=game_name,
                                   menu=False)
            return {'response': 'Ok'}
        else:
            return {'nice': False}
    return {'nice': None}


@app.route('/addGame', methods=['POST'])
def add_game():
    print("WIWIEII")
    if request.method == 'POST':
        print("walala")
        pprint(request.form)
        data = request.form
        game_name = data.get('game')
        path = data.get('path')
        data = {'name': game_name,
                'path': path}
        utilities.create_game_data(data=data, menu=False)
    return {'nice': True}


ui.run()
