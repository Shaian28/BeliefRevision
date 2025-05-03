from BeliefBase import BeliefBase
from BeliefContraction import contract_belief_base
from LogicalEntailment import resolution
from Proposition import Proposition
import sympy as sp

def success(Belief, phi):
    newBase = Belief.expand(phi)
    return phi in newBase.beliefs

def inclusion(Belief, phi):
    newBase = contract_belief_base(Belief, phi)
    return set(newBase).issubset(set(Belief.beliefs))

def vacuity(Belief, phi):
    if not resolution(Belief, phi):
        newBase = contract_belief_base(Belief, phi)
        return newBase == Belief.beliefs
    return True

def consistency(Belief, phi):
    newBase = contract_belief_base(Belief, phi)
    return consistent(newBase)

def extensionality(Belief, phi1, phi2):
    if equivalent(phi1, phi2):
        return contract_belief_base(Belief, phi1) == contract_belief_base(Belief, phi2)
    return True

def consistent(Belief):
    Belief.symbolic_form()
    local_sym = {str(sym): sym for sym in Belief.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    expr = sp.parsing.sympy_parser.parse_expr(Belief.expression, local_dict = local_sym, evaluate = False)
    return bool(sp.satisfiable(expr))

def equivalent(phi1, phi2):
    phi = Proposition(f"({phi1.premise}) iff ({phi2.premise})")
    phi.symbolic_form()
    local_sym = {str(sym): sym for sym in phi.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    expr = sp.parsing.sympy_parser.parse_expr(phi.expression, local_dict = local_sym, evaluate = False)
    return not sp.satisfiable(sp.Not(expr))
