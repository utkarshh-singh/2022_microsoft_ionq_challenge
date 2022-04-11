# %%
"""
# For Microsoft-IonQ Backends:
"""

# %%
from azure.quantum import Workspace
workspace = Workspace (
    subscription_id = "b1d7f7f8-743f-458e-b3a0-3e09734d716d",
    resource_group = "aq-hackathons",
    name = "aq-hackathon-01",
    location = "eastus"
)


# %%
from azure.quantum.qiskit import AzureQuantumProvider
provider = AzureQuantumProvider (
    resource_id = "/subscriptions/b1d7f7f8-743f-458e-b3a0-3e09734d716d/resourceGroups/aq-hackathons/providers/Microsoft.Quantum/Workspaces/aq-hackathon-01",
    location = "eastus"
)

# %%
print([backend.name() for backend in provider.backends()])

# %%
backend = provider.get_backend("ionq.qpu")
sim = Aer.get_backend('aer_simulator')

# %%


# %%
"""
# For IBMQ Backends:
"""

# %%


# %%
#backend = provider.get_backend("ibmq_manila")
backend = BasicAer.get_backend("qasm_simulator")
sim = Aer.get_backend('aer_simulator')

# %%
"""
## Import Qiskit libraries:
"""

# %%
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit.utils import algorithm_globals
from qiskit.utils import QuantumInstance

from qiskit.visualization.utils import (_bloch_multivector_data,_paulivec_data,matplotlib_close_if_inline,)
from qiskit.visualization import plot_bloch_multivector, plot_state_qsphere, plot_state_city, plot_bloch_vector
from qiskit.compiler import assemble
from qiskit.circuit.library.standard_gates import (IGate, U1Gate,XGate,YGate,ZGate,HGate,SGate,SdgGate,TGate,TdgGate,RXGate,RYGate,RZGate)

from matplotlib import pyplot as plt

import numpy as np
import time
import random
import sys


# %%
import time
import random
import sys
from qiskit import QuantumCircuit, BasicAer, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
#from azure.quantum.qiskit import AzureQuantumProvider
from qiskit.utils import algorithm_globals
from qiskit.utils import QuantumInstance
from qiskit.visualization import plot_bloch_multivector


#backend = provider.get_backend("ionq.simulator")
backend = BasicAer.get_backend('qasm_simulator')
sim = Aer.get_backend('aer_simulator')

# just of effects. add a delay of 1 second before performing any action
SLEEP_BETWEEN_ACTIONS = 0.1
MAX_VAL = 23
DICE_FACE = 4

player_turn_text = [
    "Your turn.",
    "Go.",
    "Please proceed.",
    "Lets win this.",
    "Are you ready?",
    "In a state of Quantum Superposition?",
    "Two Hadamards decide your fate..."
]
snake_bite = [
    "boohoo",
    "bummer",
    "snake bite",
    "oh no",
    "dang"
]

ladder_jump = [
    "woohoo",
    "woww",
    "nailed it",
    "oh my God...",
    "yaayyy"
]

def welcome_msg():
    msg = """
    Welcome to the Quantum Maze
    Version: 1.0.0
    Developed by: The Seekers
    
    Rules:
      1. Initally both the players are at starting position i.e. 0. 
         Take it in turns to roll the dice. 
         Move forward the number of spaces shown on the maze.
      2. The first player to solve the quantum maze is the winner.
      3. Hit enter to roll the dice.
    
    """
    print(msg)


def get_player_names():
    player1_name = None
    while not player1_name:
        player1_name = input("Please enter a valid name for first player: ").strip()

    player2_name = None
    while not player2_name:
        player2_name = input("Please enter a valid name for second player: ").strip()

    print("\nMatch will be played between '" + player1_name + "' and '" + player2_name + "'\n")
    return player1_name, player2_name


def get_dice_value():
    time.sleep(SLEEP_BETWEEN_ACTIONS)
    #function to roll the dice
    qc = QuantumCircuit(2, 2)
    qc.name = "dice roll"
    qc.h(0)
    qc.h(1)
    qc.measure([0,1], [0,1])
    job = execute(qc, backend = backend, shots = 1).result().get_counts()
    res = list(job.keys())[0]
    val = int(res, 2)
    final_val = val if val == 1 or val == 2 or val == 3 else 4
    return final_val


def last_puzzle():
  gate_list = ['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'Sdg', 'Tdg', 'RX', 'RY', 'RZ', 'U']
  print("Gates =", gate_list)
  gate = input("Please choose a gate from the gate list:")
  return gate  

def quantum_maze(player_name, current_value, dice_value):
    time.sleep(SLEEP_BETWEEN_ACTIONS)
    old_value = current_value

    #print("Current Value = "+str(current_value))
    #print("Dice Value = "+str(dice_value))
    if current_value == MAX_VAL or (current_value == 19 and dice_value == 4):
      if current_value == 19 and dice_value == 4:
        current_value += 4
      if dice_value == 4:
        print("Solve this Quantum Puzzle...")
        ##bloch_sphere function?
      else:
        print("Pass the dice to next player.", "You are in the box:", current_value )
        return current_value

    elif current_value == 0 and dice_value == 4:
      current_value = 4
      #print("Current Value = "+str(current_value))
      print("You got 1 more chance! Roll the dice.")
      next_rolled_val = get_dice_value()
      if current_value+next_rolled_val < MAX_VAL:
        current_value += next_rolled_val
        print("You got {}!.".format(next_rolled_val), "You are in the box:", current_value )
    
    elif current_value == 0 and dice_value != 4:
      if current_value+dice_value <= MAX_VAL:
        current_value = current_value + dice_value
        print("You got {}, pass the dice to next player.".format(dice_value), "You are in the box:", current_value )

    elif current_value > 0 and dice_value == 4:
      if current_value+4 <= MAX_VAL:
        current_value += 4
        print("You got 1 more chance! Roll the dice.")
        next_rolled_val = get_dice_value()
        if current_value+next_rolled_val < MAX_VAL:
          current_value += next_rolled_val
          print("You got {}! Roll the dice.".format(next_rolled_val), "You are in the box:", current_value )

    elif current_value > 0 and dice_value != 4:
      if current_value+dice_value <= MAX_VAL:
        current_value = current_value + dice_value
        print("You got {}, pass the dice to next player.".format(dice_value), "You are in the box:", current_value)
    else:
      print("Pass the chance to player-2")
      final_value = current_value
    #print("\n" + player_name + " moved from " + str(old_value) + " to " + str(current_value))
    return current_value

# %%
def blc_spr(state, title="", figsize=None, *, rho=None, filename=None):

    # Data
    bloch_data = _bloch_multivector_data(state)
    num = len(bloch_data)
    width, height = plt.figaspect(1 / num)
    fig = plt.figure(figsize=(width, height))
    for i in range(num):
        pos = i
        ax = fig.add_subplot(1, num, i + 1, projection="3d")
        #plot_bloch_vector(bloch_data[i], "qubit " + str(pos), ax=ax, figsize=figsize)
        plot_bloch_vector(bloch_data[i], ax=ax, figsize=figsize)
    fig.suptitle(title, fontsize=16, y=1.01)
    #matplotlib_close_if_inline(fig)
    return fig

    
# a = blc_spr([1,0])
# plt.pause(1)
# #plt.close('all')
# print(5)

# %%



gate_list = ['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'Sdg', 'Tdg', 'RX', 'RY', 'RZ', 'U']


def rand_bloch(num_qbits = 1, seed = None):
    gate_list = [XGate,IGate,XGate,HGate,YGate,ZGate,HGate,YGate,SGate,HGate,TGate,HGate]

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)

    rng = np.random.default_rng(seed)
    operat = rng.choice(gate_list)
    operat1 = rng.choice(gate_list)
    op = operat()
    op1 = operat1()
    pi = np.pi

    qc = QuantumCircuit(1)
    qc.append(op, [0])
    qc.append(op1, [0])
    qc.save_statevector()
    qobj = assemble(qc)  
    state = sim.run(qobj).result().get_statevector()
    return state



# def blc_spr(state, title="", figsize=None, *, rho=None, reverse_bits=False, filename=None):

#     # Data
#     bloch_data = (
#         _bloch_multivector_data(state)[::-1] if reverse_bits else _bloch_multivector_data(state)
#     )
#     num = len(bloch_data)
#     width, height = plt.figaspect(1 / num)
#     fig = plt.figure(figsize=(width, height))
#     for i in range(num):
#         pos = num - 1 - i if reverse_bits else i
#         ax = fig.add_subplot(1, num, i + 1, projection="3d")
#         plot_bloch_vector(bloch_data[i], "qubit " + str(pos), ax=ax, figsize=figsize)
#     fig.suptitle(title, fontsize=16, y=1.01)
#     #matplotlib_close_if_inline(fig)
#     return fig




def state_vec_circ(state):
    inp = [state[0], state[1]]
    svc = QuantumCircuit(1)  
    initial_state = inp
    svc.initialize(initial_state, 0) 
    return svc

def final_bloch_operation(gate, state):
    final_circuit = QuantumCircuit(1)
    final_circuit.append(state_vec_circ(state), [0])
    if gate == 'X' or 'x':
      final_circuit.x(0)

    elif gate == 'Y':
      final_circuit.y(0)

    elif gate == 'Z':
      final_circuit.z(0)

    elif gate == 'H':
      final_circuit.h(0)

    elif gate == 'S':
      final_circuit.s(0)

    elif gate == 'T':
      final_circuit.t(0)

    elif gate == 'U':
      theta = float(input("Please enter the values of Theta, Phi and Lambda:"))
      phi = float(input())
      lambd = float(input())
      final_circuit.u(theta, phi, lambd, 0)

    elif gate == 'RX':
      theta1 = float(input("Please enter the value of Theta:"))
      final_circuit.rx(theta1, 0)

    elif gate == 'RY':
      theta2 = float(input("Please enter the value of Theta:"))
      final_circuit.ry(theta2, 0)

    elif gate == 'RZ':
      theta3 = float(input("Please enter the value of Theta:"))
      final_circuit.rz(theta3, 0)

    else:
      final_circuit.barrier()

    return final_circuit

def check_win(player_name, position):
    time.sleep(SLEEP_BETWEEN_ACTIONS)
    if MAX_VAL == position:
        state = rand_bloch()
        gate = last_puzzle()
        final_state_circ = QuantumCircuit(1,1)
        final_state_circ.append(final_bloch_operation(gate, state), [0])
        final_state_circ.measure(0,0)
        job_final = execute(final_state_circ, backend = backend, shots = 1).result().get_counts()
        res_final = list(job_final.keys())[0]
        final_val = int(res_final, 2)
        if final_val ==0:
            print("\n\n\nThats it.\n\n" + player_name + " won the game.")
            print("Congratulations " + player_name)
            print("\nThank you for playing the game.")
            sys.exit(1)

def start():
    welcome_msg()
    time.sleep(SLEEP_BETWEEN_ACTIONS)
    player1_name, player2_name = get_player_names()
    time.sleep(SLEEP_BETWEEN_ACTIONS)

    player1_current_position = 0
    player2_current_position = 0

    while True:
        time.sleep(SLEEP_BETWEEN_ACTIONS)
        input_1 = input("\n" + player1_name + ": " + random.choice(player_turn_text) + " Hit the enter to roll dice: ")
        print("\nRolling dice...")
        dice_value = get_dice_value()
        print("You got", dice_value)
        time.sleep(SLEEP_BETWEEN_ACTIONS)
        print(player1_name + " moving....")
        player1_current_position = quantum_maze(player1_name, player1_current_position, dice_value)

        if player1_current_position == MAX_VAL:
            stt = rand_bloch()
            blc_spr(stt)
            plt.pause(1)
            check_win(player1_name, player1_current_position)
            blc_spr(stt)
            plt.pause(1)
            
        else:
            pass 
            check_win(player1_name, player1_current_position)

        input_2 = input("\n" + player2_name + ": " + random.choice(player_turn_text) + " Hit the enter to roll dice: ")
        print("\nRolling dice...")
        dice_value = get_dice_value()
        print("You got", dice_value)
        time.sleep(SLEEP_BETWEEN_ACTIONS)
        print(player2_name + " moving....")
        player2_current_position = quantum_maze(player2_name, player2_current_position, dice_value)
        print(player2_current_position)
        if player2_current_position == MAX_VAL:
            stt2 = rand_bloch()
            blc_spr(stt2)
            plt.pause(1)
            check_win(player2_name, player2_current_position)
            #blc_spr(stt2)
            
        else:
            pass
        
            check_win(player2_name, player2_current_position)

if __name__ == "__main__":
    start()

# %%

# %%
