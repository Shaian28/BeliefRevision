from BeliefBase import BeliefBase
from BeliefContraction import contract_belief_base
from LogicalEntailment import resolution
from Proposition import Proposition
import sympy as sp

def success(Belief, phi):
    newBase = Belief.expand(phi.premise)
    return phi in newBase.beliefs

def inclusion(Belief, phi):
    belief_base_with_priorities = [(belief, idx + 1) for idx, belief in enumerate(Belief.beliefs)]
    newBase = contract_belief_base(belief_base_with_priorities, phi)
    return set(newBase).issubset(set(Belief.beliefs))

def vacuity(Belief, phi):
    belief_base_with_priorities = [(belief, idx + 1) for idx, belief in enumerate(Belief.beliefs)]
    combined_beliefs = Proposition(" and ".join([belief.premise for belief in Belief.beliefs]))
    if not resolution(combined_beliefs, phi):
        newBase = contract_belief_base(belief_base_with_priorities, phi)
        return newBase == Belief.beliefs
    return True

def consistency(Belief, phi):
    belief_base_with_priorities = [(belief, idx + 1) for idx, belief in enumerate(Belief.beliefs)]
    newBase = contract_belief_base(belief_base_with_priorities, phi)
    return consistent(newBase)

def extensionality(Belief, phi1, phi2):
    belief_base_with_priorities = [(belief, idx + 1) for idx, belief in enumerate(Belief.beliefs)]
    if equivalent(phi1, phi2):
        return contract_belief_base(belief_base_with_priorities, phi1) == contract_belief_base(belief_base_with_priorities, phi2)
    return True

def consistent(Belief):
    combined_beliefs = Proposition(" and ".join([belief.premise for belief, _ in Belief]))
    combined_beliefs.symbolic_form()
    local_sym = {str(sym): sym for sym in combined_beliefs.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    expr = sp.parsing.sympy_parser.parse_expr(combined_beliefs.expression, local_dict = local_sym, evaluate = False)
    return bool(sp.satisfiable(expr))

def equivalent(phi1, phi2):
    phi = Proposition(f"({phi1.premise}) iff ({phi2.premise})")
    phi.symbolic_form()
    local_sym = {str(sym): sym for sym in phi.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    expr = sp.parsing.sympy_parser.parse_expr(phi.expression, local_dict = local_sym, evaluate = False)
    return not sp.satisfiable(sp.Not(expr))
