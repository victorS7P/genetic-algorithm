import random
import math
import copy

from travels import (
  travels,
  cities,
  ESCONDIDOS,
  TRAVEL_DESTINY,
  TRAVEL_MONEY_COST,
  TRAVEL_TIME_COST,
  get_city_random_destiny,
  exists_travel,
  get_travel_details
)

from items import (
  cities_items,
  ITEM_NAME,
  ITEM_WEIGHT,
  ITEM_VALUE,
  ITEM_TIME_COST
)

CITY = "city"
HAS_STEALLED = "has_stealled"
WEIGHT_LIMIT = 20
TIME_LIMIT = 72

class GeneticAlgorithm():
  def __init__(self, population_size, max_same_best, new_gene_tax, remove_gene_tax,):
    self.population_size = population_size
    self.max_same_best = max_same_best

    self.new_gene_tax = new_gene_tax
    self.remove_gene_tax = remove_gene_tax

  def create_gene(self, city = ESCONDIDOS, has_stealled = False):
    return dict({
      CITY: city,
      HAS_STEALLED: has_stealled and city != ESCONDIDOS
    })

  def create_specimen(self):
    return list([
      self.create_gene(),
      self.create_gene()
    ])

  def remove_random_genes(self, specimen):
    if (self.remove_gene_tax > random.randint(0, 100) and len(specimen) > 2):
      gene_index = random.randint(1, len(specimen) - 2)

      while True:
        del specimen[gene_index]

        if (len(specimen) == 2):
          break

        last_city = specimen[gene_index - 1][CITY]
        city = specimen[gene_index][CITY]

        if (exists_travel(last_city, city)):
          break

        if (gene_index == len(specimen) - 1):
          gene_index -= 1

  def add_random_new_genes(self, specimen):
    if (self.new_gene_tax > random.randint(0, 100)):
      gene_index = random.randint(1, len(specimen) - 2) if len(specimen) > 2 else 1

      while True:
        last_city = specimen[gene_index - 1][CITY]
        city = get_city_random_destiny(last_city)

        specimen.insert(gene_index, self.create_gene(city, bool(random.randint(0, 1))))

        if (exists_travel(city, specimen[gene_index + 1][CITY])):
          break

        gene_index += 1

  def create_random_specimen(self):
    specimen = self.create_specimen()

    if (random.randint(0,1) == 1):
      self.add_random_new_genes(specimen)

    if (random.randint(0,1) == 1):
      self.remove_random_genes(specimen)

    return specimen

  def mutate_specimen(self, specimen):
    new_specimen = copy.deepcopy(specimen)

    if (random.randint(0,1) == 1):
      self.remove_random_genes(new_specimen)
      self.add_random_new_genes(new_specimen)
    else:
      self.add_random_new_genes(new_specimen)
      self.remove_random_genes(new_specimen)

    return new_specimen

  def create_population(self):
    population = []

    for _ in range(self.population_size):
      specimen = self.create_random_specimen()
      population.append(specimen)

    return population

  def get_specimen_data(self, specimen):
    data = dict({
      ITEM_NAME: list(),
      ITEM_TIME_COST: 0,
      ITEM_VALUE: 0,
      ITEM_WEIGHT: 0,

      TRAVEL_DESTINY: list(),
      TRAVEL_MONEY_COST: 0,
      TRAVEL_TIME_COST: 0,
    })

    for i in range(len(specimen) - 1):
      city = specimen[i][CITY]
      next_city = specimen[i + 1][CITY]

      if specimen[i][HAS_STEALLED]:
        item = cities_items[city]

        data[ITEM_NAME].append(item[ITEM_NAME])
        data[ITEM_TIME_COST] += item[ITEM_TIME_COST]
        data[ITEM_VALUE] += item[ITEM_VALUE]
        data[ITEM_WEIGHT] += item[ITEM_WEIGHT]

      if (exists_travel(city, next_city)):
        travel = get_travel_details(city, next_city)

        data[TRAVEL_DESTINY].append(city)
        data[TRAVEL_MONEY_COST] += travel[TRAVEL_MONEY_COST]
        data[TRAVEL_TIME_COST] += travel[TRAVEL_TIME_COST]

      if (i == len(specimen) - 1):
        data[TRAVEL_DESTINY].append(travel[TRAVEL_DESTINY])

    return data

  def get_specimen_ponctuation(self, specimen):
    data = self.get_specimen_data(specimen)

    steal_gain = data[ITEM_VALUE]
    steal_cost = data[ITEM_WEIGHT] + data[ITEM_TIME_COST]
    travel_cost = steal_cost + data[TRAVEL_MONEY_COST] + data[TRAVEL_TIME_COST]

    return (steal_gain + (steal_gain/(steal_cost if steal_cost > 0 else 1)) - travel_cost)

  def keep_not_twice_stealled(self, specimen):
    stealled = list()

    for gene in specimen:
      if gene[HAS_STEALLED] == 1:
        if gene[CITY] in stealled:
          return False
        stealled.append(gene[CITY])
    
    return True

  def keep_not_impossible_travel(self, specimen):
    for i in range(len(specimen) - 1):
      city = specimen[i][CITY]
      destinies = travels[city]
      next_city = specimen[i + 1][CITY]

      if next_city == city or next_city not in list(map(lambda travel: travel[TRAVEL_DESTINY], destinies)):
        return False

    return True

  def keep_not_over_weight_limit(self, specimen):
    if self.get_specimen_data(specimen)[ITEM_WEIGHT] > WEIGHT_LIMIT:
      return False

    return True

  def keep_not_over_time_limit(self, specimen):
    data = self.get_specimen_data(specimen)
    total_time = data[ITEM_TIME_COST] + data[TRAVEL_TIME_COST]

    if total_time > TIME_LIMIT:
      return False

    return True

  def selection_elimination(self, population):
    return list(filter(lambda specimen:
      self.keep_not_twice_stealled(specimen) and
      self.keep_not_impossible_travel(specimen) and
      self.keep_not_over_weight_limit(specimen) and
      self.keep_not_over_time_limit(specimen)
    , population))

  def selection_sort(self, population):
    return list(sorted(
      population,
      key = lambda specimen: self.get_specimen_ponctuation(specimen),
      reverse=True
    ))

  def selection(self, population):
    local_population = self.selection_elimination(copy.deepcopy(population))
    return self.selection_sort(local_population)[:self.population_size]

  def crossover(self, population):
    crossover_population = []
    auxiliar_population = copy.deepcopy(population)

    while (len(auxiliar_population) > 0):
      specimen_1 = auxiliar_population.pop()

      for specimen_2 in auxiliar_population:
        len_1 = len(specimen_1) - 1
        len_2 = len(specimen_2) - 1
        min_len = len_1 if len_1 < len_2 else len_2

        gene = random.randint(1, min_len) if min_len > 2 else 1

        new_specimen_1 = specimen_1[:gene] + specimen_2[gene:]
        new_specimen_2 = specimen_2[:gene] + specimen_1[gene:]

        crossover_population.append(new_specimen_1)
        crossover_population.append(new_specimen_2)

    return crossover_population

  def get_population_avg(self, population):
    total = 0
    for specimen in population:
      total += self.get_specimen_ponctuation(specimen)

    return total/len(population)

  def run(self):
    random.seed()

    gen = 0
    same_best = 0
    old_best_pontuctuation = 0

    population = self.create_population()

    crossover_points = list([0.3, 0.5])
    do_crossover = [math.ceil(x * self.max_same_best) for x in crossover_points]

    while(True):
      gen += 1

      mutated_population = [self.mutate_specimen(specimen) for specimen in population]
      population = self.selection(population + mutated_population)

      if (same_best in do_crossover):
        population = self.selection(self.crossover(population) + population)

      best = population[0]
      best_pontuctuation = self.get_specimen_ponctuation(best)

      if old_best_pontuctuation == best_pontuctuation:
        same_best += 1
      else:
        same_best = 0

      if same_best == self.max_same_best:
        return best

      old_best_pontuctuation = best_pontuctuation

      print(f"\n====== GERAÇÃO {gen} =======")
      print("MELHOR PONTUAÇÃO   = {:5}".format(math.ceil(self.get_specimen_ponctuation(best))))
      print("PONTUAÇÃO MÉDIA    = {:5}".format(math.ceil(self.get_population_avg(population))))
      print("")

