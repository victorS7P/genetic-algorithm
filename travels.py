rows = open('./data/travels.txt', 'r').read().split('\n')

travels = dict()
cities = list()
TRAVEL_DESTINY = "travel_destiny"
TRAVEL_TIME_COST = "travel_time_cost"
TRAVEL_MONEY_COST = "travel_money_cost"

for row in rows:
  [origin, destiny, time, money] = row.split(',')

  col_data = dict({ TRAVEL_DESTINY: destiny, TRAVEL_TIME_COST: time, TRAVEL_MONEY_COST: money })

  if origin in travels:
    travels[origin].append(col_data)
  else:
    travels[origin] = list([col_data])
    cities.append(origin)
