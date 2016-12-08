import random
import time
from pico2d import *
import game_framework
import title_state

name = 'Main'

player = None
grass = None
font = None


Attack_List = []
Explode_List = []
EnemyAttack_List = []
Attack_List2 = []

class Time:
    def __init__(self):
        self.time_one = 0.0
        self.time_two = 0.0
        self.time_three = 0.0
        self.time_four = 0.0

    def update(self,frame_time):
        self.time_one += frame_time
        self.time_two += frame_time
        self.time_three += frame_time
        self.time_four += frame_time
        self.create_enemy1()
        self.create_enemy2()
        self.create_enemy3()
        self.create_enemy4()




    def create_enemy1(self):
        if (self.time_one >= 2):
            new_enemy1 = Enemy1()
            Enemy_1.append(new_enemy1)
            self.time_one = 0.0

    def create_enemy2(self):
        if (self.time_two >= 4):
            new_enemy2 = Enemy2()
            Enemy_2.append(new_enemy2)
            self.time_two = 0.0

    def create_enemy3(self):
        if (self.time_three >= 6):
            new_enemy3 = Enemy3()
            Enemy_3.append(new_enemy3)
            self.time_three = 0.0

    def create_enemy4(self):
        if (self.time_four >= 8):
            new_enemy4 = Enemy4()
            Enemy_4.append(new_enemy4)
            self.time_four = 0.0


class Map:
    PIXEL_PER_METER = (10.0 / 0.1)  # 10 pixel 30 cm
    SCROLL_SPEED_KMPH = 20.0  # Km / Hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self,w,h):
       self.left = 0
       self.speed = 0
       self.screen_width = w
       self.screen_height = h
       self.bgm = load_music('Resource\\sound\\BGM.mp3')
       self.bgm.set_volume(24)
       self.bgm.repeat_play()
       if Map.image == None:
           self.image = load_image('Resource\\BackGround\\forest.png')

    def draw(self):
        x = int(self.left)
        w = min(self.image.w - x, self.screen_width)
        self.image.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
        self.image.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)


    def update(self,frame_time):
        self.left = (self.left + frame_time * self.speed) % self.image.w
        self.speed = Map.SCROLL_SPEED_PPS

class Enemy1:
    PIXEL_PER_METER = (10.0 / 0.3)  # 픽셀/미터
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 미터/분
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    ENEMYATTACK_CREATE = 0.5


    image = None

    UP_RUN,DOWN_RUN,UP_STAND,DOWN_STAND= 0, 1, 2, 3

    def __init__(self):
        self.x,self.y = random.randint(250,1024),719
        self.xdir,self.ydir = 0, 0
        self.frame = random.randint(0,4)
        self.run_frames = 0
        self.stand_frames = 0
        self.total_frames = 0.0
        self.missile_count = 0
        self.name = 'enemy1'
        self.state = self.UP_RUN
        self.hp = 10
        self.LIFE = 1
        if Enemy1.image == None:
            self.image = load_image('Resource\\Enemy\\EnemyOne.png')


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
        distance = Enemy1.RUN_SPEED_PPS * frame_time
        self.total_frames += Enemy1.FRAMES_PER_ACTION * Enemy1.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)
        self.missile_count += frame_time * self.ENEMYATTACK_CREATE
        if self.missile_count > 1:
            self.missile_count = 0
            enemy_missile = EnemyAttack(self.x - 50, self.y - 10)
            EnemyAttack_List.append(enemy_missile)

    def hp_drop(self, drop_hp):   ##hp 추가
         self.hp -= drop_hp
         if (self.hp <= 0):
              self.LIFE = 0
              return self.LIFE
         else:
             return self.LIFE



    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 80, self.x, self.y)

    def get_bb(self):
        return self.x - 1,self.y - 50,self.x+1 ,self.y + 50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Enemy2:
    PIXEL_PER_METER = (10.0 / 0.3)  # 픽셀/미터
    RUN_SPEED_KMPH = 30.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 미터/분
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    ENEMYATTACK_CREATE = 0.5



    image = None

    UP_RUN,DOWN_RUN,UP_STAND,DOWN_STAND,FRONT_RUN= 0, 1, 2, 3, 4

    def __init__(self):
        self.x,self.y = random.randint(250,800),719
        self.xdir,self.ydir = 0, 0
        self.frame = random.randint(0,4)
        self.run_frames = 0
        self.stand_frames = 0
        self.total_frames = 0.0
        self.missile_count = 0
        self.state = self.UP_RUN
        self.hp = 20
        self.LIFE = 1
        if Enemy2.image == None:
            self.image = load_image('Resource\\Enemy\\EnemyTwo.png')


    def handle_front_run(self):
        self.xdir = -1
        self.ydir = 0.1
        if self.x < 200:
            self.state = self.DOWN_RUN


    def handle_up_run(self):
        self.ydir = 1
        self.run_frames += 1
        if self.y > 700:
            self.state = self.DOWN_RUN
            self.y = 700
        if self.run_frames == 40:
            self.state = self.UP_STAND
            self.stand_frames = 0
        if self.x > 1000:
            self. state = self.FRONT_RUN


    def handle_up_stand(self):
        self.stand_frames += 1
        if self.stand_frames == 100:
            self.state = self.UP_RUN
            self.run_frames = 0

    def handle_down_run(self):
        self.ydir = -1
        self.xdir = 0.1
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
        DOWN_STAND:handle_down_stand,
        FRONT_RUN:handle_front_run
    }
    def update(self,frame_time):
        distance = Enemy2.RUN_SPEED_PPS * frame_time
        self.total_frames += Enemy2.FRAMES_PER_ACTION * Enemy2.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 7
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)
        self.missile_count += frame_time * self.ENEMYATTACK_CREATE
        if self.missile_count > 1:
            self.missile_count = 0
            enemy_missile = EnemyAttack(self.x - 50, self.y - 10)
            EnemyAttack_List.append(enemy_missile)

    def hp_drop(self, drop_hp):   ##hp 추가
         self.hp -= drop_hp
         if (self.hp <= 0):
              self.LIFE = 0
              return self.LIFE
         else:
             return self.LIFE

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 80, self.x, self.y)

    def get_bb(self):
        return self.x - 1,self.y - 50,self.x + 1,self.y + 50

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Enemy3:
    PIXEL_PER_METER = (10.0 / 0.3)  # 픽셀/미터
    RUN_SPEED_KMPH = 25.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 미터/분
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    ENEMYATTACK_CREATE = 1

    image = None

    RIGHT_RUN,LEFT_RUN,UP_RUN, = 0,1,2

    def __init__(self):
        self.x,self.y = random.randint(250,1024),719
        self.xdir,self.ydir = 0, 0
        self.frame = random.randint(0,4)
        self.run_frames = 0
        self.stand_frames = 0
        self.total_frames = 0.0
        self.state = self.RIGHT_RUN
        self.missile_count = 0
        self.hp = 25
        self.LIFE = 1
        if Enemy3.image == None:
            self.image = load_image('Resource\\Enemy\\EnemyThree.png')


    def handle_right_run(self):
        self.ydir = -0.5
        self.xdir = 0.5
        if self.x > 900:
            self.state = self.LEFT_RUN
            self.x = 900
        if self.y < 0:
            self.state = self.UP_RUN
            self.y = 0

    def handle_left_run(self):
        self.ydir = -0.5
        self.xdir = -0.5
        self.run_frames += 1
        if self.x < 50:
         self.state = self.RIGHT_RUN
         self.x = 50
        if self.y < 0:
            self.state = self.UP_RUN
            self.y = 0

    def handle_up_run(self):
        self.ydir = 1
        if self.y > 700:
            self.state = self.RIGHT_RUN
            self.y = 700

    handle_state = {
        RIGHT_RUN:handle_right_run,
        LEFT_RUN:handle_left_run,
        UP_RUN:handle_up_run
    }
    def update(self,frame_time):
        distance = Enemy3.RUN_SPEED_PPS * frame_time
        self.total_frames += Enemy3.FRAMES_PER_ACTION * Enemy3.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 4
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)
        self.missile_count += frame_time * self.ENEMYATTACK_CREATE
        if self.missile_count > 1:
            self.missile_count = 0
            enemy_missile = EnemyAttack(self.x - 50, self.y - 10)
            EnemyAttack_List.append(enemy_missile)

    def hp_drop(self, drop_hp):   ##hp 추가
         self.hp -= drop_hp
         if (self.hp <= 0):
              self.LIFE = 0
              return self.LIFE
         else:
             return self.LIFE

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 75, self.x, self.y)

    def get_bb(self):
        return self.x - 1, self.y - 40, self.x + 1, self.y + 40

class Enemy4:
    PIXEL_PER_METER = (5.0 / 0.1)  # 픽셀/미터
    RUN_SPEED_KMPH = 40.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 미터/분
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 2
    ACTION_PER_TIME = 2.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    ENEMYATTACK_CREATE = 0.5

    image = None

    RIGHT_RUN,LEFT_RUN = 0,1

    def __init__(self):
        self.x = random.randint (100,500)
        self.y = random.randint (100,600)
        self.xdir,self.ydir = 0, 0
        self.frame = random.randint(0,4)
        self.total_frames = 0.0
        self.state = self.RIGHT_RUN
        self.missile_count = 0
        self.hp = 15
        self.LIFE = 1
        if Enemy4.image == None:
            self.image = load_image('Resource\\Enemy\\EnemyFour.png')


    def handle_right_run(self):
        self.xdir = 1
        if self.x > 1000:
            self.state = self.LEFT_RUN
            self.x = 1000

    def handle_left_run(self):
        self.xdir = -1
        if self.x < 50:
           self.state = self.RIGHT_RUN
           self.x = 50



    handle_state = {
        RIGHT_RUN:handle_right_run,
        LEFT_RUN:handle_left_run,

    }
    def update(self,frame_time):
        distance = Enemy4.RUN_SPEED_PPS * frame_time
        self.total_frames += Enemy4.FRAMES_PER_ACTION * Enemy4.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)
        self.handle_state[self.state](self)
        self.missile_count += frame_time * self.ENEMYATTACK_CREATE
        if self.missile_count > 1:
            self.missile_count = 0
            enemy_missile = EnemyAttack(self.x - 50, self.y - 10)
            EnemyAttack_List.append(enemy_missile)

    def hp_drop(self, drop_hp):   ##hp 추가
         self.hp -= drop_hp
         if (self.hp <= 0):
              self.LIFE = 0
              return self.LIFE
         else:
             return self.LIFE

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 80, self.x, self.y)

    def get_bb(self):
        return self.x - 1, self.y - 30, self.x + 1, self.y + 30

class Player:

    PIXEL_PER_METER = (10.0 / 0.3)  # 픽셀/미터
    RUN_SPEED_KMPH = 50.0
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
        self.hp = 10
        self.LIFE = 1
        self.frame = random.randint(0,7)
        self.total_frames = 0.0
        self.state = self.STAND
        self.font = load_font('a우주소년.TTF',120)
        self.font2 = load_font('a우주소년.TTF',35)
        if self.image == None:
            self.image = load_image('Ayin.png')


    def update(self,frame_time):
        distance = player.RUN_SPEED_PPS * frame_time
        self.total_frames += player.FRAMES_PER_ACTION * player.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 6
        self.x += (self.xdir * distance)
        self.y += (self.ydir * distance)

        self.x = clamp(50, self.x, 1100)
        self.y = clamp(50, self.y, 660)




    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        if (self.LIFE == 0):
            self.font.draw(250,360,'Game over')
        self.font2.draw(100,600,'HP: %d' % (self.hp))

    def get_bb(self):
        return self.x, self.y -10, self.x + 25, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

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

    def get_attack(self):
        if (score.score >= 100):
            newattack = Attack(self.x + 50, self.y)
            Attack_List.append(newattack)
        elif (score.score < 100):
            newattack = Attack2(self.x  + 50, self.y)
            Attack_List2.append(newattack)

    def get_special(self):
        newattack = SpecialAttack(self.x + 50,self.y)
        SpecialAttack_List.append(newattack)


    def hp_drop(self, drop_hp):   ##hp 추가
         self.hp -= drop_hp
         if (self.hp <= 0):
              self.LIFE = 0
              return self.LIFE
         else:
             return self.LIFE

class Attack:
    PIXEL_PER_METER = (25.0/ 0.3)
    RUN_SPEED_KMPH = 100.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    eat_sound = None
    attackshot_sound = None

    def __init__(self,x,y):
        self.x,self.y = x,y
        self.xdir = 1
        if self.image == None:
            self.image = load_image('Resource\\Missile\\AyinMissile_Moon.png')
        if Attack.eat_sound == None:
            Attack.eat_sound = load_wav('Resource\\Sound\\Explode.wav')
            Attack.eat_sound.set_volume(100)
        if Attack.attackshot_sound == None:
            Attack.attackshot_sound = load_wav('Resource\\Sound\\attack.wav')
            Attack.attackshot_sound.set_volume(128)


    def eat(self):  ##폭발음
        self.eat_sound.play()

    def attackshot(self):  ##발사음
        self.attackshot_sound.play()

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
             player.get_attack()
             self.attackshot()



    def update(self,frame_time):
        distance = Attack.RUN_SPEED_PPS * frame_time
        self.x += (self.xdir*distance)

        if(self.x > 1100):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x,self.y)

    def get_bb(self):
        return  self.x - 1,self.y - 55,self.x + 25,self.y + 55

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Attack2:
    PIXEL_PER_METER = (25.0/ 0.3)
    RUN_SPEED_KMPH = 100.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None
    eat_sound = None
    attackshot_sound = None

    def __init__(self,x,y):
        self.x,self.y = x,y
        self.xdir = 1
        if self.image == None:
            self.image = load_image('Resource\\Missile\\AyinMissile_Arrow.png')
        if Attack2.eat_sound == None:
            Attack2.eat_sound = load_wav('Resource\\Sound\\Explode.wav')
            Attack2.eat_sound.set_volume(100)
        if Attack2.attackshot_sound == None:
            Attack2.attackshot_sound = load_wav('Resource\\Sound\\attack.wav')
            Attack2.attackshot_sound.set_volume(128)


    def eat(self):  ##폭발음
        self.eat_sound.play()

    def attackshot(self):  ##발사음
        self.attackshot_sound.play()

    def handle_events(self,event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
             player.get_attack()
             self.attackshot()



    def update(self,frame_time):
        distance = Attack2.RUN_SPEED_PPS * frame_time
        self.x += (self.xdir*distance)

        if(self.x > 1100):
            return True
        else:
            return False

    def draw(self):
        self.image.draw(self.x,self.y)

    def get_bb(self):
        return  self.x - 1,self.y - 55,self.x + 25,self.y + 55

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
        
class SpecialAttack:

    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 40.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    ATTACK_STATE = 0

    image = None
    ayinspecialattack_sound = None

    def __init__(self,x,y):
        self.x, self.y = x,y
        self.attackcount = 5
        self.xdir = 1
        self.frame = 0
        self.total_frames = 0.0
        self.state = self.ATTACK_STATE
        self.skilltime = 0.0
        self.font = load_font('a우주소년.TTF',30)
        if SpecialAttack.image == None:
            SpecialAttack.image = load_image('제목 없음-1.png')
        if SpecialAttack.ayinspecialattack_sound == None:
            SpecialAttack.ayinspecialattack_sound = load_wav('Resource\\Sound\\AyinSpecialAttack.wav')
            SpecialAttack.ayinspecialattack_sound.set_volume(48)

    def ayinspecialattack(self):
        self.ayinspecialattack_sound.play()

    def handle_events(self, event):
        if (self.attackcount > 0):
            if event.type == SDL_KEYDOWN and event.key == SDLK_s:
                player.get_special()
                self.attackcount -= 1



    def update(self, frame_time):
        distance = SpecialAttack.RUN_SPEED_PPS * frame_time
        self.x += (self.xdir * distance)



    def draw(self):
        self.image.clip_draw(self.frame * 400, 0, 400, 208, self.x, self.y)


    def get_bb(self):
        return self.x - 100, self.y -100, self.x + 25, self.y + 120

    def draw_bb(self):
        draw_rectangle(*self.get_bb())



class EnemyAttack:

    PIXEL_PER_METER = (25.0 / 0.3)
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xdir = -1
        if EnemyAttack.image == None:
            EnemyAttack.image = load_image('Resource\\Missile\\EnemyMissile.png')

    def update(self, frame_time):
        distance = EnemyAttack.RUN_SPEED_PPS * frame_time
        self.x += (self.xdir * distance)

        if(self.x < -50) :
            return True
        else :
            return False

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y -10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Explode: ##폭발 이펙트

    TIME_PER_ACTION = 0.7
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 15

    explode_sound = None
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.total_frames = 0.0
        self.life_time = 0.0
        if Explode.image == None :
            Explode.image = load_image('Resource\\Enemy\\Explode.png')
        if self.explode_sound == None:
            self.explode_sound = load_wav('Resource\\Sound\\Explode.wav')
            self.explode_sound.set_volume(6)

    def update(self, frame_time):
        self.life_time += frame_time
        self.total_frames += Explode.FRAMES_PER_ACTION * Explode.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 15
        self.explode()
        if (self.frame == 14):
            return True
        else:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 128, 0, 128, 180, self.x, self.y)

    def explode(self):
        self.explode_sound.play()


class Score: ##점수
    def __init__(self):
        self.score = 0
        self.font = load_font('a우주소년.TTF',35)

    def draw(self):
        self.font.draw(100,650,'Score: %d' % (self.score))
        self.font.draw(50, 50, 'SpecialAttack: %d' % (specialattack.attackcount))


    def score_get(self):
        self.score += 5






def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)
            attack.handle_events(event)
            attack2.handle_events(event)
            specialattack.handle_events(event)

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True





def enter():
    global time,SpecialAttack_List,player,map,attack,Enemy_1,Enemy_2,Enemy_3,Enemy_4,score,Explode_List,EnemyAttack_List,Attack_List,attack2,Attack_List2,specialattack
    open_canvas(1024,720)
    player = Player()
    score = Score()
    map = Map(1024,720)

    time = Time()

    attack = Attack(0,0)
    attack2 = Attack2(0,0)
    specialattack = SpecialAttack(0,0)

    Enemy_1 = []
    Enemy_2 = []
    Enemy_3 = []
    Enemy_4 = []
    Attack_List = []
    Attack_List2 = []
    Explode_List = []
    EnemyAttack_List = []
    SpecialAttack_List=[]





def exit():
    global time,SpecialAttack_List,player,map,attack,Enemy_1,Enemy_2,Enemy_3,Enemy_4,score,Explode_List,EnemyAttack_List,Attack_List,Attack_List2,attack2,specialattack
    del(time)
    del(player)
    del(map)
    del(Enemy_1)
    del(Enemy_2)
    del(Enemy_3)
    del(Enemy_4)
    del(Attack_List)
    del(Attack_List2)
    del(SpecialAttack_List)
    del(attack)
    del(attack2)
    del(specialattack)
    del(score)
    del(Explode_List)
    del(EnemyAttack_List)
    close_canvas()
    pass


def update(frame_time):
    time.update(frame_time)
    map.update(frame_time)
    player.update(frame_time)

    for enemy1 in Enemy_1:
        enemy1.update(frame_time)
    for enemy2 in Enemy_2:
        enemy2.update(frame_time)
    for enemy3 in Enemy_3:
        enemy3.update(frame_time)
    for enemy4 in Enemy_4:
        enemy4.update(frame_time)

    for explode in Explode_List:
        explode.update(frame_time)
        explode_end = explode.update(frame_time)
        if explode_end == True :
            Explode_List.remove(explode)

    for enemymissile in EnemyAttack_List:
        enemymissile.update(frame_time)
        out_side = enemymissile.update(frame_time)
        if out_side == True:
            EnemyAttack_List.remove(enemymissile)

    for attack in Attack_List:
        attack.update(frame_time)

    for attack2 in Attack_List2:
        attack2.update(frame_time)

    for specialattack in SpecialAttack_List:
        specialattack.update(frame_time)




##*************************충돌처리*************************##

##적군과 플레이어 충돌
    for enemy1 in Enemy_1:
        if collide(enemy1,player):
            if(player.LIFE == 1):
                player.hp_drop(1)
                player.x -= 50
            if(player.LIFE == 0):
                player.x = -300

    for enemy2 in Enemy_2:
        if collide(enemy2, player):
             if (player.LIFE == 1):
                 player.hp_drop(1)
                 player.x -= 50
             if (player.LIFE == 0):
                 player.x = -300

    for enemy3 in Enemy_3:
        if collide(enemy3, player):
             if (player.LIFE == 1):
                 player.hp_drop(1)
                 player.x -= 50
             if (player.LIFE == 0):
                 player.x = -300

    for enemy4 in Enemy_4:
        if collide(enemy4, player):
              if (player.LIFE == 1):
                  player.hp_drop(1)
                  player.x -= 50
              if (player.LIFE == 0):
                  player.x = -300





##적군 공격과 플레이어 충돌
    for enemymissile in EnemyAttack_List:
        if collide(enemymissile,player):
            if (player.LIFE == 1):
                player.hp_drop(1)
                player.x -= 50
            if (player.LIFE == 0):
                player.x = 1100



 ##플레이어 공격과 적군 충돌

    for attack in Attack_List:
        for enemy1 in Enemy_1:
           if collide(attack,enemy1):
               if (enemy1.LIFE == 1):
                   enemy1.hp_drop(1)
               if (enemy1.LIFE ==0):
                   Enemy_1.remove(enemy1)
                   attack.eat()
                   score.score_get()
                   enemy_one_explode = Explode(enemy1.x, enemy1.y)
                   Explode_List.append(enemy_one_explode)

    for attack in Attack_List:
       for enemy2 in Enemy_2:
          if collide(attack,enemy2):
              if (enemy2.LIFE == 1):
                  enemy2.hp_drop(1)
              if (enemy2.LIFE == 0):
                  Enemy_2.remove(enemy2)
                  attack.eat()
                  score.score_get()
                  enemy_two_explode = Explode(enemy2.x, enemy2.y)
                  Explode_List.append(enemy_two_explode)

    for attack in Attack_List:
        for enemy3 in Enemy_3:
          if collide(attack,enemy3):
              if (enemy3.LIFE == 1):
                  enemy3.hp_drop(1)
              if (enemy3.LIFE == 0):
                  Enemy_3.remove(enemy3)
                  attack.eat()
                  score.score_get()
                  enemy_three_explode = Explode(enemy3.x, enemy3.y)
                  Explode_List.append(enemy_three_explode)

    for attack in Attack_List:
        for enemy4 in Enemy_4:
          if collide(attack,enemy4):
              if (enemy4.LIFE == 1):
                  enemy4.hp_drop(1)
              if (enemy4.LIFE == 0):
                  Enemy_4.remove(enemy4)
                  attack.eat()
                  score.score_get()
                  enemy_four_explode = Explode(enemy4.x, enemy4.y)
                  Explode_List.append(enemy_four_explode)
 #플레이어 공격2와 적군 충돌
    for attack2 in Attack_List2:
        for enemy1 in Enemy_1:
           if collide(attack2,enemy1):
               if (enemy1.LIFE == 1):
                   enemy1.hp_drop(1)
               if (enemy1.LIFE ==0):
                   Enemy_1.remove(enemy1)
                   attack2.eat()
                   score.score_get()
                   enemy_one_explode = Explode(enemy1.x, enemy1.y)
                   Explode_List.append(enemy_one_explode)

    for attack2 in Attack_List2:
       for enemy2 in Enemy_2:
          if collide(attack2,enemy2):
              if (enemy2.LIFE == 1):
                  enemy2.hp_drop(1)
              if (enemy2.LIFE == 0):
                  Enemy_2.remove(enemy2)
                  attack2.eat()
                  score.score_get()
                  enemy_two_explode = Explode(enemy2.x, enemy2.y)
                  Explode_List.append(enemy_two_explode)

    for attack2 in Attack_List2:
        for enemy3 in Enemy_3:
          if collide(attack2,enemy3):
              if (enemy3.LIFE == 1):
                  enemy3.hp_drop(1)
              if (enemy3.LIFE == 0):
                  Enemy_3.remove(enemy3)
                  attack2.eat()
                  score.score_get()
                  enemy_three_explode = Explode(enemy3.x, enemy3.y)
                  Explode_List.append(enemy_three_explode)

    for attack2 in Attack_List2:
        for enemy4 in Enemy_4:
          if collide(attack2,enemy4):
              if (enemy4.LIFE == 1):
                  enemy4.hp_drop(1)
              if (enemy4.LIFE == 0):
                  Enemy_4.remove(enemy4)
                  attack2.eat()
                  score.score_get()
                  enemy_four_explode = Explode(enemy4.x, enemy4.y)
                  Explode_List.append(enemy_four_explode)

    ##필살기와 적군 충돌





def draw(frame_time):
    clear_canvas()
    map.draw()
    score.draw()

    for enemy1 in Enemy_1:
        enemy1.draw()
    for enemy2 in Enemy_2:
        enemy2.draw()
    for enemy3 in Enemy_3:
        enemy3.draw()
    for enemy4 in Enemy_4:
        enemy4.draw()
    for explode in Explode_List:
        explode.draw()
    for enemyattack in EnemyAttack_List:
        enemyattack.draw()
    for attack in Attack_List:
        attack.draw()
    for attack2 in Attack_List2:
        attack2.draw()
    for specialattack in SpecialAttack_List:
        specialattack.draw()
    player.draw()


    update_canvas()

