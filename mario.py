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
P = pipe_color
mario_lives = 3             # How many lives does the bird get?
mario_size = 1       # 
debug_mode = True
loc = 0
jump = 3
mario_vert = 6
jumping = False

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

####
# Game functions
####

def draw_map(dir,map,maprows):
  debug_message("(re)drawing map)")
  global loc
  global O
  global G
  global P
  move = collision_check(G,P,map,maprows)
  #starting_cols = len(columns)
  debug_message(move)
  #move columns based on direction check if at end/beg
  if move == False or dir == "none":
    debug_message("stay still")
  else:
    if dir == "right" and loc != maprows-8:
      loc = loc +1
    elif dir == "left" and loc != 0:
      loc = loc -1

  
  for x in range(8):
    for y in range(8):
      sense.set_pixel(x,y, map[(x+loc)+(y*maprows)]) # this does the math to get the right Number from the index(creating fake rows and columns)


def collision_check(G,P,map,maprows):
  #get pixel in front of mario
  global mario_vert
  global loc
  next = map[(loc+2)+(mario_vert*maprows)]
  if next == G or next == P:
    return False
  else:
    return True
  
"""
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
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, G, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, G, G, O, O, O, O, O, O, O, G, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
G, G, G, G, G, G, G, G, G, O, G, G, G, G, G, G, G, G, G,
]
map1rows = 19

draw_map("none",map1,map1rows)
sense.set_pixel(1,6, mario_color)
sleep(1)
while True:
  events = sense.stick.get_events()
  if events:
    for e in events:
      debug_message("Processing joystick events")
      if e.direction ==  right_key and e.action == pressed:
        # User pressed up: move bird up and columns over
        debug_message("Joystick right press detected")
        draw_map("right",map1,map1rows)
        sense.set_pixel(1,mario_vert, mario_color)
      elif e.direction ==  left_key and e.action == pressed:
        # User pressed up: move bird up and columns over
        debug_message("Joystick left press detected")
        draw_map("left",map1,map1rows)
        sense.set_pixel(1,mario_vert, mario_color)
