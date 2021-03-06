import random
from pico2d import *
import game_framework
import title_state

name = 'Main'

boy = None
grass = None
font = None

class Map:
    def __init__(self):
       self.image = load_image('forest.png')

    def draw(self):
        self.image.draw(512,360)

class Enermy1:
    image = None

    UP_RUN, DOWN_RUN = 0, 1


    def handle_up_run(self):
        self.y += 2
        if self.y > 720:
            self.state = self.DOWN_RUN
            self.y = 720



    def handle_down_run(self):
        self.y -= 2
        if self.y < 0:
            self.state = self.UP_RUN
            self.y = 0

    handle_state = {
        UP_RUN : handle_up_run,
        DOWN_RUN : handle_down_run
    }
    def update(self):
        self.handle_state[self.state](self)



    def __init__(self):
        self.x,self.y = random.randint(250,1024),719
        self.frame = random.randint(0,7)
        self.state = self.UP_RUN
        if Enermy1.image == None:
            self.image = load_image('enermy1.png')



    def draw(self):
        self.image.draw(self.x, self.y)

class Boy:
    image = None

    LEFT_RUN, RIGHT_RUN, UP_RUN, DOWN_RUN, STAND = 0,1,2,3,4

    def __init__(self):
        self.x, self.y = 50,300
        self.frame = 0
        self.state = self.RIGHT_RUN
        if self.image == None:
            self.image = load_image('Ayin.png')

    def update(self):
        self.frame = (self.frame + 1) % 6
        if self.state == self.RIGHT_RUN:
            self.x = min(1024, self.x + 5)
        elif self.state == self.LEFT_RUN:
            self.x = max(0,self.x - 5)
        elif self.state == self.DOWN_RUN:
            self.y = max(0,self.y - 5)
        elif self.state == self.UP_RUN:
            self.y = min(720,self.y + 5)



    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def handle_event(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if self.state in (self.LEFT_RUN,self.UP_RUN,self.DOWN_RUN,self.STAND):
                    self.state = self.RIGHT_RUN
            elif event.key == SDLK_LEFT:
                if self.state in (self.RIGHT_RUN,self.UP_RUN,self.DOWN_RUN,self.STAND):
                    self.state = self.LEFT_RUN
            elif event.key == SDLK_UP:
                if self.state in (self.DOWN_RUN,self.LEFT_RUN,self.RIGHT_RUN,self.STAND):
                    self.state = self.UP_RUN
            elif event.key == SDLK_DOWN:
                if self.state in (self.UP_RUN,self.LEFT_RUN,self.RIGHT_RUN,self.STAND):
                    self.state = self.DOWN_RUN
        elif event.type == SDL_KEYUP:
            self.state = self.STAND


def enter():
    global boy,map,enermy1
    open_canvas(1024,720)
    boy = Boy()
    map = Map()
    enermy1 = Enermy1()
    pass


def exit():
    global boy,map
    del(boy)
    del(map)
    del(enermy1)
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)





def update():
    boy.update()
    enermy1.update()

    pass


def draw():
    clear_canvas()
    map.draw()
    boy.draw()
    enermy1.draw()
    update_canvas()
    pass
