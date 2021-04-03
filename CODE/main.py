import mcutils as mc
import utilities
import google_api as ga
from packaging import version

mc.ColorSettings.is_dev = False
mc.activate_mc_logger('info')
utilities.initialize()

mf_exit = mc.MenuFunction(title='Exit', function=mc.exit_application)
mf_add_new_game = mc.MenuFunction(title='Add New Title', function=utilities.add_game)
mf_update_game = mc.MenuFunction(title='Update Existing Title', function=utilities.update_game)
mf_download_data = mc.MenuFunction(title='Restore SaveData from Cloud', function=utilities.restore_game)
mf_change_sync_account = mc.MenuFunction(title='Change Sync Account', function=utilities.change_sync_account)
mf_about = mc.MenuFunction(title='About Cloud SaveData Manager', function=utilities.display_app_info)
mf_remove_game = mc.MenuFunction(title='Delete Cloud SaveData', function=utilities.delete_cloud_savedata)
mf_check_update = mc.MenuFunction(title='Check for updates', function=utilities.check_update)

mc_add_game = mc.Menu(title='Backup SaveData to Cloud', options=[mf_add_new_game, mf_update_game])

mc_options = mc.Menu(title='Settings', options=[mf_change_sync_account, mf_check_update, mf_about])

mc_title = f'Cloud SaveData Manager [{mc.Color.ORANGE}{utilities.APP_VERSION}{mc.Color.RESET}]\t' \
           f'({mc.Color.GREEN}{ga.get_user_info()}{mc.Color.RESET})'

latest_version = utilities.get_latest_version()
if version.parse(latest_version) > version.parse(utilities.APP_VERSION):
    mc_title += f'\nNew Version Available: [{mc.Color.GREEN}{latest_version}{mc.Color.RESET}]'

mc_menu = mc.Menu(title=mc_title,
                  options=[mf_download_data, mc_add_game, mf_remove_game, mc_options, mf_exit],
                  back=False)


while True:
    mc_menu.show()
    utilities.initialize()
