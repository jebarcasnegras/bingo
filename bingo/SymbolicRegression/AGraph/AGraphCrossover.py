"""Definition of crossover between two acyclic graph individuals

This module contains the implementation of single point crossover between
acyclic graph individuals.
"""
import numpy as np

from ...Base.Crossover import Crossover


class AGraphCrossover(Crossover):
    """Crossover between acyclic graph individuals

    Parameters
    ----------
    component_generator : ComponentGenerator
        Component generator used for generating numerical constants.
    """

    def __init__(self, component_generator):
        self._component_generator = component_generator
        self._manual_constants = \
            not component_generator.automatic_constant_optimization

    def __call__(self, parent_1, parent_2):
        """Single point crossover.

        Parameters
        ----------
        parent_1 : Agraph
                   The first parent individual
        parent_2 : Agraph
                   The second parent individual

        Returns
        -------
        tuple(Agraph, Agraph) :
            The two children from the crossover.
        """

        child_1 = parent_1.copy()
        child_2 = parent_2.copy()

        self._modify_children_for_tracking_constants(child_1, child_2,
                                                     parent_1, parent_2)
        self._crossover_command_arrays(child_1, child_2, parent_1)
        if self._manual_constants:
            self._insert_manual_constants(child_1)
            self._insert_manual_constants(child_2)

        child_age = max(parent_1.genetic_age, parent_2.genetic_age)
        child_1.genetic_age = child_age
        child_2.genetic_age = child_age

        return child_1, child_2

    @staticmethod
    def _modify_children_for_tracking_constants(child_1, child_2,
                                                parent_1, parent_2):
        num_p_1_consts = len(parent_1.constants)
        child_1.constants = parent_1.constants + parent_2.constants
        child_2.constants = parent_1.constants + parent_2.constants
        const_filt = np.logical_and(child_2.command_array[:, 0] == 1,
                                    child_2.command_array[:, 1] != -1)
        child_2.command_array[const_filt, 1] += num_p_1_consts

    @staticmethod
    def _crossover_command_arrays(child_1, child_2, parent_1):
        ag_size = parent_1.command_array.shape[0]
        cross_point = np.random.randint(1, ag_size - 1)
        child_1.command_array[cross_point:] = \
            child_2.command_array[cross_point:]
        child_2.command_array[cross_point:] = \
            parent_1.command_array[cross_point:]

    def _insert_manual_constants(self, individual):
        for i in individual.find_inserted_constants():
            individual.constants[i] = \
                self._component_generator.random_numerical_constant()
