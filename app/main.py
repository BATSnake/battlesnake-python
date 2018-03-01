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
    board_width = data.get('width') 
    board_height = data.get('height') 
    print board_width
    print board_height
    path = 0
    
    board = [[0 for x in xrange(board_height+1)] for y in xrange(board_width+1)]

    # TODO: Do things with data

    #setup Safe value
    for row in range(board_height):
	for col in range(board_width):
	    board[row][col] = SAFE
	
    # set up Wall value	
    for row in range(board_height):
	    board[row][0] = WALL    # Left wall
	    board[row][board_width-1] = WALL    # Right wall
    for col in range(board_width):
	    board[0][col] = WALL    # Top wall
	    board[board_height-1][col] = WALL   # Bottom wall

    ranlen = len(data['you']['body']['data'])
    #set the self-sanke body as the enemy
    for num in range(ranlen):
	    posx = data['you']['body']['data'][num]['x']      
	    posy = data['you']['body']['data'][num]['y']
##	    print posx
##	    print posy
	    board[posx][posy] = ENEMY
	    
    #get the position of the snake head
    sx = data['you']['body']['data'][0]['x']      
    sy = data['you']['body']['data'][0]['y']

    if board[sx+1][sy] == SAFE or board[sx+1][sy] == WALL:
        print board[sx+1][sy]
	path = 3
    elif board[sx-1][sy] == SAFE or board[sx-1][sy] == WALL:
	path = 2
    elif board[sx][sy-1] == SAFE or board[sx][sy-1] == WALL:
	path = 1
    elif board[sx][sy+1] == SAFE or board[sx][sy+1] == WALL:
	path = 0

    directions = ['up', 'down', 'left', 'right']
    print directions[path]
    return {
        'move': directions[path],
        'taunt': 'I\'m drunk'
    } 
	    
    
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
