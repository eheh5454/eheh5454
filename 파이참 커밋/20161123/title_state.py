import game_framework
import main
from pico2d import *


name = "TitleState"
image = None

class Map:

    image = None

    def __init__(self):
      self.bgm = load_music('Resource\\sound\\tengai.ogg')
      self.bgm.set_volume(24)
      self.bgm.repeat_play()
      if Map.image == None:
          self.image = load_image('title2.png')

    def draw(self):
        self.image.draw(400,300)

def enter():
    global image,map
    map = Map()



    pass


def exit():
    global image,map
    del(map)
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type,event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main)

    pass


def draw(frame_time):
    clear_canvas()
    map.draw()
    update_canvas()
    pass







def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass






