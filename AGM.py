from BeliefBase import BeliefBase
from BeliefContraction import contract_belief_base
from LogicalEntailment import resolution
from Proposition import Proposition
import sympy as sp
import copy

def success(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    newBase = oldBase.expand(phi.premise)
    newBasePremise = [(belief.premise).upper() for belief, _ in newBase.beliefs]
    return (phi.premise).upper() in newBasePremise

def inclusion(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    newBase = contract_belief_base(oldBase.beliefs, phi)
    oldSet = set([(belief.premise).upper() for belief, _ in oldBase.beliefs])
    newSet = set([(belief.premise).upper() for belief, _ in newBase])
    return newSet.issubset(oldSet)

def vacuity(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    combined_beliefs = Proposition(" and ".join([belief.premise for belief, _ in oldBase.beliefs]))
    if not resolution(combined_beliefs, phi):
        newBase = contract_belief_base(oldBase.beliefs, phi)
        oldBasePremise = [(belief.premise).upper() for belief, _ in oldBase.beliefs]
        newBasePremise = [(belief.premise).upper() for belief, _ in newBase]
        return newBasePremise == oldBasePremise
    return True

def consistency(Belief, phi):
    oldBase = copy.deepcopy(Belief)
    newBase = contract_belief_base(oldBase.beliefs, phi)
    return consistent(newBase) if len(newBase) > 0 else True

def extensionality(Belief, phi1, phi2):
    oldBase = copy.deepcopy(Belief)
    if equivalent(phi1, phi2):
        newBasePhi1 = contract_belief_base(oldBase.beliefs, phi1)
        newBasePhi2 = contract_belief_base(oldBase.beliefs, phi2)
        phi1Contract = [belief.premise for belief, _ in newBasePhi1]
        phi2Contract = [belief.premise for belief, _ in newBasePhi2]
        return phi1Contract == phi2Contract
    return True

def consistent(Belief):
    # If Belief is a list, process it directly; otherwise, assume it has a 'beliefs' attribute
    if isinstance(Belief, list):
        base = Belief
    else:
        base = Belief.beliefs

    combined_beliefs = Proposition("(" + ") and (".join([belief.premise for belief, _ in base]) + ")")
    combined_beliefs.symbolic_form()
    local_sym = {str(sym): sym for sym in combined_beliefs.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    expr = sp.parsing.sympy_parser.parse_expr(combined_beliefs.expression, local_dict=local_sym, evaluate=False)
    return bool(sp.satisfiable(expr))

def equivalent(phi1, phi2):
    phi = Proposition(f"({phi1.premise}) iff ({phi2.premise})")
    phi.symbolic_form()
    local_sym = {str(sym): sym for sym in phi.symbolic}
    local_sym.update({'Eq': sp.Equivalent})
    expr = sp.parsing.sympy_parser.parse_expr(phi.expression, local_dict = local_sym, evaluate = False)
    return not sp.satisfiable(sp.Not(expr))
