from turtle import bgcolor
from matplotlib.pyplot import text
import pygame
from requests import options

class Button:
    def __init__(self,text, position, size):
        self.__text = text
        self.__pos = position
        self.__size = size

        self.__options = []

        self.__hidden = True

    def add_option(self, text, function, par):
        self.__options.append([text,function,par,0])

    def show(self,screen, font):
        bg_color = 200,200,200
        text_color = 30,30,30

        pygame.draw.rect(screen, bg_color, pygame.Rect(self.__pos, self.__size), 0, 4)
        pygame.draw.rect(screen, [150]*3, pygame.Rect(self.__pos, self.__size), 2, 4)

        cx = self.__pos[0] + int(self.__size[0]/2)
        cy = self.__pos[1] + int(self.__size[1]/2)
        
        texts = font.render(str(self.__text), False, text_color)
                
        offset_x = int(texts.get_rect().width/2)
        offset_y = int(texts.get_rect().height/2)
        screen.blit(texts,(cx-offset_x, cy-offset_y))

        if not self.__hidden:
            top = self.__pos[1] - len(self.__options)*self.__size[1]
            for o in self.__options:
                new_bg_color = [bg_color[0]-o[3]]*3
                pygame.draw.rect(screen, new_bg_color, pygame.Rect(self.__pos[0], top, *self.__size), 0, 4)
                pygame.draw.rect(screen, [150]*3, pygame.Rect(self.__pos[0], top, *self.__size), 2, 4)
                
                cx = self.__pos[0] + int(self.__size[0]/2)
                cy = top + int(self.__size[1]/2)
                
                texts = font.render(str(o[0]), False, text_color)

                offset_x = int(texts.get_rect().width/2)
                offset_y = int(texts.get_rect().height/2)
                screen.blit(texts,(cx-offset_x, cy-offset_y))

                top = top+self.__size[1]

    def update(self, mouse_pos):
        x,y = mouse_pos
        left = self.__pos[0]
        right = self.__pos[0]+self.__size[0]
        bottom = self.__pos[1]+self.__size[1]
        if self.__hidden:
            top = self.__pos[1]
        else:
            top = self.__pos[1] - len(self.__options)*self.__size[1]

        if x < left or x > right or y < top or y > bottom:
            self.__hidden = True
        else:
            self.__hidden = False
            op = (mouse_pos[1]-top)//self.__size[1]
            
            for i in range(len(self.__options)):
                if i == op:
                    self.__options[i][3] = min(50,self.__options[i][3]+3)
                else:
                    self.__options[i][3] = max(0,self.__options[i][3]-3)


    def click(self, mouse_pos):
        top = self.__pos[1] - len(self.__options)*self.__size[1]
        op = (mouse_pos[1]-top)//self.__size[1]
        if op < len(self.__options):
            self.__options[op][1](self.__options[op][2])
            self.__hidden = True

    def is_open(self):
        return not self.__hidden