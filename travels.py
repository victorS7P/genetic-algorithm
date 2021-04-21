rows = open('./data/travels.txt', 'r').read().split('\n')

travels = dict()
cities = list()
TRAVEL_DESTINY = "travel_destiny"
TRAVEL_TIME_COST = "travel_time_cost"
TRAVEL_MONEY_COST = "travel_money_cost"
ESCONDIDOS = "Escondidos"

def create_travel_data(destiny, time, money):
  return dict({
    TRAVEL_DESTINY: destiny,
    TRAVEL_TIME_COST: int(time),
    TRAVEL_MONEY_COST: int(money)
  })

for row in rows:
  [origin, destiny, time, money] = row.split(',')

  col_data = create_travel_data(destiny, time, money)
  inverse_col_data = create_travel_data(origin, time, money)

  if origin in travels:
    travels[origin].append(col_data)
  else:
    travels[origin] = list([col_data])
    cities.append(origin)

  if destiny in travels:
    destinies = travels[destiny]

    if origin not in list(map(lambda travel: travel[TRAVEL_DESTINY], destinies)):
      travels[destiny].append(inverse_col_data)
  else:
    travels[destiny] = list([inverse_col_data])
    cities.append(destiny)
