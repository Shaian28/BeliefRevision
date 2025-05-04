from BeliefBase import BeliefBase
from BeliefContraction import contract_belief_base
from LogicalEntailment import resolution
from Proposition import Proposition
import sympy as sp
import copy

def success(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    newBase = oldBase.expand(phi.premise)
    return phi in newBase.beliefs

def inclusion(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    newBase = contract_belief_base(oldBase.beliefs, phi)
    return set(newBase).issubset(set(oldBase.beliefs))

def vacuity(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    combined_beliefs = Proposition(" and ".join([belief.premise for belief, _ in oldBase.beliefs]))
    if not resolution(combined_beliefs, phi):
        newBase = contract_belief_base(oldBase.beliefs, phi)
        return newBase == oldBase.beliefs
    return True

def consistency(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    newBase = contract_belief_base(oldBase.beliefs, phi)
    return consistent(newBase)

def extensionality(Belief, phi1, phi2):
    oldBase = copy.deepcopy(Belief)
    if equivalent(phi1, phi2):
        return contract_belief_base(oldBase.beliefs, phi1) == contract_belief_base(oldBase.beliefs, phi2)
    return True

def consistent(Belief):
    oldBase = copy.deepcopy(Belief)
    combined_beliefs = Proposition(" and ".join([belief.premise for belief, _ in oldBase]))
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
