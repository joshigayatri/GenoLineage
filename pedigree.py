"""
Module 2: Pedigree Tree + Inheritance Probability (Recursion / Dynamic Programming)
=====================================================================================
This module builds a family tree (pedigree) as a graph of Person nodes, and
calculates the probability that a person carries a disease-linked mutation,
based on their parents' mutation status -- following simplified Mendelian
inheritance logic.

Data structure used: Tree/Graph (each Person points to their two parents)
Algorithm used: Recursion (walks up the tree through parent references)
"""


class Person:
    """
    One node in the family tree.

    mutation_status:
        True  -> known to carry the disease-linked mutation
        False -> known to NOT carry it
        None  -> unknown; probability must be calculated from parents
    """

    def __init__(self, name, parent1=None, parent2=None, mutation_status=None):
        self.name = name
        self.parent1 = parent1   # another Person object, or None if founder
        self.parent2 = parent2
        self.mutation_status = mutation_status

    def __repr__(self):
        return f"Person({self.name})"


def build_sample_family():
    """
    Builds a small 4-generation sample family tree for testing.

    Generation 1 (founders): grandparents -- mutation status is KNOWN
    Generation 2: parents -- status unknown, must be calculated
    Generation 3: children -- status unknown, must be calculated
    Generation 4: grandchildren -- status unknown, must be calculated

    Returns a dictionary of {name: Person} for easy lookup.
    """
    people = {}

    # ---- Generation 1: Founders (known mutation status) ----
    people["Grandpa_A"] = Person("Grandpa_A", mutation_status=True)   # carries mutation
    people["Grandma_A"] = Person("Grandma_A", mutation_status=False)
    people["Grandpa_B"] = Person("Grandpa_B", mutation_status=False)
    people["Grandma_B"] = Person("Grandma_B", mutation_status=False)

    # ---- Generation 2: Parents (unknown, calculated from founders) ----
    people["Parent_1"] = Person("Parent_1", people["Grandpa_A"], people["Grandma_A"])
    people["Parent_2"] = Person("Parent_2", people["Grandpa_B"], people["Grandma_B"])

    # ---- Generation 3: Children of Parent_1 x Parent_2 ----
    people["Child_1"] = Person("Child_1", people["Parent_1"], people["Parent_2"])
    people["Child_2"] = Person("Child_2", people["Parent_1"], people["Parent_2"])

    # ---- Generation 4: Grandchildren ----
    # Child_1 marries an outside person (Spouse) with known clean status
    people["Spouse"] = Person("Spouse", mutation_status=False)
    people["Grandchild_1"] = Person("Grandchild_1", people["Child_1"], people["Spouse"])

    return people


def naive_inheritance_probability(person):
    """
    NAIVE recursive calculation (NO memoization).

    Mendelian simplification used here: a child's probability of carrying
    the mutation is the average of both parents' probabilities (each
    parent independently contributes one of two alleles). This mirrors
    the standard recursive structure used in inheritance-path models.

    WARNING: this recomputes every ancestor's probability from scratch
    every single time it is called -- if the same ancestor appears in
    multiple lineages (which happens in real pedigrees, e.g. cousin
    marriages), the same sub-calculation is repeated many times.
    """
    if person.mutation_status is not None:
        return 1.0 if person.mutation_status else 0.0

    # Recursive case: average of both parents' probabilities
    p1 = naive_inheritance_probability(person.parent1)
    p2 = naive_inheritance_probability(person.parent2)
    return 0.5 * p1 + 0.5 * p2


def memoized_inheritance_probability(person, memo=None):
    """
    MEMOIZED version -- identical logic, but stores each person's computed
    probability in a dictionary (memo) so it is only ever calculated ONCE,
    no matter how many descendants ask for it.
    """
    if memo is None:
        memo = {}

    if person.name in memo:
        return memo[person.name]

    if person.mutation_status is not None:
        result = 1.0 if person.mutation_status else 0.0
    else:
        p1 = memoized_inheritance_probability(person.parent1, memo)
        p2 = memoized_inheritance_probability(person.parent2, memo)
        result = 0.5 * p1 + 0.5 * p2

    memo[person.name] = result
    return result


def print_family_risk_report(people, prob_function):
    """Prints every family member's calculated mutation-carrying probability."""
    for name, person in people.items():
        if person.mutation_status is not None:
            status = "KNOWN carrier" if person.mutation_status else "KNOWN clean"
            print(f"  {name:15s} -> {status}")
        else:
            prob = prob_function(person)
            print(f"  {name:15s} -> Calculated risk: {prob:.2%}")