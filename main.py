# main.py
from BeliefBase import BeliefBase
from Proposition import Proposition
from BeliefContraction import contract_belief_base
from AGM import *

def test_agm_postulates(belief_base):
    belief = input("Enter proposition to test out: ")
    target_phi = Proposition(belief)

    belief = input("Enter an equivalent proposition to test out (for extensionality): ")
    equivalent_phi = Proposition(belief)

    print("\n--- Testing AGM Postulates ---")

    # Success Postulate: After revision, the new belief is included
    print("Success Postulate:", success(belief_base, target_phi))

    # Inclusion Postulate: All previous beliefs not contradicting new belief should be retained
    print("Inclusion Postulate:", inclusion(belief_base, target_phi))

    # Vacuity Postulate: If the new belief is already in the belief base, no change needed
    print("Vacuity Postulate:", vacuity(belief_base, target_phi))

    # Consistency Postulate: Belief base should remain consistent
    print("Consistency Postulate:", consistency(belief_base, target_phi))

    # Extensionality Postulate: If two beliefs are equivalent, they should be interchangeable
    print("Extensionality Postulate:", extensionality(belief_base, target_phi, equivalent_phi))

def print_belief_base(belief_base):
    print("Current Belief Base:")
    for i, b in enumerate(belief_base.formulas):
        print(f"  [{i+1}] {b}")

def main():
    print("=== Belief Revision Engine ===")
    belief_base = BeliefBase()

    while True:
        print("\nOptions:")
        print("1. Expand belief base with a proposition")
        print("2. Contract belief base with a proposition")
        print("3. View current belief base")
        print("4. Test with AGM postulates")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            belief = input("Enter proposition to expand with: ")
            priority = input("Enter the priority of the belief as a number between 1 and 10 (5 for don't know): ")
            while priority not in map(str, range(1, 11)):
                print("Invalid priority. Please enter a number between 1 and 10.")
                priority = input("Enter the priority of the belief as a number between 1 and 10 (5 for don't know): ")
            belief_base.expand(belief, int(priority))
            print("Belief base expanded.")
        elif choice == "2":
            oldBelief = (belief_base.beliefs).copy()
            belief = input("Enter proposition to contract with: ")
            prop = Proposition(belief)
            contract_belief = contract_belief_base(belief_base.beliefs, prop)
            belief_base.beliefs = [(Proposition(belief.premise), priority) for belief, priority in contract_belief]
            if len(oldBelief) == len(belief_base.beliefs):
                print("No beliefs were contracted.")
            else:
                print("Belief base contracted.")
        elif choice == "3":
            print(belief_base)
        elif choice == "4":
            test_agm_postulates(belief_base)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
