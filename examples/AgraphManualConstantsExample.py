# Ignoring some linting rules in tests
# pylint: disable=redefined-outer-name
# pylint: disable=missing-docstring
import numpy as np

from bingo.symbolic_regression.agraph.crossover import AGraphCrossover
from bingo.symbolic_regression.agraph.mutation import AGraphMutation
from bingo.symbolic_regression.agraph.generator import AGraphGenerator
from bingo.symbolic_regression.agraph.component_generator \
    import ComponentGenerator
from bingo.symbolic_regression.explicit_regression import ExplicitRegression, \
                                                        ExplicitTrainingData

from bingo.evolutionary_algorithms.age_fitness import AgeFitnessEA
from bingo.evaluation.evaluation import  Evaluation
from bingo.evolutionary_optimizers.island import Island

POP_SIZE = 128
STACK_SIZE = 10
MUTATION_PROBABILITY = 0.4
CROSSOVER_PROBABILITY = 0.4
NUM_POINTS = 100
START = -10
STOP = 10
ERROR_TOLERANCE = 0.05


def init_x_vals(start, stop, num_points):
    return np.linspace(start, stop, num_points).reshape([-1, 1])


def equation_eval(x):
    return x**2 + 3.5*x**3


def init_island():
    np.random.seed(10)
    x = init_x_vals(START, STOP, NUM_POINTS)
    y = equation_eval(x)
    training_data = ExplicitTrainingData(x, y)

    component_generator = ComponentGenerator(
            x.shape[1],
            automatic_constant_optimization=False,
            numerical_constant_range=10)
    component_generator.add_operator("+")
    component_generator.add_operator("-")
    component_generator.add_operator("*")

    crossover = AGraphCrossover(component_generator)
    mutation = AGraphMutation(component_generator)

    agraph_generator = AGraphGenerator(STACK_SIZE, component_generator)

    fitness = ExplicitRegression(training_data=training_data)
    evaluator = Evaluation(fitness)

    ea = AgeFitnessEA(evaluator, agraph_generator, crossover,
                      mutation, MUTATION_PROBABILITY,
                      CROSSOVER_PROBABILITY, POP_SIZE)

    island = Island(ea, agraph_generator, POP_SIZE)
    return island


def main():
    test_island = init_island()
    report_island_status(test_island)
    test_island.evolve_until_convergence(max_generations=1000,
                                         fitness_threshold=ERROR_TOLERANCE)
    report_island_status(test_island)


def report_island_status(test_island):
    print("-----  Generation %d  -----" % test_island.generational_age)
    print("Best individual:     ", test_island.get_best_individual())
    print("Best fitness:        ", test_island.get_best_fitness())
    print("Fitness evaluations: ", test_island.get_fitness_evaluation_count())


if __name__ == '__main__':
    main()
