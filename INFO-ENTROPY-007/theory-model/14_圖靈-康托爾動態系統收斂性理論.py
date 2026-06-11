# turing_cantor_computable.py

from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Set


Symbol = str
State = str
Direction = int  # -1 (left), +1 (right)


@dataclass
class Transition:
    next_state: State
    write_symbol: Symbol
    move: Direction


class ComputableTuringMachine:
    """
    A computable symbolic dynamical system:
    - tape: infinite (implemented as sparse dictionary)
    - head: integer position
    - state: finite control
    """

    def __init__(
        self,
        transitions: Dict[Tuple[State, Symbol], Transition],
        start_state: State,
        blank_symbol: Symbol = "_",
        accept_states: Set[State] = None,
        reject_states: Set[State] = None,
    ):
        self.transitions = transitions
        self.state = start_state
        self.blank = blank_symbol
        self.accept_states = accept_states or set()
        self.reject_states = reject_states or set()

        self.tape: Dict[int, Symbol] = {}
        self.head = 0
        self.step_count = 0

    # -----------------------------
    # Observation map φ
    # -----------------------------
    def observe(self):
        return (self.state, self.tape.get(self.head, self.blank), self.head)

    # -----------------------------
    # Single step dynamics F
    # -----------------------------
    def step(self) -> bool:
        key = (self.state, self.tape.get(self.head, self.blank))

        if key not in self.transitions:
            return False  # undefined transition => halt

        t = self.transitions[key]

        # write
        self.tape[self.head] = t.write_symbol

        # move head
        self.head += t.move

        # update state
        self.state = t.next_state

        self.step_count += 1

        return True

    # -----------------------------
    # Run system
    # -----------------------------
    def run(self, max_steps: int = 10_000):
        history = []

        for _ in range(max_steps):
            history.append(self.observe())

            if self.state in self.accept_states:
                return {
                    "result": "ACCEPT",
                    "history": history,
                    "steps": self.step_count,
                }

            if self.state in self.reject_states:
                return {
                    "result": "REJECT",
                    "history": history,
                    "steps": self.step_count,
                }

            if not self.step():
                return {
                    "result": "HALT (undefined transition)",
                    "history": history,
                    "steps": self.step_count,
                }

        return {
            "result": "TIMEOUT",
            "history": history,
            "steps": self.step_count,
        }


# -----------------------------
# Example machine: unary increment
# -----------------------------
def example_machine():
    """
    A simple computable dynamical system:
    input: 111
    output: 1111
    """

    transitions = {
        ("q0", "1"): Transition("q0", "1", +1),
        ("q0", "_"): Transition("q1", "1", 0),  # write final 1 and stop moving
    }

    return ComputableTuringMachine(
        transitions=transitions,
        start_state="q0",
        blank_symbol="_",
        accept_states={"q1"},
    )


# -----------------------------
# Utility: load input
# -----------------------------
def load_tape(machine: ComputableTuringMachine, s: str):
    for i, c in enumerate(s):
        machine.tape[i] = c


# -----------------------------
# Demo run
# -----------------------------
if __name__ == "__main__":
    tm = example_machine()
    load_tape(tm, "111")

    result = tm.run(max_steps=100)

    print("Result:", result["result"])
    print("Steps:", result["steps"])
    print("Final state:", tm.state)
    print("Final tape:", tm.tape)
