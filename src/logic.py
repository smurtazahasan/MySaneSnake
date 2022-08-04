import random
import math
from typing import List, Dict

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""

def get_info() -> dict:
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "murtztheman",  # TODO: Your Battlesnake Username
        "color": "#005daa",  # TODO: Personalize
        "head": "evil",  # TODO: Personalize
        "tail": "coffee",  # TODO: Personalize
    }


def choose_move(data: dict) -> str:
  my_snake = data["you"]      # A dictionary describing your snake's position on the board
  my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
  my_body = my_snake["body"]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
  my_board = data["board"]
  board_height, board_width = my_board['height'], my_board['width']
  my_food = my_board['food']
  hazards = my_board['hazards']

  otherSnakes = my_board['snakes']

  possible_moves = {
    'up': {
      'x': my_head['x'],
      'y': my_head['y'] + 1
    },
    'right': {
      'x': my_head['x'] + 1,
      'y': my_head['y']
    },
    'down': {
      'x': my_head['x'],
      'y': my_head['y'] - 1
    },
    'left': {
      'x': my_head['x'] - 1,
      'y': my_head['y']
    }
  }
  possible_moves_2 = {
    'up': {
      'x': my_head['x'],
      'y': my_head['y'] + 1
    },
    'right': {
      'x': my_head['x'] + 1,
      'y': my_head['y']
    },
    'down': {
      'x': my_head['x'],
      'y': my_head['y'] - 1
    },
    'left': {
      'x': my_head['x'] - 1,
      'y': my_head['y']
    }
  }

  possible_moves = _avoid_my_body(my_body, possible_moves)
  possible_moves = _avoid_walls(board_height, board_width, possible_moves)
  possible_moves = _avoid_others(otherSnakes, possible_moves, my_snake['id'])
  possible_moves = _look_ahead(otherSnakes, possible_moves, my_snake['length'], my_snake['id'])
  possible_moves = _flood_fill(otherSnakes, possible_moves, my_head, my_snake['length'], my_body[-1])
  
  # add to avoid others the head part to avoid head to head collisions 

  # TODO: Step 4 - Find food.
  # Use information in `data` to seek out and find food.
  # food = data['board']['food']
  

  # Choose a random direction from the remaining possible_moves to move in, and then return that move

  dist_func = _distance(my_head, my_food)
  min_dist_food = _move_to_food(my_head, dist_func, possible_moves)
  lengths = _length_of_snakes(otherSnakes)
  
  if len(possible_moves) > 0:
    if min_dist_food != None and (my_snake['length'] <= lengths[-1] or my_snake['health'] < 50):
      move = min_dist_food
    else:
      move = random.choice(list(possible_moves.keys()))
  else:
    move = 'up'
    print('No Options Left')

  print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

  return move


def _avoid_my_body(my_body, possible_moves):
    non_moves = []
    del my_body[-1]
    for dir, future_move in possible_moves.items():
      # possible_moves.keys() returns [direction "up", {'x': #, 'y': #}]
      if future_move in my_body:
        non_moves.append(dir)

    for items in non_moves:
      del possible_moves[items]

    return possible_moves

def _avoid_walls(board_height, board_width, possible_moves):
    non_moves = []
    for dir, future_move in possible_moves.items():
      x_range = future_move['x'] < 0 or future_move['x'] == board_width
      y_range = future_move['y'] < 0 or future_move['y'] == board_height

      if x_range or y_range:
        non_moves.append(dir)
  
    for items in non_moves:
      del possible_moves[items]
  
    return possible_moves
def _avoid_others(otherSnakes, possible_moves, id):
  non_moves = []
  for snake in otherSnakes:
    if snake["id"]!=id:
      for dir, future_move in possible_moves.items():
        if future_move in snake['body']:
          non_moves.append(dir)
  non_moves = set(non_moves)
  for items in non_moves:
    del possible_moves[items]
  
  return possible_moves
def _avoid_hazards(hazards, possible_moves):
  non_moves = []
  for dir, future_move in possible_moves.items():
    if future_move in hazards:
      non_moves.append(dir)

  for items in non_moves:
    del possible_moves[items]
  
  return possible_moves
def _distance(my_head, my_food):
  # nearest-neighbor search
  min_distance = [float('inf'), 0, 0] # [distance, x, y]
  for food in my_food:
    head = (my_head['x'], my_head['y'])
    point = (food['x'], food['y'])
    
    distance = math.dist(head, point)
    if distance < min_distance[0]:
      min_distance[0] = distance
      min_distance[1] = food['x']
      min_distance[2] = food['y']
  return min_distance
def _move_to_food(my_head, min_dist_food, possible_moves):
  for dir, future_move in possible_moves.items():
    new_head = (future_move['x'], future_move['y'])
    food = (min_dist_food[1], min_dist_food[2])

    if math.dist(new_head, food) < min_dist_food[0]:
      return dir
  return None
def _length_of_snakes(otherSnakes):
  lengths = []
  for snakes in otherSnakes:
    lengths.append(snakes['length'])

  lengths.sort()
  return lengths

def _look_ahead(otherSnakes, possible_moves, my_length, my_id):
  non_moves = []
  for snake in otherSnakes:
    if snake["length"] >= my_length and snake["id"] != my_id:
      snake_head = snake['head']
      snake_moves = [
        {
          'x': snake_head['x'],
          'y': snake_head['y'] + 1
        },
        {
          'x': snake_head['x'] + 1,
          'y': snake_head['y']
        },
        {
          'x': snake_head['x'],
          'y': snake_head['y'] - 1
        },
        {
          'x': snake_head['x'] - 1,
          'y': snake_head['y']
        }
      ]
      for dir, moves in possible_moves.items():
        if moves in snake_moves:
          non_moves.append(dir)
  fail = 0
  for item in possible_moves:
    if item not in non_moves:
      fail = 1
  if fail == 1:
    for items in non_moves:
      if items in possible_moves:
        del possible_moves[items]
  return possible_moves


def _flood_fill(snakes, possible_moves, head, length, tail):

  values = {
    'up': {
      'value': 120
    },
    'right': {
      'value': 120
    },
    'down': {
      'value': 120
    },
    'left': {
      'value': 120
    }
  }
  
  for moves, items in possible_moves.items():
    w, h = 11, 11
    matrix = [[0 for x in range(w)] for y in range(h)] 
    for snake in snakes:
      for part in snake["body"]:
        matrix[part['y']][part['x']]=1
        
    matrix=_flooding(matrix, items)
    count = 0
    for i in range(10):
      print("")
      j = 10
      while j >= 0:
        if matrix[j][i]==0:
          print("0", end = '')
        elif matrix[j][i]==1:
          print("1", end = '')
        else:
          print("2", end = '')
          count = count+1
        j = j-1
    values[moves]['value'] = count
    print("count:", count)
    print(values[moves]['value'])

  if len(possible_moves) == 3:
    bad_moves = []
    worst_val = 100
    for dir in values:
      value = values[dir]['value']
      if value < worst_val:
        worst_dir = dir
        worst_val = value
      if value < length:
        bad_moves.append(dir)
    if len(bad_moves) == 3:
      best_val = 0
      best_dir="up"
      for dir in values:
        value = values[dir]['value']
        if value >= best_val and value < 120:
          best_val = value
          best_dir = dir
      for items in bad_moves:
        if items != best_dir:
          print(items)
          print(best_dir)
          del possible_moves[items]
    else:
      for items in bad_moves:
        del possible_moves[items]
  if len(possible_moves) == 2:
    bad_moves = []
    for dir in values:
      value = values[dir]['value']
      if value < length:
        bad_moves.append(dir)
    if len(bad_moves) == 2:
      best_val = 0
      best_dir="up"
      for dir in values:
        value = values[dir]['value']
        if value > best_val and value < 120:
          best_val = value
          best_dir = dir
      for items in bad_moves:
        if items != best_dir:
          print(items)
          print(best_dir)
          del possible_moves[items]
    else:
      for items in bad_moves:
        del possible_moves[items]
  return possible_moves
      
      
    
    
      
      
        
      
        


def _flooding(matrix, current_point):
  if matrix[current_point['y']][current_point['x']]==1:
    return matrix
  if matrix[current_point['y']][current_point['x']]==2:
    return matrix
  if matrix[current_point['y']][current_point['x']]==0:
    matrix[current_point['y']][current_point['x']]=2
    if current_point['x']>0:
      matrix = _flooding(matrix, {'x':current_point['x']-1, 'y': current_point['y'] })
    if current_point['y']<10:
      matrix =_flooding(matrix, {'x':current_point['x'], 'y': current_point['y']+1})
    if current_point['y']>0:
      matrix =_flooding(matrix, {'x':current_point['x'], 'y': current_point['y']-1})
    if current_point['x']<10:
      matrix = _flooding(matrix, {'x':current_point['x']+1, 'y': current_point['y'] })
  return matrix
  
