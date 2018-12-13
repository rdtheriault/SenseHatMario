import sense_hat
from time import sleep, time
from random import randint

sense = sense_hat.SenseHat()
sense.clear()

"""

"""

# Edit these variables to change key game parameters
mario_color = (255,0,0)       
bg_color = (0,0,0)          
O = bg_color
gumba_color = (200,200,0)    
floor_color = (102, 51, 0 )   
G = floor_color
pipe_color = (0,255,0)
P = pipe_color
castle = (204, 153, 0)
C = castle
end = (255, 255, 0)
E = end

mario_lives = 3
death = False
mario_size = 1
debug_mode = True
loc = 0                       #beginning location
jump = 2                      #how high mario can jump
jumpHolder = 0
mario_vert = 6                #beg vertical (7 is floor)
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
  #debug_message("(re)drawing map)")
  global loc, O, G, P, death, mario_lives
  move = collision_check(map,maprows)
  #debug_message(move)
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
  
  #draw mario
  jumpMario("none", map, maprows)
  fallMario(dir, map, maprows)
  sense.set_pixel(1,mario_vert, mario_color)
  
  if death == True:
    reset()
    mario_lives = mario_lives - 1
    
  beatLLevel(map,maprows)
  
def collision_check(map,maprows):
  #get pixel in front of mario
  global mario_vert
  global loc
  next = map[(loc+2)+(mario_vert*maprows)]
  if next == G or next == P:
    return False
  else:
    return True
  
def jumpMario(btn,map,maprows):
  #debug_message("jump")
  global mario_vert, jump, jumpHolder, jumping, loc, G , P
  under = map[(loc+1)+((mario_vert+1)*maprows)]
  #debug_message(under)
  #if button up and not already jumping and there is something to jump off of
  if jumping == False and btn == "start" and (under == G or under == P):
    debug_message("start jump")
    jumping = True
  elif jumping == False and btn == "none":
    debug_message("not jumping")
  elif jumping == True:
    if jumpHolder == jump:#stop jumping
      jumping = False
      jumpHolder = 0
    else:
      jumpHolder = jumpHolder + 1
      mario_vert = mario_vert - 1
      
def fallMario(dir,map,maprows):
  global jumping, mario_vert, gumba_color, last_move, loc, death, G, P, E
  under = map[(loc+1)+((mario_vert+1)*maprows)]

  if jumping == False:
    #debug_message("falling")
    if under == G or under == P or under == E:
      debug_message("stop falling")
    elif under == gumba_color:
      debug_message("kill gumba")
    else:
      mario_vert = mario_vert + 1
      if mario_vert == 7:
        death = True
  
def move_gumba():
  debug_message("moving gumba")

def reset():
  global loc, jump, jumpHolder, mario_vert, jumping, death
  loc = 0                       #beginning location
  jump = 2                      #how high mario can jump
  jumpHolder = 0
  mario_vert = 6                #beg vertical (7 is floor)
  jumping = False
  death = False


def beatLLevel(map,maprows):
  global E
  under = map[(loc+1)+((mario_vert+1)*maprows)]
  if under == E:
    sense.show_message("You won")
    reset()

#### Levels ####

map1 = [
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, G, O, O, O, O, O, O, O, O, O, O, O, O, O, C, O, C, O, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, C, C, C, O, O, O, O, O,
O, O, O, O, G, G, O, O, O, O, O, O, O, G, O, O, O, P, O, O, O, O, O, O, O, O, O, C, C, O, C, C, O, O, O, O,
O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, O, P, O, O, O, O, O, O, O, O, O, C, C, O, C, C, O, O, O, O,
G, G, G, G, G, G, G, G, G, O, G, G, G, G, G, G, G, G, G, G, O, G, G, G, G, G, G, G, G, E, G, G, G, G, G, G,
]
map1rows = 36

draw_map("none",map1,map1rows)
sense.set_pixel(1,6, mario_color)
sleep(1)

####
# Main Game Loop
####

while True:
  sleep(0.1)
  events = sense.stick.get_events()
  if events:
    for e in events:
      debug_message("Processing joystick events")
      if e.direction ==  right_key and e.action == pressed:
        # User pressed up: move bird up and columns over
        debug_message("Joystick right press detected")
        draw_map("right",map1,map1rows)
      elif e.direction ==  left_key and e.action == pressed:
        # User pressed up: move bird up and columns over
        debug_message("Joystick left press detected")
        draw_map("left",map1,map1rows)
      elif e.direction ==  up_key and e.action == pressed:
        debug_message("Joystick up press detected")
        jumpMario("start",map1,map1rows)
  sleep(0.1)
  draw_map("none",map1,map1rows)
