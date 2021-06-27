import tkinter as tk
import time

GAME_NAME = "Cyber Medication"

root = tk.Tk()
root.title(GAME_NAME)
root.geometry("500x350")

# Cell Groups
machinecell = []
pushcell = []
enemycell = []
turncell = []
normalcell = []
bouncecell = []
generatorcell = []
buildcell = []

canvas = tk.Canvas(root, width = 500, height = 350, bg = "#0b0b0b")
canvas.pack()

tutorial_clicked = -1
get_clicked = 0

level = 0

class MachineCell:
  def __init__(self, x, y, x2, y2, color):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color)
    self.pos = canvas.coords(self.id)

  def destroy(self):
    canvas.delete(self.id)

class PushCell:
  def __init__(self, x, y, x2, y2, color, version, generator, activefill, moving):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color, tag = "id", activefill = activefill)

    self.pos = canvas.coords(self.id)

    self.fill = color
    self.activefill = activefill

    self.selected = False

    if version == 1:
      self.x = 5
      self.y = 0

      self.arrow = canvas.create_polygon(self.pos[0] + 33, self.pos[1] + 25, self.pos[0] + 20, self.pos[3] - 15, self.pos[0] + 20, self.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
    elif version == 2:
      self.x = -5
      self.y = 0

      self.arrow = canvas.create_polygon(self.pos[2] - 33, self.pos[1] + 25, self.pos[2] - 20, self.pos[3] - 15, self.pos[2] - 20, self.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
    elif version == 3:
      self.x = 0
      self.y = 5

      self.arrow = canvas.create_polygon(self.pos[2] - 25, self.pos[1] + 33, self.pos[0] + 15, self.pos[1] + 20, self.pos[2] - 15, self.pos[1] + 20, fill = "#ffffff", outline = "#ffffff")
    elif version == 4:
      self.x = 0
      self.y = -5

      self.arrow = canvas.create_polygon(self.pos[2] - 25, self.pos[3] - 33, self.pos[2] - 15, self.pos[3] - 20, self.pos[0] + 15, self.pos[3] - 20, fill = "#ffffff", outline = "#ffffff")

    self.version = version
    self.generator = generator
    
    self.moving = moving

    self.touched_generator = False

    canvas.tag_bind(self.arrow, "<Enter>", self.hover)
    canvas.tag_bind(self.arrow, "<Leave>", self.leave)

    canvas.tag_bind(self.id, "<Button-1>", self.select)
    canvas.tag_bind(self.arrow, "<Button-1>", self.select)

  def hover(self, evt):
    canvas.itemconfig(self.id, fill = self.activefill)

  def leave(self, evt):
    canvas.itemconfig(self.id, fill = self.fill)

  def select(self, evt):
    for x in buildcell:
      if x.pos == self.pos:
        self.selected = True

  def move(self):
    global tutorial_clicked
    
    if not self.touched_generator and get_clicked >= 1 and not building:
      self.moving = True

      if level == 1:
        tutorial_clicked += 1

  def draw(self):
    if self.moving:
      canvas.move(self.id, self.x, self.y)
      canvas.move(self.arrow, self.x, self.y)
      canvas.tag_raise(self.id)
      canvas.tag_raise(self.arrow)
      
      self.pos = canvas.coords(self.id)

  def control(self):
    try:
      for x in range(len(enemycell)):
        if enemycell[x].pos == self.pos:
          
          enemycell[x].destroy()
          del enemycell[x]
          self.destroy()

          if not len(enemycell):
            next_level()

          break
    except:
      pass

  def control_normalcell(self):
    if self.moving:
      for x in normalcell:
        for y in canvas.find_overlapping(x.pos[0], x.pos[1], x.pos[2], x.pos[3]):
          if canvas.find_withtag("id")[0] in canvas.find_overlapping(x.pos[0], x.pos[1], x.pos[2], x.pos[3]):
                        
            canvas.move(x.normalcell, self.x, self.y)
            x.pos = canvas.coords(x.normalcell)

            break

  def control_bouncecell(self):
    try:
      for x in bouncecell:
        for y in canvas.find_overlapping(x.pos[0], x.pos[1], x.pos[2], x.pos[3]):
          if canvas.find_withtag("id")[0] in canvas.find_overlapping(x.pos[0], x.pos[1], x.pos[2], x.pos[3]):

            canvas.delete(self.arrow)
            if self.x == 5:
              self.x = -5
              self.y = 0

              self.arrow = canvas.create_polygon(self.pos[2] - 33, self.pos[1] + 25, self.pos[2] - 20, self.pos[3] - 15, self.pos[2] - 20, self.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
              self.version = 2
            elif self.x == -5:
              self.x = 5
              self.y = 0

              self.arrow = canvas.create_polygon(self.pos[0] + 33, self.pos[1] + 25, self.pos[0] + 20, self.pos[3] - 15, self.pos[0] + 20, self.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
              self.version = 1
            if self.y == 5:
              self.y = -5
              self.x = 0

              self.arrow = canvas.create_polygon(self.pos[2] - 25, self.pos[3] - 33, self.pos[2] - 15, self.pos[3] - 20, self.pos[0] + 15, self.pos[3] - 20, fill = "#ffffff", outline = "#ffffff")
              self.version = 4
            elif self.y == -5:
              self.y = 5
              self.x = 0

              self.arrow = canvas.create_polygon(self.pos[2] - 25, self.pos[1] + 33, self.pos[0] + 15, self.pos[1] + 20, self.pos[2] - 15, self.pos[1] + 20, fill = "#ffffff", outline = "#ffffff")
              self.version = 3
              
    except:
      pass

  def control_machinecell(self):
    for x in machinecell:
      if self.version == 1:
        if [self.pos[0] + 50, self.pos[1], self.pos[2] + 50, self.pos[3]] == x.pos:
          self.moving = False
      elif self.version == 2:
        if [self.pos[0] - 50, self.pos[1], self.pos[2] - 50, self.pos[3]] == x.pos:
          self.moving = False
      elif self.version == 3:
        if [self.pos[0], self.pos[1] + 50, self.pos[2] - 50, self.pos[3] + 50] == x.pos:
          self.moving = False
      elif self.version == 4:
        if [self.pos[0], self.pos[1] - 50, self.pos[2] - 50, self.pos[3] - 50] == x.pos:
          self.moving = False
    
  def destroy(self):
    canvas.delete(self.id)
    canvas.delete(self.arrow)

  def control_buildcell(self):
    pass

class EnemyCell:
  def __init__(self, x, y,  x2, y2, color):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color, tag = "enemycell")

    self.pos = canvas.coords(self.id)

    self.mouth = canvas.create_arc(self.pos[0] + 14, self.pos[3] + 16, self.pos[2] - 14, self.pos[3] - 16, start = 22, extent = 135, style = "arc", fill = "#0b0b0b", outline = "#0b0b0b", width = 3)
    
    self.eye = canvas.create_oval(self.pos[0] + 14, self.pos[1] + 20, self.pos[0] + 18, self.pos[1] + 24, fill = "#0b0b0b", outline = "#0b0b0b")
    self.eyebrow = canvas.create_line(self.pos[0] + 11, self.pos[1] + 14, self.pos[0] + 24, self.pos[1] + 23, fill = "#0b0b0b", width = 3)

    self.eye2 = canvas.create_oval(self.pos[2] - 14, self.pos[1] + 19, self.pos[2] - 18, self.pos[1] + 23, fill = "#0b0b0b", outline = "#0b0b0b")
    self.eyebrow2 = canvas.create_line(self.pos[2] - 11, self.pos[1] + 13, self.pos[2] - 24, self.pos[1] + 22, fill = "#0b0b0b", width = 3)

  def destroy(self):
    canvas.delete(self.id)

    canvas.delete(self.mouth)
    
    canvas.delete(self.eye)
    canvas.delete(self.eyebrow)
    canvas.delete(self.eye2)
    canvas.delete(self.eyebrow2)
    
class TurnCell:
  def __init__(self, x, y, x2, y2, color, version):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color)

    self.pos = canvas.coords(self.id)

    self.version = version

    if self.version == 2:
      self.oval = canvas.create_oval(self.pos[0] + 9, self.pos[1] + 9, self.pos[2] - 9, self.pos[3] - 9, fill = color, width = 4, outline = "#ffffff")
      self.rectangle = canvas.create_rectangle(self.pos[0] + 25, self.pos[1] + 25, self.pos[2], self.pos[3], fill = color, outline = "")
      self.poly = canvas.create_polygon(self.pos[2] - 9, self.pos[3] - 17.5, self.pos[2] - 15, self.pos[3] - 25, self.pos[2] - 4, self.pos[1] + 25, fill = "#ffffff", outline = "#ffffff")

    self.selected = False

    canvas.tag_bind(self.id, "<Button-1>", self.select)

  def select(self):
    for x in buildcell:
      if x.pos == self.pos:
        self.selected = True

  def control(self):
    for x in pushcell:
      if x.pos == self.pos:

        canvas.delete(x.arrow)
        if self.version == 1:
          
          if x.x == 5 or x.x == -5:
            x.x = 0
            x.y = -5

            x.arrow = canvas.create_polygon(x.pos[2] - 33, x.pos[1] + 25, x.pos[2] - 20, x.pos[3] - 15, x.pos[2] - 20, x.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
            x.version = 4
          else:
            x.x = 5
            x.y = 0

            x.arrow = canvas.create_polygon(x.pos[0] + 33, x.pos[1] + 25, x.pos[0] + 20, x.pos[3] - 15, x.pos[0] + 20, x.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
            x.version = 0
        elif self.version == 2:
          
          if x.x == 5 or x.x == -5:
            x.x = 0
            x.y = 5

            x.arrow = canvas.create_polygon(x.pos[2] - 25, x.pos[1] + 33, x.pos[0] + 15, x.pos[1] + 20, x.pos[2] - 15, x.pos[1] + 20, fill = "#ffffff", outline = "#ffffff")
            x.version = 3
          else:
            x.x = -5
            x.y = 0

            x.arrow = canvas.create_polygon(x.pos[2] - 25, x.pos[3] - 33, x.pos[2] - 15, x.pos[3] - 20, x.pos[0] + 15, x.pos[3] - 20, fill = "#ffffff", outline = "#ffffff")
            x.version = 2

  def destroy(self):
    canvas.delete(self.id)
    canvas.delete(self.oval)
    canvas.delete(self.rectangle)
    canvas.delete(self.poly)

class NormalCell:
  def __init__(self, x, y, x2, y2, color, activefill):
    self.normalcell = canvas.create_rectangle(x, y, x2, y2, fill = color, tag = "nc", activefill = activefill)

    self.pos = canvas.coords(self.normalcell)

    self.selected = False

    canvas.tag_bind(self.normalcell, "<Button-1>", self.select)

  def select(self, evt):
    for x in buildcell:
      if x.pos == self.pos:
        self.selected = True

  def control(self):
    if not building:
      for x in range(len(enemycell)):
        if enemycell[x].pos == self.pos:

          enemycell[x].destroy()
          del enemycell[x]
          self.destroy()

          for x in range(len(normalcell)):
            if normalcell[x].pos == self.pos:
              del normalcell[x]

  def destroy(self):
    canvas.delete(self.normalcell)

class BounceCell:
  def __init__(self, x, y, x2, y2, color):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color)

    self.pos = canvas.coords(self.id)

    canvas.tag_bind(self.id, "<Button-1>", self.select)

    self.selected = False

  def select(self):
    for x in buildcell:
      if x.pos == self.pos:
        self.selected = True

  def destroy(self):
    canvas.delete(self.id)

class GeneratorCell:
  def __init__(self, x, y, x2, y2, color):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color, tag = "gc")

    self.pos = canvas.coords(self.id)

    self.line = canvas.create_rectangle(self.pos[0] + 10, self.pos[1] + 21, self.pos[2] - 10, self.pos[3] - 21, fill = "#ffffff", outline = "#ffffff")
    self.line2 = canvas.create_rectangle(self.pos[0] + 21, self.pos[1] + 10, self.pos[2] - 21, self.pos[3] - 10, fill = "#ffffff", outline = "#ffffff")

    self.selected = False

    canvas.tag_bind(self.id, "<Button-1>", self.select)
    canvas.tag_bind(self.line, "<Button-1>", self.select)
    canvas.tag_bind(self.line2, "<Button-1>", self.select)

  def select(self, evt):
    for x in buildcell:
      if x.pos == self.pos:
        self.selected = True

  def control(self):
    if building:
      for x in pushcell:
        for y in canvas.find_overlapping(x.pos[0], x.pos[1], x.pos[2], x.pos[3]):
          if canvas.find_withtag("gc")[0] in canvas.find_overlapping(x.pos[0], x.pos[1], x.pos[2], x.pos[3]) and not x.generator:

            x.moving = False

            if x.x == 5:
              version = 1
            elif x.x == -5:
              version = 2
            elif x.y == 5:
              version = 3
            elif x.y == -5:
              version = 4

            if version == 3:
              number = 0
              for y in canvas.find_withtag("id"):
                if not y in canvas.find_overlapping(self.pos[0], self.pos[1] + 50, self.pos[2], self.pos[3] + 50):
                  number += 1

              if number == len(canvas.find_withtag("id")):
                self.create_pushcell(self .pos[0], self.pos[1] + 50, self.pos[2], self.pos[3] + 50, "#4b78d7", version)
                  
            elif version == 4:
              number = 0
              for y in canvas.find_withtag("id"):
                if not y in canvas.find_overlapping(self.pos[0], self.pos[1] - 50, self.pos[2], self.pos[3] - 50):
                  number += 1

              if number == len(canvas.find_withtag("id")):
                self.create_pushcell(self .pos[0], self.pos[1] - 50, self.pos[2], self.pos[3] - 50, "#4b78d7", version)
                  
            elif version == 1:
              number = 0
              for y in canvas.find_withtag("id"):
                if not y in canvas.find_overlapping(self.pos[0] + 50, self.pos[1], self.pos[2] + 50, self.pos[3]):
                  number += 1

              if number == len(canvas.find_withtag("id")):
                self.create_pushcell(self .pos[0] + 50, self.pos[1], self.pos[2] + 50, self.pos[3], "#4b78d7", version)
                
            elif version == 2:
              number = 0
              for y in canvas.find_withtag("id"):
                if not y in canvas.find_overlapping(self.pos[0] - 50, self.pos[1], self.pos[2] - 50, self.pos[3]):
                  number += 1

              if number == len(canvas.find_withtag("id")):
                self.create_pushcell(self.pos[0] - 50, self.pos[1], self.pos[2] - 50, self.pos[3], "#4b78d7", version)

            x.touched_generator = True

  def destroy(self):
    canvas.delete(self.id)
    canvas.delete(self.line)
    canvas.delete(self.line2)

  def create_pushcell(self, x, y, x2, y2, color, version):
    pushcell.append(PushCell(x, y, x2, y2, color, version, 1, "#3b6ac2", True))

class BuildCell:
  def __init__(self, x, y, x2, y2, color, activefill):
    self.id = canvas.create_rectangle(x, y, x2, y2, fill = color)

    self.pos = canvas.coords(self.id)

    canvas.tag_bind(self.id, "<Button-1>", self.control_selected)

    self.fill = color
    self.activefill = activefill

    canvas.tag_bind(self.id, "<Enter>", self.hover)
    canvas.tag_bind(self.id, "<Leave>", self.leave)

  def hover(self, evt):
    for x in pushcell + normalcell + generatorcell + turncell + bouncecell:
      if x.selected:
        canvas.itemconfig(self.id, fill = self.activefill)

  def leave(self, evt):
    canvas.itemconfig(self.id, fill = self.fill)

  def control_selected(self, evt):
    for x in pushcell:
      if x.selected:
        canvas.coords(x.id, self.pos[0], self.pos[1], self.pos[2], self.pos[3])
        canvas.delete(x.arrow)

        if x.version == 1:
          x.arrow = canvas.create_polygon(self.pos[0] + 33, self.pos[1] + 25, self.pos[0] + 20, self.pos[3] - 15, self.pos[0] + 20, self.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
        elif x.version == 2:
          x.arrow = canvas.create_polygon(self.pos[2] - 33, self.pos[1] + 25, self.pos[2] - 20, self.pos[3] - 15, self.pos[2] - 20, self.pos[1] + 15, fill = "#ffffff", outline = "#ffffff")
        elif x.version == 3:
          x.arrow = canvas.create_polygon(self.pos[2] - 25, self.pos[1] + 33, self.pos[0] + 15, self.pos[1] + 20, self.pos[2] - 15, self.pos[1] + 20, fill = "#ffffff", outline = "#ffffff")
        else:
          x.arrow = canvas.create_polygon(self.pos[2] - 25, self.pos[3] - 33, self.pos[2] - 15, self.pos[3] - 20, self.pos[0] + 15, self.pos[3] - 20, fill = "#ffffff", outline = "#ffffff")

        x.selected = False
        x.pos = self.pos

    for x in normalcell:
      if x.selected:
        canvas.coords(x.normalcell, self.pos[0], self.pos[1], self.pos[2], self.pos[3])
        x.pos = self.pos

        x.selected = False

    for x in generatorcell:
      if x.selected:
        canvas.coords(x.id, self.pos[0], self.pos[1], self.pos[2], self.pos[3])
        canvas.delete(x.line)
        canvas.delete(x.line2)

        x.pos = canvas.coords(x.id)

        x.line = canvas.create_rectangle(self.pos[0] + 10, self.pos[1] + 21, self.pos[2] - 10, self.pos[3] - 21, fill = "#ffffff", outline = "#ffffff")
        x.line2 = canvas.create_rectangle(self.pos[0] + 21, self.pos[1] + 10, self.pos[2] - 21, self.pos[3] - 10, fill = "#ffffff", outline = "#ffffff")

        x.selected = False

  def destroy(self):
    canvas.delete(self.id)


def create_grid():

  data = buildcell_map(level + 1)

  for x in range(len(data[0])):
    for y in range(len(data)):

      if data[y][x] == 12:
        # Build Cell
        buildcell.append(BuildCell(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, "#4a4a4a", "#5e5e5e"))
      else:
        # Air Cell
        canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill = "#2e2e2d")

def create_map():
  global cx, cy

  data = load_level(level)

  cx = -1
  cy = -1

  for x in data:
    cy += 1
    cx = -1
    for y in x:
      cx += 1

      # Machine Cell
      if y == 1:
        machinecell.append(MachineCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#171717"))
                    
      # Push Cell
      if y == 2:
        pushcell.append(PushCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#4b78d7", 1, 0, "#3b6ac2", False))

      if y == 3:
        # Enemy
        enemycell.append(EnemyCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#ed2626"))

      if y == 4:
        # Turn Cell
        turncell.append(TurnCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#f58a1b", 1))

      if y == 5:
        # Normal Cell
        normalcell.append(NormalCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#3dbbd4", "#3fcce8"))

      if y == 6:
        # Push Cell 2
        pushcell.append(PushCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#4b78d7", 2, 0, "#3b6ac2", False))

      if y == 7:
        # Push Cell 3:
        pushcell.append(PushCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#4b78d7", 3, 0, "#3b6ac2", False))

      if y == 8:
        # Push Cell 4:
        pushcell.append(PushCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#4b78d7", 4, 0, "#3b6ac2", False))

      if y == 9:
        # Bounce Cell
        bouncecell.append(BounceCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#51e872"))

      if y == 10:
        # Generator Cell
        generatorcell.append(GeneratorCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#34e09b"))

      if y == 11:
        # Turn Cell 2
        turncell.append(TurnCell(cx * 50, cy * 50, (cx + 1) * 50, (cy + 1) * 50, "#f58a1b", 2))
        
def load_level(level):
  if level == 1:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 3, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 2:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 11, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 3:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 5, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 3, 0, 3, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 4:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 2, 0, 0, 0, 0, 1],
          [1, 3, 0, 0, 0, 0, 0, 0, 0, 9],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 5:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 10, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 3, 3, 3, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 2, 0, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 6:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 2, 0, 0, 0, 11, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 10, 1, 1, 0, 1],
          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
          [1, 1, 1, 1, 1, 3, 1, 1, 1, 1]]

def buildcell_map(level):
  if level == 1:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 2:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 3:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 4:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 5:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 12, 12, 0, 0, 0, 0, 1],
            [1, 0, 0, 12, 12, 0, 0, 0, 0, 1],
            [1, 0, 0, 12, 12, 0, 0, 0, 0, 1],
            [1, 0, 0, 12, 12, 0, 0, 0, 0, 1],
            [1, 0, 0, 12, 12, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  elif level == 6:
    return [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 12, 12, 12, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


# Startscreen
def startscreen():
  global machinecell, pushcell, enemycell, title, playbutton

  # Delete All
  for x in machinecell + pushcell + enemycell:
    x.destroy()

  # Cell Groups
  machinecell = []
  pushcell = []
  enemycell = []

  create_grid()

  title = canvas.create_text(250, 80, text = "Cyber Medication", fill = "#ed2626", font = "Helvetica 26 bold")

  playbutton = canvas.create_text(250, 180, text = "Play", fill = "#f5b342", font = "Helvetica 19 bold")

  canvas.tag_bind(playbutton, "<Button-1>", delete_startscreen)

def levellabel():
  global leveltext
  
  leveltext = canvas.create_text(50, 25, text = "", fill = "#ffffff", font = "Helvetica 19")

def startbutton():
  startbutton = canvas.create_text(444, 322, text = "start", fill = "#ffffff", font = "Helvetica 19")

  canvas.tag_bind(startbutton, "<Button-1>", start)

def start(evt):
  global building

  if get_clicked == level:
    building = False

    for x in pushcell:
      x.move()

    for x in buildcell:
      x.destroy()

def change_level():
  global leveltext

  if level > 5:
    canvas.itemconfig(leveltext, text = 'level: ' + str(level))

def next_level():
  global machinecell, pushcell, enemycell, turncell, normalcell, bouncecell, generatorcell, buildcell, level, tutorial_clicked, building

  level += 1

  for x in machinecell + pushcell + enemycell + turncell + normalcell + bouncecell + generatorcell + buildcell:
    x.destroy()

  # Cell Groups
  machinecell = []
  pushcell = []
  enemycell = []
  turncell = []
  normalcell = []
  bouncecell = []
  generatorcell = []
  buildcell = []

  change_level()

  create_grid()
  create_map()
  levellabel()
  startbutton()

  building = True

  tutorial_clicked += 1

  if level <= 5:
    tutorialtext()

def delete_startscreen(evt):
  canvas.delete(title)
  canvas.delete(playbutton)

  levellabel()
  next_level()

def tutorialtext():
  global get_clicked, tutorial_text, starting
  
  if level == 1:
    strings = ["zet de Push Cell ergens,", "waardat hij de kankercel kan doden", ""]
    tutorial_text = canvas.create_text(250, 75, text = "", fill = "#db4242", font = "Helvetica 16")

    show_text(strings)
      
    get_clicked += 1

  elif level == 2:
    strings = ["de oranje cel...", "is een Turn Cell,", "die zorgt ervoor dat...", "een Push Cell kan worden gedraaid", ""]

    show_text(strings)
          
    get_clicked += 1

  elif level == 3:
    strings = ["als een cel een kankercel dood,", "dan gaat hijzelf ook dood,", "daarom kan je...",  "een Normal Cell laten duwen...", "om twee kankercellen te doden", ""]

    show_text(strings)

    get_clicked += 1

  elif level == 4:
    strings = ["de groene cel...", "is een Bounce Cell", "als je ertegenaan botst,", "dan stuiter je terug", ""]

    show_text(strings)

    get_clicked += 1

  elif level == 5:
    strings = ["de blauwe cel...", "is een Generator", "als een blok ertegenaan botst,", "dan kopiëert het het blok", ""]

    show_text(strings)

    get_clicked += 1

def show_text(strings):
  for x in strings:
    for y in range(len(x) + 1):
      canvas.itemconfig(tutorial_text, text = x[0:y])
      time.sleep(0.05)

      canvas.tag_raise(tutorial_text)
      root.update()
    time.sleep(0.2)


startscreen()

try:
  while 1:
    for x in pushcell:
      x.control()
      x.control_normalcell()
      x.control_bouncecell()
      x.control_buildcell()
      x.control_machinecell()
      x.draw()

    for x in turncell:
      x.control()

    for x in normalcell:
      x.control()

    for x in generatorcell:
      x.control()

    if level <= 5 and tutorial_clicked > get_clicked:
      tutorialtext()

    time.sleep(0.01)
    root.update()
except:
  pass


root.mainloop()
