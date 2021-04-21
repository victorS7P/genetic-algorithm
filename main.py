from genetic_algorithm import GeneticAlgorithm

if __name__ == "__main__":
  genetic_algorithm = GeneticAlgorithm(100, 20, 10000, 50, 10)
  genetic_algorithm.run()

  print('OK!')
