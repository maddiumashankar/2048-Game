import pygame
import random
import math

pygame.init()

FPS=60 #Framespersecond how quickly the game is running

Width,Height=400,400

Rows=4
Cols=4

Rectangular_height=Height//Rows
Rectangular_width=Width//Cols

Outline_color=(187,173,160)

Outline_thickness=10

Background_color=(205,192,180)

Font_color=(119,110,101)

Font=pygame.font.SysFont("comicsans",60,bold=True)
Move_vel=20

Window=pygame.display.set_mode((Width,Height))

pygame.display.set_caption("2048")


class Tile:
    COLORS=[
        [237,229,218],
        [238,225,201],
        [243,178,122],
        [246,150,101],
        [247,124,95],
        [247,95,59],
        [237,208,115],
        [237,204,99],
        [236,202,80]
    ]

    def __init__(self,value,row,col):
        self.row=row
        self.col=col
        self.value=value
        self.x=col*Rectangular_width
        self.y=row*Rectangular_height
    
    def get_color(self):
        color_index=int(math.log2(self.value))
        color=self.COLORS[color_index]
        return color
    
    def draw(self,window):
        color=self.get_color()
        pygame.draw.rect(window,color,(self.x,self.y,Rectangular_width,Rectangular_height))
        text=Font.render(str(self.value),True,Font_color)
        window.blit(text,
                    (self.x+(Rectangular_width/2-text.get_width()/2),
                    self.y+(Rectangular_height/2-text.get_height()/2)),
                     
                    ),
   
   
    def set_pos(self,ceil=False):
        if ceil:
            self.row=math.ceil(self.y/Rectangular_height)
            self.col=math.ceil(self.x/Rectangular_width)
        else:
            self.row=math.floor(self.y/Rectangular_height)
            self.col=math.floor(self.x/Rectangular_width)
    def move(self,delta):
        self.x+=delta[0]
        self.y+=delta[1]


def draw_grid(window):

    for row in range(1,Rows):
        y=row*Rectangular_height
        pygame.draw.line(window,Outline_color,(0,y),(Width,y),Outline_thickness)
    
    for col in range(1,Cols):
        x=col*Rectangular_width
        pygame.draw.line(window,Outline_color,(x,0),(x,Height),Outline_thickness) 
    
    
    
    pygame.draw.rect(window,Outline_color,(0,0,Width,Height),Outline_thickness)



def draw(window,tiles):
    window.fill(Background_color)

    for tile in tiles.values():
        tile.draw(window)


    draw_grid(window)
    pygame.display.update()

def get_random_pos(tiles):
    row=None
    col=None
    while True:
        row=random.randrange(0,Rows)
        col=random.randrange(0,Cols)
        if f"{row}{col}" not in tiles:
            break
    return row,col

def generate_tiles():
    tiles={}
    for _ in range(2):
        row,col=get_random_pos(tiles)
        tiles[f"{row}{col}"]=Tile(2,row,col)
    return tiles

def move_tiles(window,tiles,clock,direction):
    updated=True
    blocks=set()
    if direction =="left":
        sort_func=lambda x:x.col 
        reverse=False
        delta=(-Move_vel,0)
        Boundary_check=lambda tile:tile.col==0
        get_next_tile=lambda tile:tiles.get(f"{tile.row}{tile.col-1}")
        merge_check=lambda tile,next_tile: tile.x>next_tile.x+Move_vel 
        move_check=lambda tile,next_tile:tile.x>next_tile.x+Rectangular_width+Move_vel
        ceil=True
    elif direction=="right":
        sort_func=lambda x:x.col 
        reverse=True
        delta=(Move_vel,0)
        Boundary_check=lambda tile:tile.col==Cols-1
        get_next_tile=lambda tile:tiles.get(f"{tile.row}{tile.col+1}")
        merge_check=lambda tile,next_tile: tile.x<next_tile.x-Move_vel 
        move_check=lambda tile,next_tile:tile.x+Rectangular_width+Move_vel<next_tile.x
        ceil=False
    elif direction=="up":
        sort_func=lambda x:x.row
        reverse=False
        delta=(0,-Move_vel)
        Boundary_check=lambda tile:tile.row==0
        get_next_tile=lambda tile:tiles.get(f"{tile.row-1}{tile.col}")
        merge_check=lambda tile,next_tile: tile.y>next_tile.y+Move_vel 
        move_check=lambda tile,next_tile:tile.y>Rectangular_height+Move_vel+next_tile.y
        ceil=True
    elif direction=="down":
        sort_func=lambda x:x.row
        reverse=True
        delta=(0,Move_vel)
        Boundary_check=lambda tile:tile.row==Rows-1
        get_next_tile=lambda tile:tiles.get(f"{tile.row+1}{tile.col}")
        merge_check=lambda tile,next_tile: tile.y<next_tile.y-Move_vel 
        move_check=lambda tile,next_tile:tile.y+Rectangular_height+Move_vel<next_tile.y
        ceil=False
    
    while updated:
        clock.tick(FPS)
        updated=False
        sorted_tiles=sorted(tiles.values(),key=sort_func,reverse=reverse)
        for i,tile in enumerate(sorted_tiles):
            if Boundary_check(tile):
                continue
            next_tile=get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value==next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile,next_tile):
                    tile.move(delta)
                else:
                    next_tile.value*=2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile,next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated=True
        updated_tiles(window,tiles,sorted_tiles)
    end_move(tiles)

def end_move(tiles):
    if len(tiles)==16:
        return "lost Try Again"
    row,col=get_random_pos(tiles)
    tiles[f"{row}{col}"]=Tile(random.choice([2,4]),row,col)
    return "continue"
    
def updated_tiles(window,tiles,sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"]=tile
    draw(window,tiles)

def main(Window):
    clock=pygame.time.Clock()
    run=True
    tiles=generate_tiles()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    move_tiles(Window,tiles,clock,"left")
                if event.key==pygame.K_RIGHT:
                    move_tiles(Window,tiles,clock,"right")
                if event.key==pygame.K_UP:
                    move_tiles(Window,tiles,clock,"up")
                if event.key==pygame.K_DOWN:
                    move_tiles(Window,tiles,clock,"down")

                
        draw(Window,tiles)

    pygame.quit()



if __name__=="__main__":
    main(Window)