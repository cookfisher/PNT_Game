import copy
import math

import PNT_Player
#from PNT_Player import read_arg, generate_input_list

from numpy import inf
# Initial value of alpha be Double.NEGATIVE_INFINITY (which is in JAVA, not python, here we use the numpy)
# beta be Double.POSITIVE_INFINITY. Assume the worst case with infinity.
ALPHA = -inf
BETA = inf


class Node:
    def __init__(self, tokens_remain, parent, last_move, depth):
        self.tokens_remain = tokens_remain
        self.parent = parent
        self.last_move = last_move
        self.depth = depth
        self.e = 0
        self.children = []

        def addNode(self, obj):
            self.children.append(obj)
            self.depth += 1

        def addNodes(self, obj):
            self.children.extend(obj)
            self.depth += 1

        def setLast_move(self, last_move):
            self.last_move = last_move

        def setDepth(self, depth):
            self.depth = depth

        def get_tokens(self):
            return self.tokens_remain

        def getChildNodes(self):
            return self.children

        def getRemainTokens(self, parent, last_move):
            new_tokens_remain = copy.deepcopy(parent)
            new_tokens_remain.remove(last_move)
            return new_tokens_remain


def create_node(tokens_remain, parent_node, last_move, depth):
    return Node(tokens_remain, parent_node, last_move, depth)
    # return Node(tokens_remain, parent_node, last_move, depth, e)


# all possible nodes/choices
def findChildNodes(parent_node, first_turn): # , num_of_tokens
    tokens_remain = parent_node.tokens_remain
    #last_move = parent_node.last_move
    length = len(tokens_remain)
    child_nodes = []
    # At the first move
    if first_turn:
        for move in tokens_remain:
            if move < length/2 and move % 2 == 1:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                child_nodes.append(child_node)
                #child_nodes.insert(0, child_node)
    # At subsequent moves
    else:
        possible_moves = find_multiples_or_factors(parent_node.last_move, parent_node.tokens_remain)
        for move in tokens_remain:
            if move in possible_moves:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                child_nodes.append(child_node)
                #child_nodes.insert(0, child_node)

    print("Children of", parent_node.tokens_remain, "=", len(child_nodes))
    for i in range(len(child_nodes)):
        print(child_nodes[i].tokens_remain, "move =", child_nodes[i].last_move, "depth = ", child_nodes[i].depth)

    parent_node.children = child_nodes
    return child_nodes


# parameter is root and children in level 1
def build_tree(start_node, c1):
    global max_tree_depth
    c_Total = []
    if c1:
        for i in c1:
            c2 = findChildNodes(i, False)
            c_Total.extend(c2)
        max_tree_depth += 1
        return build_tree(start_node, c_Total)
    else:
        #print("TREE BUILT")
        return max_tree_depth


# return list of all multiples and factors,
# add (and XXX in tokens_remain) if want to return the elements in token_remain only
def find_multiples_or_factors(num, tokens_remain):
    factors_multiples = []
    # factors
    for i in range(1, num + 1):
        mod = num % i
        if mod == 0:
            factors_multiples.append(i)
    # multiples
    multiplier = 2
    n = num
    while n < max(tokens_remain):
        n *= multiplier
        if n <= max(tokens_remain):
            factors_multiples.append(n)
            multiplier += 1
            n = num
    print(num, "'s all factors and multiples (include taken token) in", tokens_remain, ": ", factors_multiples)
    return factors_multiples


def generate_list(number):
    tokens = []
    for i in range(number):
        tokens.append(i+1)
    print(tokens)
    return tokens


def is_max_turn(taken_tokens):
    # taken_tokens is list
    if len(taken_tokens) % 2 == 0:
        return True
    else:
        return False


def alpha_beta_search(node, depth, alpha, beta, maximizingPlayer):
    global best_state
    global num_of_e
    global num_nodes_visited

    child_nodes = node.children
    num_nodes_visited += len(child_nodes)

    #test children
    #for node in child_nodes:
        #print(node.tokens_remain)
    #print("alpha_beta_search depth =", depth)

    # If depth is 0, search to end game states and return the index of player.
    if depth == 0 or len(child_nodes) == 0:
        e = evaluation(maximizingPlayer, node, node.last_move)
        num_of_e += 1
        print(node.tokens_remain, "Move:", node.last_move)
        print("e =", e)
        print()
        best_state = node
        return e

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        for child in child_nodes:
            max_value = alpha_beta_search(child, depth - 1, alpha, beta, False)
            if max_value >= alpha:
                best_state = child
            alpha = max(alpha, max_value)
            # If beta is less or equal to alpha, break the loop
            if alpha >= beta:
                break
            #else:
                #best_state = child
                #print("Move:", best_state.last_move)
        #print("Max =", max_value)
        return max_value
    else:
        min_value = inf
        for child in child_nodes:
            min_value = alpha_beta_search(child, depth - 1, alpha, beta, True)
            if min_value <= beta:
                best_state = child
            beta = min(beta, min_value)
            if beta <= alpha:
                break
            #else:
                #best_state = child
                #print("Move:", best_state.last_move)
        #print("Min =", min_value)
        return min_value


def evaluation(isMaxTurn, node, last_move): # , num_of_tokens, turns
    e = 0
    # game end
    child_nodes = node.children
    if len(node.tokens_remain) == 0 or len(child_nodes) == 0:
        #Player A (MAX) wins: 1.0, Player B (MIN) wins: -1.0
        if isMaxTurn:   #min's turn & game finish /turns % 2 == 0
            e = -1.0
        else:               #max's turn & game finish
            e = 1.0
        #print("Value =", e)
        return e
    # max turn
    if isMaxTurn == True: # turns % 2 == 1
        # token 1 is not taken yet
        if 1 in node.tokens_remain:
            e = 0
            #print("Value =", e)
            return e
        # last move was 1
        if last_move == 1:
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = 0.5
            elif len(child_nodes) % 2 == 0:
                e = -0.5
            #print("Value =", e)
            return e
        # last move is a prime
        if is_prime(last_move):
            #child_nodes = findChildNodes(tokens_remain)
            prime_multiples = find_prime_multiples(last_move, child_nodes, True)
            if prime_multiples % 2 == 1:
                e = 0.7
            elif prime_multiples % 2 == 0:
                e = -0.7
            #print("Value =", e)
            return e
        #the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            prime_multiples = find_prime_multiples(largest_prime, child_nodes, False)

            if prime_multiples % 2 == 1:
                e = 0.6
            elif prime_multiples % 2 == 0:
                e = -0.6
            #print("Value =", e)
            return e
    # min turn
    if isMaxTurn == False:
        # token 1 is not taken yet
        if 1 in node.tokens_remain:
            e = 0
            return e
        # last move was 1
        if last_move == 1:
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = -0.5
            elif len(child_nodes) % 2 == 0:
                e = 0.5
            #print("Value =", e)
            return e
        # last move is a prime
        if is_prime(last_move):
            #child_nodes = findChildNodes(tokens_remain)
            prime_multiples = find_prime_multiples(last_move, child_nodes, True)
            if prime_multiples % 2 == 1:
                e = -0.7
            elif prime_multiples % 2 == 0:
                e = 0.7
            #print("Value =", e)
            return e
        # the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            prime_multiples = find_prime_multiples(largest_prime, child_nodes, False)

            if prime_multiples % 2 == 1:
                e = -0.6
            elif prime_multiples % 2 == 0:
                e = 0.6
            #print("Value =", e)
            return e



def is_prime(n):
    if n < 2:
        print("Is prime = ", False)
        return False
    else:
        if n % 2 == 0 or n % 3 == 0:
            print("Is prime = ", False)
            return False
        # all primes are of the form 6k ± 1
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                print("Is prime = ", False)
                return False
            i = i + 6
        print(n, "is prime =", True)
        return True


def find_prime_multiples(num, child_nodes, is_prime):
    num_of_multiples = 0
    multiplier = 1
    list_multiples = []
    for node in child_nodes:
        copy_tokens_remain = copy.deepcopy(node.tokens_remain)
        n = num

        if is_prime == True:
            multiplier = 2
        elif is_prime == False:
            multiplier = 1

        while n < max(copy_tokens_remain):
            n = num
            n *= multiplier
            if n <= max(copy_tokens_remain) and n in copy_tokens_remain:
                list_multiples.append(n)
                num_of_multiples += 1
            multiplier += 1
    print("Find prime multiples in all children =", num_of_multiples, ":",list_multiples)
    return num_of_multiples


def maxPrimeFactors (n):
    max_prime = -1
    while n % 2 == 0:
        max_prime = 2
        #n /= 2
        n >>= 1
    # find last odd integer that cannot divide n
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            max_prime = i
            n = n / i
    if n > 2:
        max_prime = n
    print("max_prime_factor:", max_prime)
    return int(max_prime)


# ----------Driver Code----------
#test
test_list2 = [4, 5, 6, 7, 8]

is_prime(31)
maxPrimeFactors(25)
find_multiples_or_factors(2,test_list2)

#start_node = create_node(test_list, None, 0, 0)
#second_node = create_node([3,6,7,9,12], start_node, 1, 1)
#third_node = create_node([3,4,5,7], start_node, 1, 1)

# test find_prime_multiples
#nodes = [second_node, third_node]
#find_prime_multiples(3, nodes, True)
#find_prime_multiples(3, nodes, False)
#print()

# e(n)
#test_node = create_node(test_list2, None, 0, 0)
#test_node.children = nodes
#evaluation(3, test_node, 5)

# PNT
if __name__ == '__main__':
    # ----------------global variable-------------
    # number of nodes evaluated
    num_of_e = 0
    # best move
    best_state = None
    # include root
    num_nodes_visited = 1
    # tree depth
    max_tree_depth = 0

    # ----------------------------------------------test case-----------------------------------------------
    #1 python pnt_game.py PNT_Player 3 0 0
    #2 python pnt_game.py PNT_Player 7 1 1 2
    #3 python pnt_game.py PNT_Player 10 3 4 2 6 4
    #4 python pnt_game.py PNT_Player 7 3 1 4 2 3
    #5 python pnt_game.py PNT_Player 8 3 3 1 2 0
    #6 python pnt_game.py PNT_Player 10 5 3 1 8 4 2 0

    #7 python pnt_game.py PNT_Player 7 2 3 6 3
    #8 python pnt_game.py PNT_Player 10 3 1 3 6 4
    #9 python pnt_game.py PNT_Player 10 1 3 4
    #0 python pnt_game.py PNT_Player 10 3 3 6 2 4
    # ----------------------------------------------test case-----------------------------------------------
    num_token, num_taken_token, taken_token, depth = PNT_Player.read_arg()
    user_input = PNT_Player.generate_input_list(num_token, taken_token)

    if len(taken_token) == 0:
        last_token = 0
    else:
        last_token = taken_token[-1]

    print('input list for child nodes is : ', user_input)
    print("last_token", last_token)
    print("taken_token", taken_token)
    print(depth)

    if len(user_input) == num_token:
        first_turn = True
    else:
        first_turn = False

    # root
    root = create_node(user_input, None, last_token, 0)
    nodes_depth1 = findChildNodes(root, first_turn)
    print(len(nodes_depth1))
    max_tree_depth = build_tree(root, nodes_depth1)
    print("max_tree_depth =", max_tree_depth)
    print()
    isMaxTurn = is_max_turn(taken_token)

    # If depth is 0, search to end game states (the whole tree)
    if depth == 0:
        e = alpha_beta_search(root, max_tree_depth, ALPHA, BETA, isMaxTurn)
        max_depth_reached = max_tree_depth
    else:
        e = alpha_beta_search(root, depth, ALPHA, BETA, isMaxTurn)
        max_depth_reached = min(max_tree_depth, depth)

    avg_factor = (num_nodes_visited - 1) / (num_nodes_visited - num_of_e)
    print("Move:", best_state.last_move)
    print("Value:", e)
    print("Number of Nodes Visited:", num_nodes_visited)
    print("Number of Nodes Evaluated:", num_of_e)
    print("Max Depth Reached:", max_depth_reached)
    print("Avg Effective Branching Factor:", round(avg_factor, 1))