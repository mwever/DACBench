from enum import Enum


class ProblemDomain:
    """
    This class implements a generic python wrapper for HyFlex problem domains.
    """

    HeuristicType = Enum('CROSSOVER', 'LOCAL_SEARCH', 'MUTATION', 'OTHER', 'RUIN_RECREATE')

    def __init__(self, domain: str, seed: int):
        """
        Creates a new problem domain and creates a new random number generator using the seed provided. If
        the seed takes the value -1, the seed is generated taking the current System time. The random number generator
        is used for all stochastic operations, so the problem will be initialised in the same way if the seed is the
        same. Sets the solution memory size to 2.

        :param domain: the unqualified class name of the HyFlex domain to be wrapped, e.g., SAT, BinPacking, etc.
        :param seed: a random seed
        """
        raise NotImplementedError

    def getHeuristicCallRecord(self) -> list[int]:
        """
        Shows how many times each low level heuristic has been called.

        :return: A list which contains an integer value for each low level heuristic, representing the number of times
            that heuristic has been called by the HyperHeuristic object.
        """
        raise NotImplementedError

    def getHeuristicCallTimeRecord(self) -> list[int]:
        """
        Shows the total time that each low level heuristic has been operating on the problem.

        :return: A list which contains an integer value representing the total number of milliseconds used by each low
            level heuristic.
        """
        raise NotImplementedError

    def setDepthOfSearch(self, depthOfSearch: float) -> None:
        """
        Sets the parameter specifying the extent to which a local search heuristic will modify the solution.
        This parameter is related to the number of improving steps to be completed by the local search heuristics.

        :param depthOfSearch: must be in the range 0 to 1. The initial value of 0.1 represents the default operation of
            the low level heuristic.
        :return: None
        """
        raise NotImplementedError

    def setIntensityOfMutation(self, intensityOfMutation: float) -> None:
        """
        Sets the parameter specifying the extent to which a mutation or ruin-recreate low level heuristic will mutate
        the solution. For a mutation heuristic, this could mean the range of new values that a variable can take,
        in relation to its current value. It could mean how many variables are changed by one call to the heuristic.
        For a ruin-recreate heuristic, it could mean the percentage of the solution that is destroyed and rebuilt.
        For example, a value of 0.5 may indicate that half the solution will be rebuilt by a RUIN_RECREATE heuristic.
        The meaning of this variable is intentionally vaguely stated, as it depends on the heuristic in question,
        and the problem domain in question.

        :param intensityOfMutation: must be in the range 0 to 1. The initial value of 0.1 represents the default
            operation of the low level heuristic.
        :return: None
        """
        raise NotImplementedError

    def getDepthOfSearch(self) -> float:
        """
        Gets the current intensity of mutation parameter.

        :return: the current value of the intensity of mutation parameter.
        """
        raise NotImplementedError

    def getIntensityOfMutation(self) -> float:
        """
        Gets the current intensity of mutation parameter.

        :return: the current value of the intensity of mutation parameter.
        """
        raise NotImplementedError

    def getHeuristicsOfType(self, heuristicType: HeuristicType) -> list[int]:
        """
        Gets an array of heuristicIDs of the type specified by heuristicType.

        :param heuristicType: the heuristic type.
        :return: An list containing the indices of the heuristics of the type specified. If there are no heuristics of
            this type it returns None.
        """
        raise NotImplementedError

    def getHeuristicsThatUseIntensityOfMutation(self) -> list[int]:
        """
        Gets an array of heuristicIDs that use the intensityOfMutation parameter

        :param heuristicType: the heuristic type.
        :return: An array containing the indexes of the heuristics that use the intensityOfMutation parameter, or None
            if there are no heuristics of this type.
        """
        raise NotImplementedError

    def getHeuristicsThatUseDepthOfSearch(self) -> list[int]:
        """
        Gets an array of heuristicIDs that use the depthOfSearch parameter

        :param heuristicType: the heuristic type.
        :return: An array containing the indexes of the heuristics that use the depthOfSearch parameter, or None if
            there are no heuristics of this type.
        """
        raise NotImplementedError

    def loadInstance(self, instanceID: int) -> None:
        """
        Loads the instance specified by instanceID.

        :param instanceID: Specifies the instance to load. The ID's start at zero.
        :return: None
        """
        raise NotImplementedError

    def setMemorySize(self, size: int) -> None:
        """
        Sets the size of the array where the solutions are stored. The default size is 2.

        :param size: The new size of the solution array.
        :return: None
        """
        raise NotImplementedError

    def initialiseSolution(self, index: int) -> None:
        """
        Create an initial solution at a specified position in the memory array. The method of initialising the solution
        depends on the specific problem domain, but it is a random process, which will produce a different solution
        each time. The initialisation process may randomise all of the elements of the problem, or it may use a
        constructive heuristic with a randomised input.

        :param index: The index of the memory array at which the solution should be initialised.
        :return: None
        """
        raise NotImplementedError

    def getNumberOfHeuristics(self) -> None:
        """
        Gets the number of heuristics available in this problem domain

        :return: The number of heuristics available in this problem domain
        """

    def applyHeuristic(self, heuristicID: int, solutionSourceIndex: int, solutionDestinationIndex: int) -> float:
        """
        Applies the heuristic specified by heuristicID to the solution at position solutionSourceIndex and places the
        resulting solution at position solutionDestinationIndex in the solution array. If the heuristic is a
        CROSSOVER type then the solution at solutionSourceIndex is just copied to solutionDestinationIndex.

        :param heuristicID: The ID of the heuristic to apply (starts at zero)
        :param solutionSourceIndex: The index of the solution in the memory array to which to apply the heuristic
        :param solutionDestinationIndex: The index in the memory array at which to store the resulting solution
        :return: the objective function value of the solution created by applying the heuristic
        """
        raise NotImplementedError

    def applyHeuristic2(self, heuristicID: int, solutionSourceIndex1: int, solutionSourceIndex2: int,
                        solutionDestinationIndex: int = -1) -> float:
        """
        Apply the heuristic specified by heuristicID to the solutions at position solutionSourceIndex1 and position
        solutionSourceIndex2 and put the resulting solution at position solutionDestinationIndex. The heuristic can
        be of any type (including CROSSOVER).

        :param heuristicID: The ID of the heuristic to apply (starts at zero)
        :param solutionSourceIndex1: The index of the first solution in the memory array to which to apply the heuristic
        :param solutionSourceIndex2: The index of the second solution in the memory array to which to apply the heuristic
        :param solutionDestinationIndex: The index in the memory array at which to store the resulting solution
        :return: the objective function value of the solution created by applying the heuristic
        """
        raise NotImplementedError

    def copySolution(self, solutionSourceIndex: int, solutionDestinationIndex: int) -> None:
        """
        Copies a solution from one position in the solution array to another

        :param solutionSourceIndex: The position of the solution to copy
        :param solutionDestinationIndex: The position in the array to copy the solution to.
        :return: None
        """
        raise NotImplementedError

    def toString(self) -> str:
        """
        Gets the name of the problem domain. For example, "Bin Packing"

        :return: the name of the ProblemDomain
        """
        raise NotImplementedError

    def getNumberOfInstances(self) -> int:
        """
        Gets the number of instances available in this problem domain

        :return: the number of instances available
        """
        raise NotImplementedError

    def bestSolutionToString(self) -> str:
        """
        Returns the objective function value of the best solution found so far by the HyperHeuristic.

        :return: The objective function value of the best solution.
        """
        raise NotImplementedError

    def getBestSolutionValue(self) -> float:
        """
        Returns the objective function value of the best solution found so far by the HyperHeuristic.

        :return: The objective function value of the best solution.
        """

    def solutionToString(self, solutionIndex: int) -> str:
        """
        Gets a String representation of a given solution in memory

        :param solutionIndex: The index of the solution of which a String representation is required
        :return: A String representation of the solution at solutionIndex in the solution memory
        """
        raise NotImplementedError

    def getFunctionValue(self, solutionIndex: int) -> float:
        """
        Gets the objective function value of the solution at index solutionIndex

        :param solutionIndex: The index of the solution from which the objective function is required
        :return: A double value of the solution's objective function value.
        """
        raise NotImplementedError

    def compareSolutions(self, solutionIndex1: int, solutionIndex2: int) -> bool:
        """
        Compares the two solutions on their structure (i.e. in the solution space, not in the objective/fitness
        function space).

        :param solutionIndex1: The index of the first solution in the comparison
        :param solutionIndex2: The index of the second solution in the comparison
        :return: true if the solutions are identical, false otherwise.
        """
        raise NotImplementedError
