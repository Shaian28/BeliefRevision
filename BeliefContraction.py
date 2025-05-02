from itertools import combinations
from LogicalEntailment import resolution
from Proposition import Proposition

# belief_base is a list of (Proposition, priority) tuples
def contract_belief_base(belief_base, target_phi):
    # Step 1: Sort by ascending priority (low priority removed first)
    sorted_base = sorted(belief_base, key=lambda x: x[1])  # [(Proposition, priority)]

    # Step 2: If KB doesn't entail φ, return unchanged
    formulas = [prop for prop, _ in sorted_base]
    if not resolution(combine_propositions(formulas), target_phi):
        return belief_base

    # Step 3: Try removing combinations of formulas to break entailment
    for i in range(1, len(sorted_base) + 1):
        for subset in combinations(sorted_base, len(sorted_base) - i):
            test_formulas = [prop for prop, _ in subset]
            if not resolution(combine_propositions(test_formulas), target_phi):
                # We found a minimal remainder set
                return list(subset)

    # If no remainder set found (unlikely), return empty
    return []

def combine_propositions(propositions):
    if not propositions:
        return Proposition("A and not A")  # A contradiction
    combined_str = " and ".join([" ".join(p.order) for p in propositions])
    return Proposition(combined_str)
