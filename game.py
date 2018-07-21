#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random
from menu import Menu

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

WHITE = (255,255,255)
BLACK = (0,0,0)

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font("kenvector_future_thin.ttf",50)
        self.menu = Menu(("start","about","exit"),font_color=WHITE,font_size=50,ttf_font="kenvector_future.ttf")
        self.show_about_frame = False # True: display about frame of the menu
        self.show_menu = True # True: when we are playing the game
        # Create ball object
        self.ball = Ball(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
        # Create the player
        self.player = Player(50,SCREEN_HEIGHT / 2)
        # Create the enemy
        self.enemy = Enemy(SCREEN_WIDTH - 65,SCREEN_HEIGHT / 2)
        # Load beep sound
        self.beep_sound = pygame.mixer.Sound("sfx_sounds_Blip3.ogg")
        # Count the score of the player
        self.player_score = 0
        # Count the score of the enemy
        self.enemy_score = 0
        

    def process_events(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.show_menu and not self.show_about_frame:
                        if self.menu.state == 0:
                            self.show_menu = False
                            self.game_init()
                        elif self.menu.state == 1:
                            self.show_about_frame = True
                        elif self.menu.state == 2:
                            # User clicked exit
                            return True
                elif event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.show_about_frame = False

                elif event.key == pygame.K_UP:
                    self.player.go_up()
                elif event.key == pygame.K_DOWN:
                    self.player.go_down()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.stop()
            
        return False

    def run_logic(self):
        if not self.show_menu:
            self.ball.update()
            self.player.update(self.ball,self.beep_sound)
            self.enemy.update(self.ball,self.beep_sound)
            if self.ball.rect.x < 0:
                self.ball.reset()
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.enemy_score += 1
            elif self.ball.rect.x > SCREEN_WIDTH:
                self.ball.reset()
                self.player.rect.centery = SCREEN_HEIGHT / 2
                self.player_score += 1

    def game_init(self):
        # Return to the initial values
        # Set ball in the center of the screen
        self.ball.rect.centerx = SCREEN_WIDTH / 2
        self.ball.rect.centery = SCREEN_HEIGHT / 2
        # Set ball change_x and change_y initial values
        self.ball.change_x = -5
        self.ball.change_y = 0
        # Set player and enemy in the initial position
        self.player.rect.centery = SCREEN_HEIGHT / 2
        self.enemy.rect.centery = SCREEN_HEIGHT / 2
        # Set scores to 0
        self.player_score = 0
        self.enemy_score = 0
        
        

    def display_frame(self,screen):
        # First, clear the screen to white. Don't put other drawing commands
        screen.fill(BLACK)
        time_wait = False # True: when we have to wait at the end 
        # --- Drawing code should go here
        if self.show_menu:
            if self.show_about_frame:
                # Display the about frame
                self.display_message(screen,"By Edu Grando")
            else:
                # Display the menu
                self.menu.display_frame(screen)

        # Check if the player won the game
        elif self.player_score == 10:
            self.display_message(screen,"You Won!",WHITE)
            time_wait = True
            self.player_score = 0
            self.enemy_score = 0
            self.show_menu = True
            
        # Check if the enemy won the game
        elif self.enemy_score == 10:
            self.display_message(screen,"You lost",WHITE)
            time_wait = True
            self.player_score = 0
            self.enemy_score = 0
            self.show_menu = True
        else:
            # Display the game
            self.ball.draw(screen)
            self.player.draw(screen)
            self.enemy.draw(screen)
            # Draw center line
            for y in range(0,SCREEN_HEIGHT,20):
                pygame.draw.rect(screen,WHITE, [SCREEN_WIDTH / 2, y, 10, 10])
            # Draw the score
            player_score_label = self.font.render(str(self.player_score),True,WHITE)
            screen.blit(player_score_label,(270,10))
            enemy_score_label = self.font.render(str(self.enemy_score),True,WHITE)
            screen.blit(enemy_score_label,(350,10))
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- This is for the game to wait a few seconds to display the message
        if time_wait:
            pygame.time.wait(3000)

    def display_message(self,screen,message,color=(255,0,0)):
        label = self.font.render(message,True,color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)
        # Draw the label onto the screen
        screen.blit(label,(posX,posY))

class Ball(object):
    def __init__(self,x,y):
        # Create rect to represent the position of the ball
        self.rect = pygame.Rect(x,y,12,12)
        self.change_x = 0
        self.change_y = 0

    def update(self):
        # Check for limits
        if self.rect.top < 0:
            self.change_y *= -1
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.change_y *= -1
            self.rect.bottom = SCREEN_HEIGHT
        # Move left/right
        self.rect.x += self.change_x
        # Move up/down
        self.rect.y += self.change_y

    def reset(self):
        # Return to initial values
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2
        self.change_x = -5
        self.change_y = random.randint(-3,3)

    def draw(self,screen):
        pygame.draw.rect(screen,WHITE,self.rect)

class Player(object):
    def __init__(self,x,y):
        # Create rect to represent the position of the player
        self.rect = pygame.Rect(x,y,15,50)
        self.change = 0

    def update(self,ball,beep_sound):
        # Check for limits
        if self.rect.top <= 0 and self.change < 0:
            self.change = 0
        elif self.rect.bottom >= SCREEN_HEIGHT and self.change > 0:
            self.change = 0
        # Check if we hit the ball
        if self.rect.colliderect(ball.rect):
            # Change change_y to a random number between -5 and 5
            ball.change_y = random.randint(-5,5)
            ball.change_x *= -1
            ball.rect.left = self.rect.right
            # Play effect sound
            beep_sound.play()
        # Move up/down
        self.rect.y += self.change

    def go_up(self):
        self.change = -5

    def go_down(self):
        self.change = 5

    def stop(self):
        self.change = 0

    def draw(self,screen):
        # Draw the rectangle onto the screen
        pygame.draw.rect(screen,WHITE,self.rect)

class Enemy(object):
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,15,50)

    def update(self,ball,beep_sound):
        if self.rect.centery > ball.rect.centery:
            diff = self.rect.centery - ball.rect.centery
            if diff <= 4:
                self.rect.centery = ball.rect.centery
            else:
                self.rect.y -= 4
        elif self.rect.centery < ball.rect.centery:
            diff = ball.rect.centery - self.rect.centery
            if diff <= 4:
                self.rect.centery = ball.rect.centery
            else:
                self.rect.y += 4
        # Check if we hit the ball
        if self.rect.colliderect(ball.rect):
            ball.change_x *= -1
            ball.rect.right = self.rect.left
            # Play effect sound
            beep_sound.play()

    def draw(self,screen):
        # Draw the rectangle onto the screen
        pygame.draw.rect(screen,WHITE,self.rect)
        
