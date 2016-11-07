import random
import json
import time
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
    PIXEL_PER_METER = (5.0 / 0.1)  # 픽셀/미터
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 미터/분
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8


    image = None

    UP_RUN,DOWN_RUN,UP_STAND,DOWN_STAND= 0, 1, 2, 3

    def __init__(self):
        self.x,self.y = random.randint(250,1024),719
        self.xdir,self.ydir = 0, 0
        self.frame = random.randint(0,4)
        self.run_frames = 0
        self.stand_frames = 0
        self.total_frames = 0.0
        self.state = self.UP_RUN
        if Enermy1.image == None:
            self.image = load_image('enermy1.png')


    def handle_up_run(self):
        self.ydir = 1
        self.run_frames += 1
        if self.y > 700:
            self.state = self.DOWN_RUN
            self.y = 700
        if self.run_frames == 40:
            self.state = self.UP_STAND
            self.stand_frames = 0

    def handle_up_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 100:
            self.state = self.UP_RUN
            self.run_frames = 0

    def handle_down_run(self):
        self.ydir = -1
        self.run_frames += 1
        if self.y < 50:
         self.state = self.UP_RUN
         self.y = 50
        if self.run_frames == 20:
         self.state = self.DOWN_STAND
         self.stand_frames = 0

    def handle_down_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 100:
            self.state = self.DOWN_RUN
            self.run_frames = 0

    handle_state = {
        UP_RUN : handle_up_run,
        DOWN_RUN : handle_down_run,
        UP_STAND: handle_up_stand,
        DOWN_STAND:handle_down_stand
    }
    def update(self,frame_time):
        distance = Enermy1.RUN_SPEED_PPS * frame_time
        self.total_frames += Enermy1.FRAMES_PER_ACTION * Enermy1.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)




    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 80, self.x, self.y)

class Boy:

    PIXEL_PER_METER = (10.0 / 0.1)  # 픽셀/미터
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 미터/분
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    image = None

    LEFT_RUN, RIGHT_RUN, UP_RUN, DOWN_RUN, STAND = 0,1,2,3,4

    def __init__(self):
        self.x, self.y = 50,300
        self.xdir,self.ydir = 0,0
        self.frame = random.randint(0,7)
        self.total_frames = 0.0
        self.state = self.STAND
        if self.image == None:
            self.image = load_image('Ayin.png')

    def update(self,frame_time):
        distance = Boy.RUN_SPEED_PPS * frame_time
        self.total_frames += Boy.FRAMES_PER_ACTION * Boy.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)





    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def handle_event(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if self.state in (self.LEFT_RUN,self.UP_RUN,self.DOWN_RUN,self.STAND):
                    self.state = self.RIGHT_RUN
                    self.xdir = 1
            elif event.key == SDLK_LEFT:
                if self.state in (self.RIGHT_RUN,self.UP_RUN,self.DOWN_RUN,self.STAND):
                    self.state = self.LEFT_RUN
                    self.xdir = -1
            elif event.key == SDLK_UP:
                if self.state in (self.DOWN_RUN,self.LEFT_RUN,self.RIGHT_RUN,self.STAND):
                    self.state = self.UP_RUN
                    self.ydir = 1
            elif event.key == SDLK_DOWN:
                if self.state in (self.UP_RUN,self.LEFT_RUN,self.RIGHT_RUN,self.STAND):
                    self.state = self.DOWN_RUN
                    self.ydir = -1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if self.state in (self.STAND,self.RIGHT_RUN,self.UP_RUN,self.DOWN_RUN):
                    self.state = self.STAND
                    self.xdir = 0
            elif event.key == SDLK_LEFT:
                if self.state in (self.STAND,self.LEFT_RUN,self.UP_RUN,self.DOWN_RUN):
                    self.state = self.STAND
                    self.xdir = 0
            elif event.key == SDLK_UP:
                if self.state in (self.STAND,self.LEFT_RUN,self.RIGHT_RUN,self.UP_RUN):
                    self.state = self.STAND
                    self.ydir = 0
            elif event.key == SDLK_DOWN:
                if self.state in (self.STAND,self.LEFT_RUN,self.RIGHT_RUN,self.DOWN_RUN):
                    self.state = self.STAND
                    self.ydir = 0




def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)



def enter():
    global boy,map,enermy1
    open_canvas(1024,720)
    boy = Boy()
    map = Map()
    enermy1 = Enermy1()
    pass


def exit():
    global boy,map,enermy1
    del(boy)
    del(map)
    del(enermy1)
    close_canvas()
    pass


def update(frame_time):
    boy.update(frame_time)
    enermy1.update(frame_time)




def draw(frame_time):
    clear_canvas()
    map.draw()
    boy.draw()
    enermy1.draw()
    update_canvas()

