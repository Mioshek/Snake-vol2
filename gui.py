import PySimpleGUI as sg
import logic
from time import time
from time import sleep
import scores_json

#
class SettingsWindow:
    def __init__(self) -> None:
        self.board_rows = [
        sg.Text(text="Field Width"),
        sg.Slider(range=(10, 30), default_value=10, orientation="horizontal")]
        
        self.board_cols = [
            sg.Text(text="Field Height"),
            sg.Slider(range=(10, 30), default_value=10, orientation="horizontal")]
        
        self.layout = [
            [sg.Text("Welcome to Snake The Game!", justification="center")],  # First row
            self.board_rows,  # Second row
            self.board_cols, # Third row
            [sg.Radio("Easy", "difficulty", default=True),sg.Radio("Medium", "difficulty"),  sg.Radio("Hard", "difficulty")],  # Fourth row
            [sg.Button("New Game"), sg.Button("Exit")],  #Fifth row
        ]
        
    def create_settings_window(self):
        sg.theme('Dark')
        window = sg.Window("Snake The Game", self.layout)

        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "New Game":
                window.close()
                DIFFICULTY=1
                if values[2]: DIFFICULTY = 0.4
                elif values[3]: DIFFICULTY = 0.25
                else: DIFFICULTY = 0.1
                return [int(values[0]), int(values[1]), DIFFICULTY]

       
# settings = SettingsWindow.create_settings_window()

class GameWindow:
    def __init__(self, game_settings):
        self.CELL_SIZE = 36 #the cell's size is 36x36 [px]
        self.CELLS_VERTICAL = game_settings[0]
        self.CELLS_HORIZONTAL = game_settings[1]
        self.DIFFICULTY = game_settings[2]
        self.field = sg.Graph(
        canvas_size=(self.CELLS_VERTICAL*self.CELL_SIZE, self.CELLS_HORIZONTAL*self.CELL_SIZE),
        graph_bottom_left=(0, 0),
        graph_top_right=(self.CELLS_VERTICAL*self.CELL_SIZE, self.CELLS_HORIZONTAL*self.CELL_SIZE),
        background_color="black")
        self.layout = [[self.field]]
        self.snake = logic.Snake()
        self.apple_pos = logic.Enviroment.generate_apple(self.CELLS_VERTICAL, self.CELLS_HORIZONTAL, self.snake)
    
    @staticmethod
    def position_to_pixels(point, CELL_SIZE):
        top_left_pos = [point.x*CELL_SIZE, point.y*CELL_SIZE]
        bottom_right_pos = top_left_pos[0] + CELL_SIZE, top_left_pos[1] + CELL_SIZE
        return top_left_pos, bottom_right_pos
    
    def create_game_window(self):
        sg.theme("DarkAmber")
        window = sg.Window("Snake The Game", self.layout, return_keyboard_events=True)
        return time(), window
    
    @staticmethod
    def restart_game_popup_window(current_score, window):
        size = 10
        current_score = len(current_score)
        try:
            ten_best_scores = scores_json.read_from_json()
        except: ten_best_scores = {0:0}
        ten_best_scores_list = [score for score in ten_best_scores]
        scores_json.write_to_json([current_score] + ten_best_scores_list)
        ten_best_scores_list = [score for score in ten_best_scores]
        
        if len(ten_best_scores_list)<10:
            size = len(ten_best_scores_list)
        print(current_score)
        score_popup = "Your Score was: {}". format(current_score)
        top_ten_scores = ["{th_score}. best was: {score}".format(th_score=i+1, score=ten_best_scores_list[i]) for i in range(size)]
        # restart_text = "Do You Want To Restart Snake The Game?"
        # restart_button = sg.Button(button_text="Restart")
        # exit_button  = sg.Button(button_text="yes")
        sg.PopupScrolled(score_popup, *top_ten_scores)

        sleep(2)
        window.close()
    
    def window_update(self):
        begin_time, window = GameWindow.create_game_window(self)
        direction = self.snake.current_direction
        while True:
            event, values = window.read(timeout=20)#in ms
            
            if event == sg.WIN_CLOSED:
                break
            if event == "Left:113" or event=="a:38": direction = self.snake.directions["left"] #AWSD does not work idk why
            if event == "Up:111" or event=="w:25": direction = self.snake.directions["upwards"]
            if event == "Right:114" or event=="d:40": direction = self.snake.directions["right"]
            if event == "Down:116" or event=="s:39": direction = self.snake.directions["downwards"]
            
            action_time = time() - begin_time #time between last user input and next read
            
            if action_time >= self.DIFFICULTY: #if any action has not been taken within chosen time then snake moves anyway(to prevent stopping) the shorter the time the faster snake moves
                begin_time = time()
                snake_update = self.snake.snake_update(direction, self.CELLS_VERTICAL, self.CELLS_HORIZONTAL, self.apple_pos, )
                if snake_update == 1: self.apple_pos = logic.Enviroment.generate_apple(self.CELLS_VERTICAL, self.CELLS_HORIZONTAL, self.snake)
                elif snake_update == -1: self.restart_game_popup_window(self.snake.snake_body, window)
                else: self.field.DrawRectangle((0, 0), (self.CELL_SIZE*self.CELLS_VERTICAL, self.CELL_SIZE*self.CELLS_HORIZONTAL), "black")

                top_left, bottom_right = GameWindow.position_to_pixels(logic.Point(self.apple_pos.x, self.apple_pos.y), self.CELL_SIZE)
                self.field.draw_rectangle(top_left, bottom_right, "red")
                
                for i, body_part in enumerate(self.snake.snake_body):
                    top_left, bottom_right = GameWindow.position_to_pixels(body_part, self.CELL_SIZE)
                    color = "gray" if i == 0 else "blue"
                    self.field.draw_rectangle(top_left, bottom_right, color)
        window.close()
