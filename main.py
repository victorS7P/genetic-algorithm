import time

from genetic_algorithm import (
  GeneticAlgorithm,
  CITY,
  HAS_STEALLED
)

from travels import (
  TRAVEL_DESTINY,
  TRAVEL_MONEY_COST,
  TRAVEL_TIME_COST
)

from items import (
  ITEM_NAME,
  ITEM_WEIGHT,
  ITEM_VALUE,
  ITEM_TIME_COST
)

if __name__ == "__main__":
  tic = time.time()

  POPULATION_SIZE   = 250
  MAX_SAME_BEST     = 15
  NEW_GENE_TAX      = 100
  REMOVE_GENE_TAX   = 100

  genetic_algorithm = GeneticAlgorithm(
    POPULATION_SIZE,
    MAX_SAME_BEST,
    NEW_GENE_TAX,
    REMOVE_GENE_TAX
  )

  best = genetic_algorithm.run()
  data = genetic_algorithm.get_specimen_data(best)

  toc = time.time()

  print('======= MELHOR CAMINHO =========')
  for i in range(len(best)):
    print("[{:^10}] {:42}".format('ROUBAR' if best[i][HAS_STEALLED] else 'NÃO ROUBAR', best[i][CITY], ))
  print('================================')
  print('')

  print('=============== ITENS ROUBADOS ===============')
  for i in range(len(data[ITEM_NAME])):
    print("{:2}. {:19}".format(i + 1, data[ITEM_NAME][i]))
  print('==============================================')
  print('')

  print('======================================')
  print('PESO FINAL DA MOCHILA   =     {:6}kg'.format(data[ITEM_WEIGHT]))
  print('--------------------------------------')
  print('TEMPO GASTO VIAJANDO    =      {:6}h'.format(data[TRAVEL_TIME_COST]))
  print('TEMPO GASTO ROUBANDO    =      {:6}h'.format(data[ITEM_TIME_COST]))
  print('TEMPO TOTAL GASTO       =      {:6}h'.format(data[TRAVEL_TIME_COST] + data[ITEM_TIME_COST]))
  print('--------------------------------------')
  print('TOTAL DE DINHEIRO GANHO = R$ {:6,}.00'.format(data[ITEM_VALUE]))
  print('TOTAL GASTO COM VIAGENS = R$ {:6,}.00'.format(data[TRAVEL_MONEY_COST]))
  print('--------------------------------------')
  print('GANHO FINAL             = R$ {:6,}.00'.format(data[ITEM_VALUE] - data[TRAVEL_MONEY_COST]))
  print('======================================')
  print("RESULTADO ALCANÇADO EM  =      {:6.2f}s".format((toc - tic)))
  print('======================================')
