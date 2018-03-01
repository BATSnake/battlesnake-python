import bottle
import os
import random
from random import randint

ENEMY = 1
WALL = 2
SAFE = 5
#---------------------------------------------------------------------------
game_id = ''
board_width = 0
board_height = 0
board = [[0 for x in range(board_width)] for y in range(board_height)] 
#---------------------------------------------------------------------------

@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    global game_id
    global board_width
    global board_height
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head2.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'cc',
        "head_type": "tongue",
        "tail_type": "pixel"
    }
                            


@bottle.post('/move')
def move():
    data = bottle.request.json

    #crate a 2d array for board: all values are 0
    global board
    board = [[0 for x in range(board_width)] for y in range(board_height)] 

    #get food location
    my_food_list = []
    food_list = data.get('food')['data']
    for each_food in food_list:
        food_x = each_food['x']
        food_y = each_food['y']
        my_food_list.append([food_x, food_y]) #my_food_list e.g. [[12,1], [23,12], [0,9]]

    #get the location of myself
    my_body_list = []
    body_list = data.get('you')['body']['data']
    for each_segment in body_list:
        segment_x = each_segment['x']
        segment_y = each_segment['y']
        my_body_list.append([segment_x,segment_y]) #my_body_list e.g. [[1,1], [2,1], [2,2]] #first coor is the head!!


    #get the location of other snakes   (TODO!!!)
    enemy_body_list = []
    enemy_list = data.get('snakes')['data']
    for each_enemy in enemy_list:
        each_enemy_snake = []
        for each_enemy_segement in each_enemy['body']['data']:
            enemy_body_x = each_enemy_segement['x']
            enemy_body_y = each_enemy_segement['y']
            each_enemy_snake.append([enemy_body_x, enemy_body_y])
        enemy_body_list.append(each_enemy_snake) #enemy_body_list e.g [ [[2,3],[2,4]], [[5,6],[5,7],[5,8]] ]  two snakes
    
    #set the value of walls to be 1 (including my body and enemy snakes' bodies)
    board = set_walls(my_body_list, enemy_body_list)

    #get the position of the snake head
    head = my_body_list[0] #e.g.[1,1]

    #get the optional directions for the head
    directions = direction_options(head)
    
    #TODO!!!
    direction = find_best_direction(directions, head, my_food_list)

    
    return {
        'move': direction,
        'taunt': 'I\'m drunk'
    } 

#the coor for walls are [1]
def set_walls(my_body_list, enemy_body_list):
    global board
    for each_segment in my_body_list:  #[1,1]
        segx = each_segment[0]
        segy = each_segment[1]
        board[segx][segy] = 1
    return board

#get the direction options of my snake head 
def direction_options(head):
    global board
    global board_width
    global board_height
    curx = head[0]
    cury = head[1]
    directions = []
    #check if we can move up
    if cury >= 1:
        if board[curx][cury-1] == 0:
             directions.append('up')
    #check if we can move right
    if curx <= board_width - 2:
        if board[curx+1][cury] == 0:
             directions.append('right')
    #check if we can move left
    if curx >= 1:
        if board[curx-1][cury] == 0:
             directions.append('left')
    #check if we can move down
    if cury <= board_height - 2:
        if board[curx][cury+1] == 0:
             directions.append('down')
    return directions

#TODO
def find_best_direction(directions, head, my_food_list):
    direction = ''
    food_pos = my_food_list[0] #e.g.[3,7]
    headx = head[0]
    heady = head[1]
    foodx = food_pos[0]
    foody = food_pos[1]
    updistance, rightdistance, downdistance, leftdistance = float("inf"),float("inf"),float("inf"),float("inf") 

    for legal_direction in directions:
        if legal_direction == 'up':
            updistance = (headx-foodx)**2 + (heady-1-foody)**2
        elif legal_direction == 'right':
            rightdistance = (headx+1-foodx)**2 + (heady-foody)**2
        elif legal_direction == 'left':
            leftdistance = (headx-1-foodx)**2 + (heady-foody)**2
        elif legal_direction == 'down':
            downdistance = (headx-foodx)**2 + (heady+1-foody)**2

    print(updistance, rightdistance, downdistance, leftdistance)
    direction= 'up'
    min_distance = updistance
    if rightdistance<min_distance:
        direction = 'right'
        min_distance = rightdistance
    if downdistance<min_distance:
        direction='down'
        min_distance = downdistance
    if leftdistance<min_distance:
        direction='left'
        min_distance = leftdistance

    return direction


@bottle.post('/end')
def end():
    data = bottle.request.json
    return {'taunt': 'uh'}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
