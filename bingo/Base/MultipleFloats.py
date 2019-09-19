"""Multiple Floats for genetic information

This file contains the several classes that are used for chromosomes
that contains a list of floats for their genetic information.
"""
from .ContinuousLocalOptimization import ChromosomeInterface
from ..Util.ArgumentValidation import argument_validation
from .MultipleValues import MultipleValueChromosome, \
                            MultipleValueChromosomeGenerator


class MultipleFloatChromosome(MultipleValueChromosome, ChromosomeInterface):
    """Multiple float-value individual

    Parameters
    ----------
    values : list of floats
        The genetic information stored in an individual chromosome.
    needs_opt_list : list of ints
        (optional) The indices of the `individual_list` in a
        `Chromosome` object that are subject local optimization.
        This list may be empty
    """
    def __init__(self, values, needs_opt_list=None):
        super().__init__(values)
        if needs_opt_list is None:
            needs_opt_list = []
        self._needs_opt_list = needs_opt_list

    @property
    def needs_continuous_opt(self):
        """Does the individual need local optimization"""
        if not self._needs_opt_list:
            return False
        return True

    @needs_continuous_opt.setter
    def needs_continuous_opt(self, value):
        pass

    def get_number_local_optimization_params(self):
        """Get number of parameters in local optimization

        Returns
        -------
        int
            number of paramneters to be optimized
        """
        return len(self._needs_opt_list)

    def set_local_optimization_params(self, params):
        """Set local optimization parameters

        Parameters
        ----------
        params : list-like of numeric
                 Values to set the parameters
        """
        for param, index in zip(params, self._needs_opt_list):
            self.values[index] = param


class MultipleFloatChromosomeGenerator(MultipleValueChromosomeGenerator):
    """Generation of a population of Multi-Value Chromosomes

    Parameters
    ----------
    random_value_function : user defined function
        A function that returns a list of randomly generated float values.
        This list is then passed to the ``MultipleValueChromosome``
        constructor.
    values_per_chromosome : int
        The number of values that each chromosome will hold
    needs_opt_list : list of ints
        The indices of the `individual_list` in a  `Chromosome` object
        that are subject local optimization. This list may be empty
    """
    @argument_validation(values_per_chromosome={">=": 0})
    def __init__(self, random_value_function, values_per_chromosome,
                 needs_opt_list=None):

        self._check_function_produces_float(random_value_function)
        super().__init__(random_value_function, values_per_chromosome)
        self._check_list_contains_ints_in_valid_range(needs_opt_list)
        if needs_opt_list is None:
            needs_opt_list = []
        self._needs_opt_list = self._remove_duplicates(needs_opt_list)

    def __call__(self):
        """Generation of a population of size `population_size`
        of Multi-Value Chromosomes with lists that contain
        `values_per_list` values.

        Returns
        -------
        list of Chromosomes:
            The chromosomes which their values are generated by
            `random_value_function` with the optimization list
            `needs_opt_list`.
        """
        random_list = self._generate_list(self._values_per_chromosome)
        return MultipleFloatChromosome(random_list, self._needs_opt_list)

    @staticmethod
    def _check_function_produces_float(random_value_function):
        val = random_value_function()
        if not isinstance(val, float):
            raise ValueError("Random value function must generate floats.")

    def _check_list_contains_ints_in_valid_range(self, list_of_indices):
        if not list_of_indices:
            return
        if not all(isinstance(x, int) for x in list_of_indices):
            raise ValueError("The list of optimization indices must be \
                              unsigned integers.")
        if min(list_of_indices) < 0 or \
               max(list_of_indices) > self._values_per_chromosome:
            raise ValueError("The list of optimization indices must be within \
                              the length of the list of values.")

    @staticmethod
    def _remove_duplicates(list_of_ints):
        set_of_ints = set(list_of_ints)
        return sorted([val for val in set_of_ints])
