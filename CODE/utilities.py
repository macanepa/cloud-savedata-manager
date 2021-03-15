import google_api as ga
import os
import mcutils as mc
import zipfile
import logging
from pprint import pprint

SETTINGS_PATH = 'settings.config'


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def create_config():
    mc.generate_json(SETTINGS_PATH, {})

def download_config():
    logging.info('Downloading Config Files')
    service = ga.get_service()
    ga.download_file(service=service,
                     )

def upload_settings():
    service = ga.get_service()
    ga.upload_file(service=service,
                   file_path='settings.config',
                   parent_id=ga.list_folders(service))

def create_game_data(data):
    folder_id = None
    try:
        config = mc.get_dict_from_json(SETTINGS_PATH)
    except FileNotFoundError:
        logging.warning(f'{SETTINGS_PATH} not found')
        create_config()
        config = mc.get_dict_from_json(SETTINGS_PATH)

    if data['name'] in config.keys():
        mc_overwrite = mc.Menu(title=f'{data["name"]} already exists. Overwrite SaveData?', options=['Yes', 'No'], back=False)
        mc_overwrite.show()
        if mc_overwrite.returned_value == '2':
            return
        else:
            folder_id = config[data['name']]['id']


    username = os.path.basename(os.path.expanduser('~'))
    user_profile = os.path.expanduser('~')
    path = data['path']
    if path.startswith(user_profile):
        path = path.replace(user_profile, 'HOME')
    print(path)

    # zip savedata
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    zip_filename = f'tmp/{data["name"]}.zip'
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    zipdir(data['path'], zipf)
    zipf.close()

    # Upload to google drive
    service = ga.get_service()
    if not folder_id:
        folder_id = ga.create_folder(service=service,
                                     folder_name=data['name'],
                                     parent_id=ga.list_folders(service))
    ga.upload_file(service, zip_filename, folder_id)

    data_config = {
        'name': data['name'],
        'path': path,
        'id': folder_id,
    }

    config[data['name']] = data_config
    mc.generate_json(SETTINGS_PATH, config)


def add_game():
    mc_add_game = mc.Menu(title='Complete the following information', options=['name', 'path'], input_each=True)
    mc_add_game.show()
    data = mc_add_game.returned_value
    create_game_data(data)

if __name__ == '__main__':
    upload_settings()



