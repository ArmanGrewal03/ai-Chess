import pygame
from dragger import Dragger
from constants import *
from board import Board
from config import Config
from square import Square



class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_square=None
        self.board=Board()
        self.dragger=Dragger()
        self.config=Config()

    def bg(self,surface):
        theme=self.config.theme
        for row in range(ROWS):
            for col in range(COL):
                if (row+col) %2 ==0:
                    color=theme.bg.light#light green
                else:
                    color=theme.bg.dark#dark green

                rect=(col*SQSIZE,row*SQSIZE,SQSIZE,SQSIZE)#this creates a rectangle with poitioning(defined by col/row*SQSIZE) and size defined by SQSIZE
                pygame.draw.rect(surface,color,rect)#draw rectangle on surface with color

                if col ==0:
                    color=theme.bg.dark if row%2==0 else theme.bg.light
                    label=self.config.font.render(str(ROWS-row),1,color)
                    label_pos=(5,5+row*SQSIZE)
                    surface.blit(label,label_pos)

                if row ==7:
                    color=theme.bg.dark if (row+col)%2==0 else theme.bg.light
                    label=self.config.font.render(Square.get_alphacol(col),1,color)
                    label_pos=(col*SQSIZE+SQSIZE-20,HEIGHT-20)
                    surface.blit(label,label_pos)

    
    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COL):
                #look for pieces 
                if self.board.squares[row][col].has_piece():
                    piece=self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img=pygame.image.load(piece.texture)
                        img_center=col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2#centers image
                        piece.texture_rect=img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)

    def show_moves(self,surface):
        theme=self.config.theme
       
        if self.dragger.dragging:
            piece=self.dragger.piece

            for move in piece.moves:
                if (move.final.row+move.final.col)%2==0:
                    color=theme.moves.light
                else:
                    color=theme.moves.dark

                rect=(move.final.col*SQSIZE,move.final.row*SQSIZE,SQSIZE,SQSIZE)


                pygame.draw.rect(surface,color,rect)

    def next_turn(self):
        self.next_player='white' if self.next_player=='black' else 'black'
    
    def show_last_move(self,surface):
        theme=self.config.theme
        if self.board.last_move:
            initial=self.board.last_move.initial
            final=self.board.last_move.final

            for pos in (initial,final):
                color=theme.trace.light if (pos.row+pos.col)%2==0 else theme.trace.dark
                rect=(pos.col*SQSIZE,pos.row*SQSIZE,SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)


    def show_hover(self,surface):
        if self.hovered_square:
            color=(180,180,180) 
            rect=(self.hovered_square.col*SQSIZE,self.hovered_square.row*SQSIZE,SQSIZE,SQSIZE)
            pygame.draw.rect(surface,color,rect,width=3)

                
    def set_hover(self,row,col):
        if 0 <= row < ROWS and 0 <= col < COL:
            self.hovered_square = self.board.squares[row][col]
        else:
            self.hovered_square = None

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self,captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()
