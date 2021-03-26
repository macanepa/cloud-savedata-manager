import google_api as ga
import os
import mcutils as mc
import zipfile
import logging
import subprocess
import webbrowser
from pprint import pprint


SETTINGS_PATH = 'credentials/settings.config'
TOKEN_PATH = 'credentials/token.json'
CREDENTIALS_PATH = 'credentials/credentials.json'


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
                   file_path=SETTINGS_PATH,
                   parent_id=ga.list_folders(service))


def create_game_data(data, menu=True):
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
        if menu:
            mc_overwrite = mc.Menu(title=f'{data["name"]} already exists. Overwrite SaveData?',
                                   options=['Yes', 'No'], back=False)
            mc_overwrite.show()
            if mc_overwrite.returned_value == '2':
                return
            else:
                file_id = config[data['name']]['id']
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
        if mc_upload_settings.returned_value == '1' or not menu:
            logging.info('uploading local settings.config to cloud')
            ga.upload_file(service=service,
                           file_path=SETTINGS_PATH,
                           parent_id=ga.list_folders(service=service, get_root=True))


def check_credentials():
    credentials_directory = os.path.join(os.getcwd(), "credentials")
    link = 'https://developers.google.com/drive/api/v3/quickstart/python'
    if not os.path.exists('credentials'):
        os.mkdir('credentials')
    if not os.path.exists(CREDENTIALS_PATH):
        webbrowser.open(link, new=2)
        subprocess.call(f"explorer {credentials_directory}", shell=True)
    while not os.path.exists(CREDENTIALS_PATH):
        logging.warning('no credentials.json found')
        mc.mcprint(f"""
        1. Head to {link} and click on "Enable the Drive API"
        2. Enter a name for the project, e.g "Cloud SaveData Manager"
        3. Select "Yes" and "Next"
        4. Select "Desktop app" and Create
        5. Click "Download Client Configuration"
        6. Place the "credentials.json" inside the "credentials" folder\n""")
        input('Enter to continue...')
        mc.clear(10)


def initialize():
    check_credentials()
    download_config()


def add_game():
    mc_add_game = mc.Menu(title='Complete the following information', options=['name', 'path'], input_each=True)
    mc_add_game.show()
    data = mc_add_game.returned_value
    create_game_data(data)


def update_game(game_id: str=None, menu: bool=True):
    config = mc.get_dict_from_json(SETTINGS_PATH)
    options = list(config.keys())
    if len(options) == 0:
        logging.warning('No title SaveData found')
        return
    if menu:
        mc_add_game = mc.Menu(title='Select a Title', options=options)
        mc_add_game.show()
        index = int(mc_add_game.returned_value)
        if index == 0:
            return
        data = config[options[index - 1]]
    else:
        data = config[game_id]
    pprint(data)
    create_game_data(data, menu=menu)


def restore_game(game_id: str=None, menu: bool=True):
    config = mc.get_dict_from_json(SETTINGS_PATH)
    if menu:
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
    else:
        data = config[game_id]
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
    if menu:
        mc_confirmation.show()
    if not menu or mc_confirmation.returned_value == '1':
        if not os.path.exists(os.path.dirname(output_path)):
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
                                          options=['Yes', 'No'],
                                          back=False)
    mc_remove_sync_confirmation.show()
    if mc_remove_sync_confirmation.returned_value == '1':
        os.remove(TOKEN_PATH)
        os.remove(SETTINGS_PATH)
    ga.get_service()


def display_app_info():
    about = mc.About(
        authors=['Matías Cánepa'],
        github_repo='https://github.com/macanepa/cloud-savedata-manager'
    )

    about.print_credits()


if __name__ == '__main__':
    download_config()
