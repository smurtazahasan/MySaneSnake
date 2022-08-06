import random
import math
from typing import List, Dict

def get_info() -> dict:
    return {"apiversion": "1", "author": "murtztheman", "color": "#000000", "head": "dead", "tail": "block-bum"}

def choose_move(data: dict) -> str:
  # Global Variables
  board = data['board']
  snakes = board['snakes']
  head = snakes[0]['body'][0]
  foods = board['food']
  possible_moves = {
      'up': {'x': head['x'], 'y': head['y'] + 1},
      'right': {'x': head['x'] + 1, 'y': head['y']},
      'down': {'x': head['x'], 'y': head['y'] - 1},
      'left': {'x': head['x'] - 1, 'y': head['y']}}

  del snakes[0]['body'][-1] # Impossible for snake to collide with tail
  
  # Main Function Calls
  possible_moves = avoid_obstacles(snakes, board, possible_moves)
  possible_moves = _look_ahead(snakes, possible_moves, snakes[0]['length'], snakes[0]['id'])
  possible_moves = _flood_fill(snakes, possible_moves, snakes[0]['length'])

  # Move Decision
  if len(possible_moves) > 0:
    dir = move_for_food(foods, snakes, possible_moves)
    if dir != None and (snakes[0]['length'] < max(highest_length(snakes), 16) or snakes[0]['health'] < 50): return dir
    else: return random.choice(list(possible_moves.keys()))
  print('Game Lost - No Possible Moves')

# Health Up-Keep
def move_for_food(foods, snakes, possible_moves):
  food_target = [float('inf'), (0, 0)]
  pointA = (snakes[0]['body'][0]['x'], snakes[0]['body'][0]['y'])
  for food in foods:
      pointB = (food['x'], food['y'])
      if math.dist(pointA, pointB) < food_target[0]: food_target = [math.dist(pointA, pointB), pointB]

  for dir, future_move in possible_moves.items():
      new_head = (future_move['x'], future_move['y'])

      if math.dist(new_head, food_target[1]) < food_target[0]:
          return dir
  return None
# Obstacle Avoidance
def avoid_obstacles(snakes, board, possible_moves):
  non_moves, curr_snakes = [], []
  for snake in snakes: curr_snakes += snake['body']
  
  for dir, future_move in possible_moves.items():
    x_range = future_move['x'] < 0 or future_move['x'] == board['width']
    y_range = future_move['y'] < 0 or future_move['y'] == board['height']
    if x_range or y_range: non_moves.append(dir)
    elif future_move in curr_snakes: non_moves.append(dir)
  
  for i in non_moves: del possible_moves[i]
  return possible_moves


# Max Length of Other Snakes
def highest_length(snakes):
  del snakes[0]
  currMax = -float('inf')
  for snake in snakes:
    currMax = max(currMax, snake['length'])
  return currMax


def look_ahead(snakes, possible_moves):
    non_moves, mylength, fail = [], snakes[0]['length'], False
    del snakes[0]

    for snake in snakes:
      enemy_snake_possible_moves = {
        {'x': snake['head']['x'], 'y': snake['head']['y'] + 1},
        {'x': snake['head']['x'] + 1, 'y': snake['head']['y']},
        {'x': snake['head']['x'], 'y': snake['head']['y'] - 1},
        {'x': snake['head']['x'] - 1, 'y': snake['head']['y']}}
      if snake['length'] >= mylength:
        for dir, moves in possible_moves.items():
          if moves in enemy_snake_possible_moves: non_moves.append(dir)
    for item in possible_moves:
      if item not in non_moves: fail = True
    if fail:
      for items in non_moves:
        if items in possible_moves: del possible_moves[items]
    return possible_moves


def _flood_fill(snakes, possible_moves, length):
  
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
    if len(bad_moves) >= 3:
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
    if len(bad_moves) >= 2:
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