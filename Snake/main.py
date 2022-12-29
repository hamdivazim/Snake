from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
import random


kv = """
#:import random random
#:import MDLabel kivymd.uix.label.MDLabel
#:import Window kivy.core.window.Window


<SnakePart>:
    size: 40, 40
    canvas.before:
        Color:
            rgb: random.random(), random.random(), random.random()
        Rectangle:
            size: self.size
            pos: self.pos

<Danger>:
    size: 40, 40
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'danger.png'

<SnakeDetail>:
    size: 40, 40
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'right.jpg'


GameScreen:
    canvas.before:
        Color:
            rgb: 1,1,1
        Rectangle:
            size: self.size
            pos: self.pos
    Widget:
        size: 40, 40
        pos: 120, 120
        id: food
        canvas.before:
            Rectangle:
                size: self.size
                pos: self.pos
                source: 'apple.png'


"""

class SnakePart(Widget):
    type = StringProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'head' in kwargs.keys():
            if kwargs['head']:
                self.type = 'apple.png'

class SnakeDetail(Widget):
    type = StringProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'head' in kwargs.keys():
            if kwargs['head']:
                self.type = 'apple.png'    

class Danger(Widget):
    type = StringProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__()
        if 'head' in kwargs.keys():
            if kwargs['head']:
                self.type = 'apple.png'

class GameScreen(Widget):
    step_size = 40
    movement_x = 0
    movement_y = 0
    snake_parts = []
    dangers = []
    lose_life = False
    detail = None

    def new_game(self, restarted=False):
        lose_life = True
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
            if isinstance(child, Danger):
                to_be_removed.append(child)
            if isinstance(child, SnakeDetail):
                to_be_removed.append(child)
        for child in to_be_removed:
            if restarted:
                self.remove_widget(child)
            else:
                while child.y > 0:
                    child.y -= 20
                self.remove_widget(child)


        self.snake_parts = []
        self.dangers = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart(head=True)
        head.pos = (0, 0)
        self.snake_parts.append(head)
        self.add_widget(head)

        '''
        detail = SnakeDetail(head=True)
        detail.pos = (0, 0)
        self.detail = detail
        self.add_widget(detail)
        '''
        
        for i in range(3):
            danger = Danger()
            danger.x = randint(0, Window.width-danger.width)
            danger.y = randint(0, Window.height - danger.height)
            self.dangers.append(danger)
            self.add_widget(danger)
        lose_life = False

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            # Moving left or right
            self.movement_y = 0
            if dx > 0:
                self.movement_x = self.step_size
            else:
                self.movement_x = - self.step_size
        else:
            # Moving up or down
            self.movement_x = 0
            if dy > 0:
                self.movement_y = self.step_size
            else:
                self.movement_y = - self.step_size

    def collides_widget(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

    def next_frame(self, *args):       
        # Move the snake
        head = self.snake_parts[0]
        food = self.ids.food
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y

        # Move the body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.new_y = self.snake_parts[i-1].y
            part.new_x = self.snake_parts[i-1].x
        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x

        # Move the head
        head.x += (self.movement_x)
        head.y += self.movement_y

        '''

        self.detail.x = head.x + 20
        self.detail.y += self.movement_y

        '''




        # Check for snake colliding with food
        if self.collides_widget(head, food):
            food.x = randint(0, Window.width-food.width)
            food.y = randint(0, Window.height - food.height)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)

        # Check for snake colliding with itself
        for part in self.snake_parts[1:]:
            if self.collides_widget(part, head):
                self.new_game()

        # Check for snake colliding with danger
        for danger in self.dangers:
            if self.collides_widget(danger, head):
                self.new_game()

        # Check for snake colliding with wall
        if not self.collides_widget(self, head):
            self.new_game()

        '''

        # Change detail sprite
        if self.movement_x == 0:
            pass
        elif self.movement_x > 0:
            self.detail.source = 'right.jpg'
        elif self.movement_x < 0:
            self.detail.source = 'left.jpg'
        '''

        #print(self.detail.source)

class MainApp(MDApp):
    def on_start(self):
        #SoundLoader.load('music.mp3').play()
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, 1/10.)
        Clock.schedule_interval(self.play_music, 4.22)

    def play_music(self, obj=None):
        if self.root.lose_life:
            SoundLoader.load('Lose Life.wav').play()
        else:
            SoundLoader.load('music.mp3').play()

    def build(self):
        self.title = 'Snake!'
        return Builder.load_string(kv)


MainApp().run()
