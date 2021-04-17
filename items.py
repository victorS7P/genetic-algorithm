rows = open('./data/items.txt', 'r').read().split('\n')

cities_items = dict()
ITEM_NAME = "item_name"
ITEM_TIME_COST = "item_time_cost"
ITEM_VALUE = "item_value"
ITEM_WEIGHT = "item_weight"

for row in rows:
  [name, weight, time, money, city] = row.split(',')

  cities_items[city] = dict({
    ITEM_NAME: name,
    ITEM_TIME_COST: time,
    ITEM_VALUE: money,
    ITEM_WEIGHT: weight
  })
