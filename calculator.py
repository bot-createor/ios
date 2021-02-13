import tkinter as tk

root = tk.Tk()
root.title("calculator")

class Screen:
  def __init__(self):
    self.screen_width = root.winfo_width / 7
    self.screen_height = root.winfo_height / 4
    root.geometry(self.screen_width + "x" + self.screen_height)
    
    # input variables
    input_width = self.screen_width - (self.screen_width / 20 * 2)
    input_height = self.screen_height - self.screen_height - (self.screen_height / 20 * 2)
    # create input
    self.create_input(self.screen_width - (self.screen_width - input_width / 2), self.screen_height - (self.screen_height - input_height), \
                      self.screen_width - input_width / 2, self.screen_height - input_height)
    self.create_number_buttons()
    
  def create_input(self, x1, y1, x2, y2, width, height):
    input = tk.Entry(root, x1, y1, x2, y2, fill = "#e0dede", outline = "#383838", state = DISABLED)
   
  def create_number_buttons(self, width, height):
    pass
    
screen = Screen()
