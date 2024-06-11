from turtle import position
import pygame
import math
import colorsys

class Board:
    def __init__(self,*, position,size,padding, version='english') -> None:
        self.__pos = position
        self.__size = size
        self.__padding = padding

        self.__ball_radius = (size- (8*padding))//14

        self.__moving = (-1,-1)
        self.__is_dragging = False

        self.__hue = 0

        self.reset_board(version)

    def __check_for_legal_moves(self,pos):
        i,j = pos
        if i - 2 >= 0:
            if self.board[i-2][j] == 0 and self.board[i-1][j]:
                return True

        if i + 2 < 7:
            if self.board[i+2][j] == 0 and self.board[i+1][j]:
                return True

        if j - 2 >= 0:
            if self.board[i][j-2] == 0 and self.board[i][j-1]:
                return True

        if j + 2 < 7:
            if self.board[i][j+2] == 0 and self.board[i][j+1]:
                return True
        
        return False


    def check_game_status(self):        
        b = 0
        last_ball_pos = 0,0
        for i in range(7):
            for j in range(7):
                if self.board[i][j] != -1:
                    b += self.board[i][j]

                    if self.board[i][j] == 1:
                        last_ball_pos = i,j
                        if self.__check_for_legal_moves((i,j)):
                            return 0
                        
        if b == 1:
            if (self.__version == 'english' and last_ball_pos == (3,3)) or (self.__version == 'french' and last_ball_pos == (6,4)):
                return 1
        return -1



    def show(self,screen,mouse_pos,game_status):
        pygame.draw.rect(screen, (50,50,255), (self.__pos,(self.__size,self.__size)),0,5)
        if game_status == 1:
            for i in range(7):
                for j in range(7):
                    if self.board[i][j] != -1:
                        center = (self.__pos[0] + (j+1)*self.__padding + (2*j+1)*self.__ball_radius,self.__pos[1] + (i+1)*self.__padding + (2*i+1)*self.__ball_radius)
                        if ((i != 3 or j != 3) and self.__version == 'english') or ((i != 6 or j != 4) and self.__version == 'french') :
                            s = 0.2+(math.dist(center,(self.__pos[0]+self.__size//2, self.__pos[1]+self.__size//2))/(math.sqrt(2*(self.__size**2))//2))*0.8
                            theta = math.acos((center[0]-(self.__pos[0]+self.__size//2))/math.dist(center,(self.__pos[0]+self.__size//2, self.__pos[1]+self.__size//2)))
                            color = colorsys.hsv_to_rgb((((self.__hue)%360)/180)*3.14 +theta,s,1)
                            color = int(color[0]*255),int(color[1]*255),int(color[2]*255)
                        else: 
                            color = 230,230,230    
                        
                        pygame.draw.circle(screen, color, center, self.__ball_radius)
            self.__hue+=1
            
        else:
            for i in range(7):
                for j in range(7):
                    if self.board[i][j] != -1:
                        center = (self.__pos[0] + (j+1)*self.__padding + (2*j+1)*self.__ball_radius,self.__pos[1] + (i+1)*self.__padding + (2*i+1)*self.__ball_radius)
                        if self.board[i][j] == 1 and not ((i,j)==(self.__moving) and self.__is_dragging):
                            pygame.draw.circle(screen, (230,230,230), center, self.__ball_radius)
                        else:
                            pygame.draw.circle(screen, (0,0,0), center, self.__ball_radius)

            if self.__is_dragging:
                pygame.draw.circle(screen, (230,230,230), mouse_pos, self.__ball_radius)

    def __get_ball_by_pos(self,pos):
        for i in range(7):
            for j in range(7):
                center = (self.__pos[0] + (j+1)*self.__padding + (2*j+1)*self.__ball_radius,self.__pos[1] + (i+1)*self.__padding + (2*i+1)*self.__ball_radius)
                if math.dist(pos, center) < self.__ball_radius:
                    return (i,j)
        return (-1,-1)

    def pick(self,position):
        ball = self.__get_ball_by_pos(position)
        if self.board[ball[0]][ball[1]] == 1:
            self.__is_dragging = True
            self.__moving = ball

    def release(self, position):
        if self.__is_dragging:
            newpos = self.__get_ball_by_pos(position)
            if self.board[newpos[0]][newpos[1]] == 0:
                dx = abs(newpos[0]-self.__moving[0])
                dy = abs(newpos[1]-self.__moving[1])

                if (dx == 0 and dy == 2) or (dx == 2 and dy == 0):
                    if self.board[(newpos[0]+self.__moving[0])//2][(newpos[1]+self.__moving[1])//2] == 1:
                        self.board[(newpos[0]+self.__moving[0])//2][(newpos[1]+self.__moving[1])//2] = 0
                        self.board[self.__moving[0]][self.__moving[1]] = 0
                        self.board[newpos[0]][newpos[1]] = 1 
            
            self.__is_dragging = False


    def reset_board(self, version='english'):
        self.__version = version
        self.__is_dragging = False
        self.board = [[1 for _ in range(7)] for _ in range(7)]
        
        
        for i in range(2):
            for j in range(2):
                self.board[i][j] = -1
                self.board[5+i][j] = -1
                self.board[i][5+j] = -1
                self.board[5+i][5+j] = -1

        if version == 'english':
            self.board[3][3] = 0
        elif version == 'french':
            self.board[0][2] = 0
            self.board[1][1] = 1
            self.board[1][5] = 1
            self.board[5][5] = 1
            self.board[5][1] = 1
        else:
            raise Exception("Invalid game version")


        