import random
import math
import copy

from travels import (
  travels,
  cities,
  ESCONDIDOS,
  TRAVEL_DESTINY,
  TRAVEL_MONEY_COST,
  TRAVEL_TIME_COST
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

def get_city_random_destiny(city):
  destinies = travels[city]
  return travels[city][random.randint(0, len(destinies) - 1)][TRAVEL_DESTINY]

class GeneticAlgorithm():
  def __init__(self, population_size, best_selected_slice, max_generations, mutation_tax, crossover_tax):
    self.population_size = population_size
    self.best_selected_slice = best_selected_slice
    self.max_generations = max_generations

    self.mutation_tax = mutation_tax
    self.crossover_tax = crossover_tax

    self.population = []

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

  def add_random_new_gene(self, specimen):
    gene_index = random.randint(1, len(specimen) - 1)

    last_city = specimen[gene_index - 1][CITY]
    city = get_city_random_destiny(last_city)

    specimen.insert(gene_index, self.create_gene(city, bool(random.randint(0, 1))))

  def create_random_specimen(self):
    specimen = self.create_specimen()
    while (random.randint(0, 100) > 50):
      self.add_random_new_gene(specimen)

    return specimen

  def mutate_specimen(self, specimen):
    new_specimen = copy.deepcopy(specimen)

    while (random.randint(0, 100) > 50):
      self.add_random_new_gene(new_specimen)

    genes_to_mutate = math.ceil((len(new_specimen) - 2) * self.mutation_tax)

    for _ in range(genes_to_mutate):
      gene = random.randint(1, len(new_specimen) - 2)

      last_city = new_specimen[gene - 1][CITY]
      city = get_city_random_destiny(last_city)

      new_specimen[gene] = self.create_gene(city, bool(random.randint(0, 1)))

    return new_specimen

  def create_population(self):
    for _ in range(self.population_size):
      specimen = self.create_random_specimen()
      self.population.append(specimen)

  def get_specimen_total_time(self, specimen):
    time = 0

    for i in range(len(specimen)):
      city = specimen[i][CITY]
      destinies = travels[city]

      if specimen[i][HAS_STEALLED]:
        time += cities_items[specimen[i][CITY]][ITEM_TIME_COST]

      if i < len(specimen) - 1:
        next_city = specimen[i + 1][CITY]
        destiny = list(filter(lambda travel: travel[TRAVEL_DESTINY] == next_city, destinies))

        if (len(destiny)):
          time += destiny[0][TRAVEL_TIME_COST]

    return time

  def get_specimen_total_weight(self, specimen):
    weight = 0

    for gene in specimen:
      if gene[HAS_STEALLED]:
        weight += cities_items[gene[CITY]][ITEM_WEIGHT]

    return weight

  def get_specimen_total_money(self, specimen):
    money = 0

    for i in range(len(specimen)):
      city = specimen[i][CITY]
      destinies = travels[city]

      if specimen[i][HAS_STEALLED]:
        money += cities_items[specimen[i][CITY]][ITEM_VALUE]

      if i < len(specimen) - 1:
        next_city = specimen[i + 1][CITY]
        destiny = list(filter(lambda travel: travel[TRAVEL_DESTINY] == next_city, destinies))

        if (len(destiny)):
          money -= destiny[0][TRAVEL_MONEY_COST]

    return money

  def get_specimen_ponctuation(self, specimen):
    return self.get_specimen_total_money(specimen) - self.get_specimen_total_time(specimen)

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
    if self.get_specimen_total_weight(specimen) > WEIGHT_LIMIT:
      return False

    return True

  def keep_not_over_time_limit(self, specimen):
    if self.get_specimen_total_time(specimen) > TIME_LIMIT:
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

    if (self.crossover_tax > random.randint(0,100)):
      auxiliar_population = copy.deepcopy(population)

      while (len(auxiliar_population) > 0):
        specimen_1 = auxiliar_population.pop()

        for specimen_2 in auxiliar_population:
          gene = random.randint(0, len(specimen_1) - 1)

          new_specimen_1 = specimen_1[:gene] + specimen_2[gene:]
          new_specimen_2 = specimen_2[:gene] + specimen_1[gene:]

          crossover_population.append(new_specimen_1)
          crossover_population.append(new_specimen_2)

    return crossover_population

  def run(self):
    random.seed()

    for i in range(10):
      self.create_population()
      mutated_population = [self.mutate_specimen(specimen) for specimen in self.population]
      crossover_population = self.crossover(self.population)

      selecteds = self.selection(self.population + mutated_population + crossover_population)
      best = selecteds[0]

      print(f"BEST PONCTUATION = {self.get_specimen_ponctuation(best)}")
      print(f"MONEY = {self.get_specimen_total_money(best)}")
      print(f"TIME  = {self.get_specimen_total_time(best)}")

      # if geracoes % 100 == 0:
      #   print("geracoes: " + str(geracoes) + " Fitness: " + str(fitness(populacao[0])))
      # geracoes += 1

    print(best)
