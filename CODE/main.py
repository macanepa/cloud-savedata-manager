import mcutils as mc
import utilities
import google_api as ga

mc.activate_mc_logger(console_log_level='info')
mc.ColorSettings.is_dev = True
mc.ColorSettings.print_color = True

mf_exit = mc.MenuFunction(title='Exit', function=mc.exit_application)
mf_add_new_game = mc.MenuFunction(title='Add New Title', function=utilities.add_game)
mf_update_game = mc.MenuFunction(title='Update Existing Title', function=utilities.update_game)
mf_download_data = mc.MenuFunction(title='Restore SaveData from Cloud', function=utilities.restore_game)
mf_change_sync_account = mc.MenuFunction(title='Change Sync Account', function=utilities.change_sync_account)

mc_add_game = mc.Menu(title='Backup SaveData to Cloud', options=[mf_add_new_game, mf_update_game])

mc_options = mc.Menu(title='Settings', options=[mf_change_sync_account])

mc_menu = mc.Menu(title='Cloud SaveData Manager\t'
                        f'({mc.Color.GREEN}{ga.get_user_info()}{mc.Color.RESET})',
                  options=[mf_download_data, mc_add_game, mc_options, mf_exit],
                  back=False)


while True:
    utilities.initialize()
    mc_menu.show()
