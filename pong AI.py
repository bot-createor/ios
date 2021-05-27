import tkinter as tk
import random
import time

class Bal:
    def __init__(self, canvas, paddle, computer, color):
        self.canvas = canvas
        self.paddle = paddle
        self.computer = computer
        self.id = canvas.create_oval(root.winfo_width() // 2 - 10, root.winfo_height() // 2 - 10, root.winfo_width() // 2 + 10, root.winfo_height() // 2 + 10, fill = color, outline = color)
        self.pos = self.canvas.coords(self.id)
        self.starts = [-3, -2, -1, 1, 2, 3]
        self.x = self.starts[random.randint(0, len(self.starts) - 1)]
        self.y = self.starts[random.randint(0, len(self.starts) - 1)]
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.paddle_scored = None
        self.computer_scored = None
        self.paddle_height = paddle.pos[3] - paddle.pos[1]
        self.start = True

    def hit_paddle(self):
         if self.pos[0] <= paddle.pos[2] and self.pos[2] >= paddle.pos[0]:
            if self.pos[3] > paddle.pos[1] - 5 and self.pos[1] < paddle.pos[3] - 5:
                return True
         return False

    def hit_computer(self):
         if self.pos[2] >= computer_paddle.computer_pos[0] and self.pos[0] <= computer_paddle.computer_pos[2]:
             if self.pos[1] >= computer_paddle.computer_pos[1] and self.pos[3] <= computer_paddle.computer_pos[3]:
                 return True
         return False
            
    def draw(self):
        global paddle_y
        self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)
        if self.pos[1] <= 0:
            self.y = 3
        if self.pos[0] <= 0:
            self.computer_scored = True
            self.hit_bottom = True
        if self.pos[2] >= self.canvas_width:
            self.paddle_scored  = True
            self.hit_bottom = True
        if self.pos[3] >= self.canvas_height:
            self.y = random.randint(-3, -1)
        if self.hit_paddle() == True:
            if self.y > 0:
                self.y = random.randint(1, 2)
            else:
                self.y = random.randint(-2, -1)
            self.x = random.randint(1, 3)
        if self.hit_computer() == True:
            if self.y > 0:
                self.y = random.randint(1, 2)
            else:
                self.y = random.randint(-2, -1)
            self.x = random.randint(-3, -1)
            
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        height = SCREEN_HEIGHT / 10 * 2.6 - SCREEN_HEIGHT / 10
        self.id = canvas.create_rectangle(SCREEN_WIDTH / 20, SCREEN_HEIGHT / 2 - height / 2, (SCREEN_WIDTH / 20) * 1.4, SCREEN_HEIGHT / 2 + height / 2, fill = color)
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.pos = self.canvas.coords(self.id)
        self.time = 0
        self.move = ''
        self.goto = ''

    def draw(self):
        global middelpunt
        middelpunt = (self.pos[3] + self.pos[1]) / 2
        if bal.x < 0:
            self.goto = self.calculate_move(middelpunt)
            if self.goto != '':
                if self.goto >= middelpunt:
                    self.y = 2
                else:
                    self.y = -2
        else:
            self.y = self.calculate_center(middelpunt)
        try:
            self.canvas.move(self.id, 0, self.y)
        except:
            pass
        self.pos = self.canvas.coords(self.id)
        if self.pos[1] <= 0:
            self.y = 0
            self.canvas.move(self.id, 0, 3)
        elif self.pos[3] >= self.canvas_height:
            self.y = 0
            self.canvas.move(self.id, 0, -3)

    def calculate_move(self, middelpunt):
        x = (bal.pos[2] + bal.pos[0]) / 2
        y = (bal.pos[3] + bal.pos[1]) / 2
        move_x = bal.x
        move_y = bal.y
        while True:
            x += move_x
            y += move_y
            if y <= 0:
                move_y = 2
            if y >= self.canvas_height:
                move_y = -2
            if x <= self.pos[2]:
                return y

    def calculate_center(self, middelpunt):
        center = self.canvas_height / 2
        if middelpunt > center or self.move == 'up':
            self.time += 1
            self.move = 'up'
            if self.time == 26:
                self.move = ''
                self.time = 0
            return -2
        elif middelpunt < center or self.move == 'down':
            self.time += 1
            self.move = 'down'
            if self.time == 26:
                self.move = ''
                self.time = 0
            return 2

class Computer_paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        height = SCREEN_HEIGHT / 10 * 2.6 - SCREEN_HEIGHT / 10
        self.id = canvas.create_rectangle((SCREEN_WIDTH / 20) * 19, SCREEN_HEIGHT / 2 - height / 2, (SCREEN_WIDTH / 20) * 18.6, SCREEN_HEIGHT / 2 + height / 2, fill = color)
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.computer_pos = self.canvas.coords(self.id)
        self.move = ''
        self.time = 0
        self.time_hit = 0
        self.move_hit = ''
        self.goto = ''

    def draw(self):

        self.y = self.choice()
        try:
            if self.computer_pos[1] + self.y < 0 or self.computer_pos[3] + self.y > self.canvas_height:
                self.y = 0
        except:
            pass
        try:
            self.canvas.move(self.id, 0, self.y)
        except:
            pass
        self.computer_pos = self.canvas.coords(self.id)

    def choice(self):
        middelpunt = (self.computer_pos[1] + self.computer_pos[3]) / 2
        if bal.x < 0:
            return self.calculate_center(middelpunt)
        return self.move_ball(middelpunt)

    def move_ball(self, middelpunt):
        global x, y
        if bal.x > 0:
            self.goto = self.calculate_move(middelpunt)
            if self.goto != '':
                if self.goto >= middelpunt:
                    self.time_hit += 1
                    self.move_hit = 'down'
                    if self.time_hit == 21:
                        self.move_hit = ''
                        self.time_hit = 0
                    return 2
                else:
                    self.time_hit += 1
                    self.move_hit = 'up'
                    if self.time_hit == 21:
                        self.move_hit = ''
                        self.time_hit = 0
                    return -2

    def calculate_center(self, middelpunt):
        center = self.canvas_height / 2
        if middelpunt > center or self.move == 'up':
            self.time += 1
            self.move = 'up'
            if self.time == 26:
                self.move = ''
                self.time = 0
            return -2
        elif middelpunt < center or self.move == 'down':
            self.time += 1
            self.move = 'down'
            if self.time == 26:
                self.move = ''
                self.time = 0
            return 2

    def calculate_move(self, middelpunt):
        x = (bal.pos[2] + bal.pos[0]) / 2
        y = (bal.pos[3] + bal.pos[1]) / 2
        move_x = bal.x
        move_y = bal.y
        while True:
            x += move_x
            y += move_y
            if y <= 0:
                move_y = 2
            if y >= self.canvas_height:
                move_y = -2
            if x >= self.computer_pos[0]:
                return y
        
class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.screen_middle = SCREEN_WIDTH / 2
        self.width = SCREEN_WIDTH / 30
        self.height = SCREEN_HEIGHT / 25

    def line(self):
        global paddle_pos_zero_1, paddle_pos_zero_2, paddle_pos_zero_3, paddle_pos_zero_4, paddle_pos_zero_5, paddle_pos_zero_6, paddle_pos_zero_7, computer_pos_zero_1, computer_pos_zero_2, computer_pos_zero_3, computer_pos_zero_4, computer_pos_zero_5, computer_pos_zero_6, computer_pos_zero_7

        paddle_zero_1 = canvas.create_rectangle(self.screen_middle - (self.width * 1.75), self.height / 2, self.screen_middle - self.width, self.height * 0.75, fill = '#0b0b0b')
        paddle_pos_zero_1 = self.canvas.coords(paddle_zero_1)
        
        line_width = paddle_pos_zero_1[3] - paddle_pos_zero_1[1]
        line_lenght =paddle_pos_zero_1[2] - paddle_pos_zero_1[0]
        
        paddle_pos_zero_2 = [paddle_pos_zero_1[0], paddle_pos_zero_1[1] + line_lenght * 2 - line_width, paddle_pos_zero_1[2] + line_width, paddle_pos_zero_1[3] + line_lenght * 2 - line_width]

        paddle_pos_zero_3 = [paddle_pos_zero_1[0], paddle_pos_zero_1[1] + line_lenght - line_width, paddle_pos_zero_1[2] + line_width, paddle_pos_zero_1[3] + line_lenght - line_width]
        
        paddle_pos_zero_4 = [paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[0] + line_width, paddle_pos_zero_1[1] + line_lenght]
        
        paddle_pos_zero_5 = [paddle_pos_zero_1[0] + line_lenght, paddle_pos_zero_1[1], paddle_pos_zero_1[0] + line_width + line_lenght, paddle_pos_zero_1[1] + line_lenght]
        
        paddle_pos_zero_6 = [paddle_pos_zero_1[0], paddle_pos_zero_1[1] + line_lenght, paddle_pos_zero_1[0] + line_width, paddle_pos_zero_1[1] + line_lenght * 2]
        
        paddle_pos_zero_7 = [paddle_pos_zero_1[0] + line_lenght, paddle_pos_zero_1[1] + line_lenght, paddle_pos_zero_1[0] + line_width + line_lenght, paddle_pos_zero_1[1] + line_lenght * 2]
            
        computer_zero_1 = self.canvas.create_rectangle(self.screen_middle + (self.width * 1.75), self.height / 2, self.screen_middle + self.width, self.height * 0.75, fill = '#0b0b0b')
        computer_pos_zero_1 = self.canvas.coords(computer_zero_1)
        
        line_width = computer_pos_zero_1[3] - computer_pos_zero_1[1]
        line_lenght = computer_pos_zero_1[2] - computer_pos_zero_1[0]
        
        computer_pos_zero_2 = [computer_pos_zero_1[0], computer_pos_zero_1[1] + line_lenght * 2 - line_width, computer_pos_zero_1[2] + line_width, computer_pos_zero_1[3] + line_lenght * 2 - line_width]

        computer_pos_zero_3 = [computer_pos_zero_1[0], computer_pos_zero_1[1] + line_lenght - line_width, computer_pos_zero_1[2] + line_width, computer_pos_zero_1[3] + line_lenght - line_width]
        
        computer_pos_zero_4 = [computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[0] + line_width, computer_pos_zero_1[1] + line_lenght]
        
        computer_pos_zero_5 = [computer_pos_zero_1[0] + line_lenght, computer_pos_zero_1[1], computer_pos_zero_1[0] + line_width + line_lenght, computer_pos_zero_1[1] + line_lenght]
        
        computer_pos_zero_6 = [computer_pos_zero_1[0], computer_pos_zero_1[1] + line_lenght, computer_pos_zero_1[0] + line_width, computer_pos_zero_1[1] + line_lenght * 2]
        
        computer_pos_zero_7 = [computer_pos_zero_1[0] + line_lenght, computer_pos_zero_1[1] + line_lenght, computer_pos_zero_1[0] + line_width + line_lenght, computer_pos_zero_1[1] + line_lenght * 2]

    def score_zero(self, white, black, score):
        if score == 0:
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = black)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)

        elif score == 1:
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = white)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = black)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = white)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = white)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)
        else:
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = black)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)

            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = white)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = black)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = white)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = white)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_one(self, white, black, score):
        if score == 0:
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = black)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = black)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = black)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = black)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = black)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)

        else:
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = black)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = black)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = black)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = black)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = black)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_two(self, white, black, score):
        if score == 0:
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = black)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = black)
            
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = white)
        else:
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = black)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = black)
            
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = white)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = white)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = white)

    def score_three(self, white, black, score):
        if score == 0:
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = black)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = black)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)
        else:
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = white)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = white)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = black)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = black)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_for(self, white, black, score):
        if score == 0:
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = black)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = black)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = black)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)
        else:
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = black)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = black)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = white)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = white)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = black)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)
            
    def score_five(self, white, black, score):
        if score == 0:
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = black)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = black)
            
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2] + (paddle_pos_zero_1[3] - paddle_pos_zero_1[1]), paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)
        else:
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = black)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = black)
            
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2] + (computer_pos_zero_1[3] - computer_pos_zero_1[1]), computer_pos_zero_1[3], fill = white)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = white)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = white)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_six(self, white, black, score):
        if score == 0:
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = black)

            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)
        else:
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = black)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = black)
            
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = white)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = white)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_seven(self, white, black, score):
        if score == 0:
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = black)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = black)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = black)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = black)
            
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)
        else:
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = black)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = black)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = black)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = black)
            
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = white)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_eight(self, white, black, score):
        if score == 0:
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)
        else:
            computer_zero_1 = canvas.create_rectangle(computer_pos_zero_1[0], computer_pos_zero_1[1], computer_pos_zero_1[2], computer_pos_zero_1[3], fill = white)
            computer_zero_2 = canvas.create_rectangle(computer_pos_zero_2[0], computer_pos_zero_2[1], computer_pos_zero_2[2], computer_pos_zero_2[3], fill = white)
            computer_zero_3 = canvas.create_rectangle(computer_pos_zero_3[0], computer_pos_zero_3[1], computer_pos_zero_3[2], computer_pos_zero_3[3], fill = white)
            computer_zero_4 = canvas.create_rectangle(computer_pos_zero_4[0], computer_pos_zero_4[1], computer_pos_zero_4[2], computer_pos_zero_4[3], fill = white)
            computer_zero_5 = canvas.create_rectangle(computer_pos_zero_5[0], computer_pos_zero_5[1], computer_pos_zero_5[2], computer_pos_zero_5[3], fill = white)
            computer_zero_6 = canvas.create_rectangle(computer_pos_zero_6[0], computer_pos_zero_6[1], computer_pos_zero_6[2], computer_pos_zero_6[3], fill = white)
            computer_zero_7 = canvas.create_rectangle(computer_pos_zero_7[0], computer_pos_zero_7[1], computer_pos_zero_7[2], computer_pos_zero_7[3], fill = white)

    def score_nine(self, white, black, score):
        if score == 0:
            paddle_zero_2 = canvas.create_rectangle(paddle_pos_zero_2[0], paddle_pos_zero_2[1], paddle_pos_zero_2[2], paddle_pos_zero_2[3], fill = black)
            paddle_zero_6 = canvas.create_rectangle(paddle_pos_zero_6[0], paddle_pos_zero_6[1], paddle_pos_zero_6[2], paddle_pos_zero_6[3], fill = black)
            
            paddle_zero_1 = canvas.create_rectangle(paddle_pos_zero_1[0], paddle_pos_zero_1[1], paddle_pos_zero_1[2], paddle_pos_zero_1[3], fill = white)
            paddle_zero_3 = canvas.create_rectangle(paddle_pos_zero_3[0], paddle_pos_zero_3[1], paddle_pos_zero_3[2], paddle_pos_zero_3[3], fill = white)
            paddle_zero_4 = canvas.create_rectangle(paddle_pos_zero_4[0], paddle_pos_zero_4[1], paddle_pos_zero_4[2], paddle_pos_zero_4[3], fill = white)
            paddle_zero_5 = canvas.create_rectangle(paddle_pos_zero_5[0], paddle_pos_zero_5[1], paddle_pos_zero_5[2], paddle_pos_zero_5[3], fill = white)
            paddle_zero_7 = canvas.create_rectangle(paddle_pos_zero_7[0], paddle_pos_zero_7[1], paddle_pos_zero_7[2], paddle_pos_zero_7[3], fill = white)

root = tk.Tk()
root.title('pong')
root.resizable(0, 0)
root.wm_attributes('-fullscreen', 1)
root.configure(bg = '#000000')
root.update()

SCREEN_WIDTH = root.winfo_width()

SCREEN_HEIGHT = root.winfo_height()

canvas = tk.Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, bd = 0, highlightthickness = 0, bg = '#000000')
canvas.pack()
root.update()

paddle = Paddle(canvas, '#ffffff')
computer_paddle = Computer_paddle(canvas, '#ffffff')
bal = Bal(canvas, paddle, computer_paddle, '#ffffff')
score = Score(canvas)

game_score = [0, 0]
score.line()
score.score_zero('#ffffff', '#0b0b0b', 3)

number_list = {'0' : 'zero', '1' : 'one', '2' : 'two', '3' : 'three', '4' : 'for', '5' : 'five', '6' : 'six', '7' : 'seven', '8' : 'eight', '9' : 'nine'}

bal.draw()
paddle.draw()
computer_paddle.draw()
root.update()

time.sleep(1.5)
        
try:
    while 1:
        if bal.hit_bottom == False:
            bal.draw()
            paddle.draw()
            computer_paddle.draw()
            root.update()
        else:

            if bal.paddle_scored:
                game_score[0] += 1
                draw_score = list(str(game_score[0]))
                if len(draw_score) == 1:
                    for number in number_list:
                        if draw_score[0] == number:
                            if number_list[number] == 'zero':
                                score.score_zero('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'one':
                                score.score_one('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'two':
                                score.score_two('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'three':
                                score.score_three('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'for':
                                score.score_for('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'five':
                                score.score_five('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'six':
                                score.score_six('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'seven':
                                score.score_seven('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'eight':
                                score.score_eight('#ffffff', '#0b0b0b', 0)
                            elif number_list[number] == 'nine':
                                score.score_nine('#ffffff', '#0b0b0b', 0)
                            break
            elif bal.computer_scored:
                game_score[1] += 1
                draw_score = list(str(game_score[1]))
                if len(draw_score) == 1:
                    for number in number_list:
                        if draw_score[0] == number:
                            if number_list[number] == 'zero':
                                score.score_zero('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'one':
                                score.score_one('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'two':
                                score.score_two('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'three':
                                score.score_three('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'for':
                                score.score_for('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'five':
                                score.score_five('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'six':
                                score.score_six('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'seven':
                                score.score_seven('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'eight':
                                score.score_eight('#ffffff', '#0b0b0b', 1)
                            elif number_list[number] == 'nine':
                                score.score_nine('#ffffff', '#0b0b0b', 1)
                            break
            
            bal.canvas.delete(bal.id)
            bal = Bal(canvas, paddle, computer_paddle, '#ffffff')

            paddle.canvas.delete(paddle.id)
            paddle = Paddle(canvas, '#ffffff')

            computer_paddle.canvas.delete(computer_paddle.id)
            computer_paddle = Computer_paddle(canvas, '#ffffff')

            root.update()
            time.sleep(1.5)
        root.update_idletasks()
except:
    pass
