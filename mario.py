import sense_hat
from time import sleep, time
from random import randint

sense = sense_hat.SenseHat()
sense.clear()

"""

"""

# Edit these variables to change key game parameters
mario_color = (255,0,0)      # 
bg_color = (0,0,0)          #
O = bg_color
gumba_color = (200,200,0)   # 
floor_color = (102, 51, 0 )   #
G = floor_color
pipe_color = (0,255,0)
bird_y = 2                 # Where the player starts 
mario_lives = 3             # How many lives does the bird get?
mario_size = 1       # 
jump = 3
debug_mode = False
loc = 0
mario_vert = 0

# Variables for convenience and readability
up_key = sense_hat.DIRECTION_UP
down_key = sense_hat.DIRECTION_DOWN
left_key = sense_hat.DIRECTION_LEFT
right_key = sense_hat.DIRECTION_RIGHT
pressed = sense_hat.ACTION_PRESSED

# Initial settings - should be no need to alter these
speed = 0
game_over = False
setup = True
moved = False
column_interval = 10

# Debug functions: pause or print messages if debug_mode is set to True
def debug_message(message):
  if debug_mode:
    print(message)


#set up game board


"""
# Get true color values for comparisons: get_pixel() sometimes returns different values
sense.set_pixel(0,0, col_color)
col_color = sense.get_pixel(0,0)
sense.set_pixel(0,0, bg_color)
bg_color = sense.get_pixel(0,0)
sense.set_pixel(0,0, bird_color)
bird_color = sense.get_pixel(0,0)
sense.clear()

# Save setup in a tuple to restart game
reset_state = (col_color, bg_color, bird_color, bird_y, bird_lives, columns, column_speed_base, speed, game_over)
"""
####
# Game functions
####

def draw_map(dir,map,map1rows):
  debug_message("Moving columns")
  global loc
  global O
  global G
  move = True
  #starting_cols = len(columns)
  
  #move columns based on direction check if at end/beg
  if dir == "right":
    loc = loc +1
  elif dir == "left":
    if loc == 0:
      move = False
    else:
      loc = loc -1
  elif dir == "none":
    move = False
  
  for x in range(8):
    for y in range(8):
      sense.set_pixel(x,y, map[(x+loc)+(y*map1rows)])
  
"""
def draw_column(col, custom_color = None):
  debug_message("Drawing column")
  
  if custom_color:
    back_color = custom_color
  else:
    back_color = bg_color

  # Construct a list of column color and background color tuples, then set those pixels
  x, gap_start, gap_size = col
  c = [col_color] * 8
  c[gap_start - gap_size: gap_start] = [back_color] * gap_size
  for y, color in enumerate(c):   
    sense.set_pixel(x,y,color)

def draw_bird(falling = True):
  debug_message("drawing bird")
  global bird_y, bird_lives, game_over
  # Replace bird with upcoming background or column at x=4
  sense.set_pixel(3,bird_y,sense.get_pixel(3, bird_y))
  
  if falling:
    bird_y += speed

  # Stay onscreen
  if bird_y > 7:
    bird_y = 7
  if bird_y < 0:
    bird_y = 0
  
  # Collisions are when the bird moves onto a column
  hit = sense.get_pixel(3, bird_y) == col_color
  if hit:
    flash_screen()
    bird_lives -= 1
    # ignore any keypresses here
    sense.stick.get_events()
  
  # Draw bird lives
  if bird_lives > 8:
    # Can only draw 8 at a time
    draw_lives = 8
  else:
    draw_lives = bird_lives
    
  for i in range(draw_lives):
    sense.set_pixel(0,i, (200,200,200))
  
  game_over = bird_lives < 0
  
  # Draw bird in new position
  sense.set_pixel(3,bird_y,bird_color)
  debug_message("Bird drawn")

def flash_screen():
  for i in range(3):
    custom_color = ([randint(50, x) for x in [255,255,255]])
    draw_screen(custom_color)
    # Make sure bird is still visible
    sense.set_pixel(3,bird_y,bird_color)
    sleep(.1)
  draw_screen()

####
# Main Game Loop
####

while True:

  if setup:
    col_color, bg_color, bird_color, bird_y, bird_lives, columns, column_speed_base, speed, game_over = reset_state
    # Initial screen setup
    last_redraw = round(time(), 1) * column_interval
    draw_screen()
    draw_bird()
    
    # Clear joystick events
    sense.stick.get_events()
    column_speed = int(column_speed_base)
    
    setup = False
  
  column_tick = round(time(), 1) * column_interval

  if (column_tick % (column_interval - column_speed) == 0) and (column_tick > last_redraw):
    # Enough time has passed: columns move 
    debug_message("Tick!")
    speed = 1
    # make columns faster if possible as game goes on
    if column_interval > (column_speed + 2):
      column_speed = column_speed_base + len(columns) // (column_interval * 3)

    move_columns()
    draw_screen()
    draw_bird()
    debug_message("Tick length: " + str(column_tick - last_redraw) \
                   + " Speed: " + str(column_speed)\
                   + "Columns: " + str(len(columns)))
    last_redraw = column_tick

  events = sense.stick.get_events()
  if events:
    for e in events:
      debug_message("Processing joystick events")
      if e.direction ==  up_key and e.action == pressed:
        # User pressed up: move bird up and columns over
        debug_message("Joystick up press detected")
        move_columns()
        draw_screen()
        speed = -1
        draw_bird()
        moved = True
        # Prevent double falls
        last_redraw -= column_interval // 2
  else:
    moved = False
    
  if game_over:
    flash_screen()
      
    # Score is number of columns survived
    score = len(columns) - 2 
    sense.show_message(str(score) + "pts!", text_colour=(255,255,255))
    
    # Start over
    setup = True
"""




map1 = [
O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O,
O, O, O, O, G, G, O, O, O,
O, O, O, O, O, O, O, O, O,
G, G, G, G, G, G, G, G, G,
]
map1rows = 9

draw_map("none",map1,map1rows)
sense.set_pixel(1,6, mario_color)
sleep(1)
draw_map("right",map1,map1rows)
sense.set_pixel(1,6, mario_color)
