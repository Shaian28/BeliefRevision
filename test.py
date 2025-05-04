from BeliefBase import BeliefBase
from Proposition import Proposition
from BeliefContraction import contract_belief_base
# Import AGM postulates
from AGM import success, inclusion, vacuity, consistency, extensionality

def main():
    # Create a new belief base
    belief_base = BeliefBase()

    # Add beliefs to the belief base
    belief_base.expand("A and B")
    belief_base.expand("not C or A")
    belief_base.expand("D iff (A or B)")

    # Print the current belief base
    print("Current Belief Base:")
    print(belief_base)

    # Assign priorities to beliefs and prepare the belief base for contraction
    belief_base_with_priorities = [(belief, idx + 1) for idx, belief in enumerate(belief_base.beliefs)]

    # Contract the belief base using the contract_belief_base function
    target_phi = Proposition("A and B")
    contracted_belief_base = contract_belief_base(belief_base_with_priorities, target_phi)

    # Update the belief base with the contracted beliefs
    belief_base.beliefs = [belief for belief, _ in contracted_belief_base]

    # Print the belief base after contraction using the function
    print("\nBelief Base after contraction using contract_belief_base:")
    print(belief_base)

    # Define a target proposition for testing AGM postulates
    target_phi = Proposition("A and B")
    equivalent_phi = Proposition("B and A")

    # Test AGM postulates
    print("\nTesting AGM Postulates:")

    # Success Postulate
    print("Success Postulate:", success(belief_base, target_phi))

    # Inclusion Postulate
    print("Inclusion Postulate:", inclusion(belief_base, target_phi))

    # Vacuity Postulate
    print("Vacuity Postulate:", vacuity(belief_base, target_phi))

    # Consistency Postulate
    print("Consistency Postulate:", consistency(belief_base, target_phi))

    # Extensionality Postulate
    print("Extensionality Postulate:", extensionality(belief_base, target_phi, equivalent_phi))

if __name__ == "__main__":
    main()