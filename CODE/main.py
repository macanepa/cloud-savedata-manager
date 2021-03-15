import mcutils as mc
import utilities

mc.activate_mc_logger(console_log_level='warning')
mc.ColorSettings.is_dev = True
mc.ColorSettings.print_color = True

mf_exit = mc.MenuFunction(title='Exit', function=mc.exit_application)
mf_add_game = mc.MenuFunction(title='Backup SaveData to Cloud', function=utilities.add_game)
mf_download_data = mc.MenuFunction(title='Restore SaveData from Cloud')

mc_menu = mc.Menu(title='Cloud SaveData Manager',
                  options=[mf_download_data, mf_add_game, mf_exit],
                  back=False)


while True:
    mc_menu.show()
