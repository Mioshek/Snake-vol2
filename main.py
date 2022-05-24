import gui

if __name__ == '__main__':
    settings_window = gui.SettingsWindow()
    game_settings = settings_window.create_settings_window()
    game_window = gui.GameWindow(game_settings)
    game_window.window_update()
    