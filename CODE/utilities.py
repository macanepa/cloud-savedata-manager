import google_api as ga
import os
import mcutils as mc
import zipfile
import logging
from pprint import pprint

SETTINGS_PATH = 'settings.config'


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def unzipdir(file_path: str, output_path: str = None):
    with zipfile.ZipFile(file_path, 'r') as zipObj:
        if output_path:
            zipObj.extractall(output_path)
        else:
            zipObj.extractall()


def create_config():
    mc.generate_json(SETTINGS_PATH, {})
    logging.info('New settings.config file generated')


def download_config():
    logging.info('Downloading Config Files')
    service = ga.get_service()
    settings_file_id = ga.return_id(service=service,
                                    find='settings.config')
    if settings_file_id:
        ga.download_file(service=service,
                         file_id=settings_file_id,
                         output_path=SETTINGS_PATH)
        logging.info('settings.config file downloaded successfully')
    elif os.path.exists(SETTINGS_PATH):
        logging.warning('Using local settings.config file')
    else:
        logging.warning('No settings.config file found')
        create_config()


def upload_settings():
    service = ga.get_service()
    ga.upload_file(service=service,
                   file_path='settings.config',
                   parent_id=ga.list_folders(service))


def create_game_data(data):
    if 'id' in list(data.keys()):
        file_id = data['id']
    else:
        file_id = None
    try:
        config = mc.get_dict_from_json(SETTINGS_PATH)
    except FileNotFoundError:
        logging.warning(f'{SETTINGS_PATH} not found')
        create_config()
        config = mc.get_dict_from_json(SETTINGS_PATH)

    if data['name'] in config.keys():
        mc_overwrite = mc.Menu(title=f'{data["name"]} already exists. Overwrite SaveData?',
                               options=['Yes', 'No'], back=False)
        mc_overwrite.show()
        if mc_overwrite.returned_value == '2':
            return
        else:
            file_id = config[data['name']]['id']

    user_profile = os.path.expanduser('~')
    path = data['path']
    if path.startswith(user_profile):
        path = path.replace(user_profile, 'HOME')
    print(path)

    # zip savedata
    real_path = path
    if path.startswith('HOME'):
        real_path = real_path.replace('HOME', os.path.expanduser('~'))
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    zip_filename = f'tmp/{data["name"]}.zip'
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    zipdir(real_path, zipf)
    zipf.close()

    # Upload to google drive
    service = ga.get_service()
    if file_id:
        ga.update_file(service, zip_filename, file_id)
    else:
        folder_id = ga.create_folder(service=service,
                                     folder_name=data['name'],
                                     parent_id=ga.list_folders(service=service, get_root=True))
        file_id = ga.upload_file(service, zip_filename, folder_id)

    data_config = {
        'name': data['name'],
        'path': path,
        'id': file_id,
    }

    config[data['name']] = data_config
    mc.generate_json(SETTINGS_PATH, config)

    settings_file_id = ga.return_id(service=service,
                                    find='settings.config')
    if settings_file_id:
        logging.info('updating settings.config in cloud')
        ga.update_file(service=service,
                       file_path=SETTINGS_PATH,
                       file_id=settings_file_id)
    else:
        logging.warning('no settings.config found in cloud')
        mc_upload_settings = mc.Menu(title=f'Upload local settings.config to cloud?', options=['Yes', 'No'], back=False)
        mc_upload_settings.show()
        if mc_upload_settings.returned_value == '1':
            logging.info('uploading local settings.config to cloud')
            ga.upload_file(service=service,
                           file_path=SETTINGS_PATH,
                           parent_id=ga.list_folders(service=service, get_root=True))


def initialize():
    download_config()


def add_game():
    mc_add_game = mc.Menu(title='Complete the following information', options=['name', 'path'], input_each=True)
    mc_add_game.show()
    data = mc_add_game.returned_value
    create_game_data(data)


def update_game():
    config = mc.get_dict_from_json(SETTINGS_PATH)
    options = list(config.keys())
    if len(options) == 0:
        logging.warning('No title SaveData found')
        return
    mc_add_game = mc.Menu(title='Select a Title', options=options)
    mc_add_game.show()
    index = int(mc_add_game.returned_value)
    if index == 0:
        return
    data = config[options[index - 1]]
    pprint(data)
    create_game_data(data)


def restore_game():
    config = mc.get_dict_from_json(SETTINGS_PATH)
    options = list(config.keys())
    if len(options) == 0:
        logging.warning('No title SaveData found')
        return
    mc_add_game = mc.Menu(title='Select a Title', options=options)
    mc_add_game.show()
    index = int(mc_add_game.returned_value)
    if index == 0:
        return
    data = config[options[index - 1]]
    pprint(data)
    directory = data['path']
    print(directory)
    if directory.startswith('HOME'):
        directory = directory.replace('HOME', os.path.expanduser('~'))
    output_path = directory+'.zip'
    print(output_path)

    mc_confirmation = mc.Menu(title=f'Cloud SaveData will overwrite local data at {output_path}\n'
                                    f'Continue?',
                              options=['Yes', 'No'], back=False)
    mc_confirmation.show()
    if mc_confirmation.returned_value == '1':
        os.makedirs(os.path.dirname(output_path))
        service = ga.get_service()
        ga.download_file(service=service,
                         file_id=data['id'],
                         output_path=output_path)

        unzipdir(file_path=output_path,
                 output_path=os.path.dirname(output_path))

    os.remove(output_path)


def change_sync_account():
    mc_remove_sync_confirmation = mc.Menu(title='Are you sure you want to change sync account?\n'
                                                'You will have to login again with a Google Account',
                                          options=['Yes', 'No'])
    mc_remove_sync_confirmation.show()
    if mc_remove_sync_confirmation.returned_value == '1':
        os.remove('token.json')
        os.remove('settings.config')
    ga.get_service()


if __name__ == '__main__':
    download_config()
