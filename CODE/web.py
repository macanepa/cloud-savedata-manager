import mcutils as mc
from flask import Flask
from flaskwebgui import FlaskUI   # get the FlaskUI class
from flask import render_template, request, redirect
import utilities
import google_api as ga
from pprint import pprint
import sys
import os
from packaging import version


if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

ui = FlaskUI(app, width=1100, height=550)

mc.ColorSettings.is_dev = False
mc.activate_mc_logger('info')
utilities.initialize()


@app.route("/")
def index():
    config = mc.get_dict_from_json(utilities.SETTINGS_PATH)
    game_list = list(config.keys())
    latest_version = utilities.get_latest_version()
    new_version = None
    if version.parse(latest_version) > version.parse(utilities.APP_VERSION):
        new_version = latest_version
    return render_template('index.html',
                           email=ga.get_user_info(),
                           games=game_list,
                           len=len(game_list),
                           APP_VERSION=utilities.APP_VERSION,
                           new_version=new_version)


@app.route('/games', methods=['GET'])
def games():
    if request.method == 'GET':
        game_name = request.args.get('gameName')
        config = mc.get_dict_from_json(utilities.SETTINGS_PATH)
        if game_name in list(config.keys()):
            return_dict = config[game_name]
            return_dict['game_name'] = game_name
            is_local = utilities.check_local(utilities.decrypt_path(return_dict['path']))
            return_dict['path'] = utilities.decrypt_path(return_dict['path'])
            return_dict['is_local'] = is_local
            return return_dict
        else:
            return {'nice': False}
    return {'nice': None}


@app.route('/upload_cloud', methods=['GET'])
def upload_cloud():
    print('wiwi')
    if request.method == 'GET':
        config = mc.get_dict_from_json(utilities.SETTINGS_PATH)
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
        config = mc.get_dict_from_json(utilities.SETTINGS_PATH)
        print(request.args)
        game_name = request.args.get('gameName')
        print(game_name)
        if game_name in list(config.keys()):
            utilities.restore_game(game_id=game_name,
                                   menu=False)
            return redirect('')  # refresh
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


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':

        utilities.change_sync_account(menu=False)
        return redirect('/')
    return {'nice': False}


@app.route('/delete_cloud', methods=['GET'])
def delete_cloud():
    if request.method == 'GET':
        utilities.delete_cloud_savedata(game_name=request.args.get('gameName'),
                                        menu=False)
        return redirect('/')
    return {'nice': False}


ui.run()
