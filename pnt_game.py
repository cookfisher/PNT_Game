import copy
import math

from numpy import inf
# Initial value of alpha be Double.NEGATIVE_INFINITY (which is in JAVA, not python, here we use the numpy)
# beta be Double.POSITIVE_INFINITY. Assume the worst case with infinity.
ALPHA = -inf
BETA = inf


class Node:
    def __init__(self, tokens_remain, parent, last_move, depth, best_state):
        self.tokens_remain = tokens_remain
        self.parent = parent
        self.last_move = last_move
        self.depth = depth
        self.e = 0
        self.children = []
        self.best_state = None

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
    return Node(tokens_remain, parent_node, last_move, depth, None)
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
    # At subsequent moves
    else:
        possible_moves = find_multiples_or_factors(parent_node.last_move, parent_node.tokens_remain)
        for move in tokens_remain:
            if move in possible_moves:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                child_nodes.append(child_node)

    print("Children of", parent_node.tokens_remain, "=", len(child_nodes))
    for i in range(len(child_nodes)):
        print(child_nodes[i].tokens_remain, "move =", child_nodes[i].last_move, "depth = ", child_nodes[i].depth)

    parent_node.children = child_nodes
    return child_nodes


# parameter is root and children in level 1
def build_tree(start_node, c1):
    global max_tree_depth
    cTotal = []
    #c1 = findChildNodes(start_node,turn)
    if c1:
        for i in c1:
            c2 = findChildNodes(i, False)
            cTotal+=c2
            #if c2:
                #i.addNodes(c2)
        max_tree_depth += 1
        #return build_tree(start_node, c2)
        return build_tree(start_node, cTotal)
    else:
        print("TREE BUILT")
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


# ---------------------------------back up-------------------------------------------
def min_max(node, depth, alpha, beta, maximizingPlayer):
    child_nodes = node.children
    # If depth is 0, search to end game states and return the index of player.
    if depth == 0 or len(child_nodes) == 0:
        return maximizingPlayer

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        for child in child_nodes:
            eval = min_max(child, depth - 1, alpha, beta, False)
            max_value = max(max_value, eval)
            alpha = max(alpha, eval)
            # If beta is less or equal to alpha, break the loop
            if beta <= alpha:
                break
        return max_value
            # recursive for the children
    else:
        min_value = inf
        for child in child_nodes:
            eval = min_max(child, depth - 1, alpha, beta, True)
            min_value = min(min_value, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_value



num_of_e = 0
#best_state = None
num_nodes_visited = 0
def alpha_beta_search(node, depth, alpha, beta, maximizingPlayer):
    #global best_state
    global num_of_e
    global num_nodes_visited


    child_nodes = node.children
    num_nodes_visited += len(child_nodes)
    #child_nodes.reverse()

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
        return e
        #return maximizingPlayer

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        #for child in child_nodes:
        for child in child_nodes:
            max_value = alpha_beta_search(child, depth - 1, alpha, beta, False)
            #max_value = max(max_value, eval)
            if max_value >= alpha:
                node.best_state = child
            alpha = max(alpha, max_value)
            # If beta is less or equal to alpha, break the loop
            if alpha >= beta:
                break
            #else:
                #node.best_state = child
                #print("Move:", best_state.last_move)
        #print("Max =", max_value)
        return max_value
            # recursive for the children
    else:
        min_value = inf
        for child in child_nodes:
            min_value = alpha_beta_search(child, depth - 1, alpha, beta, True)
            #min_value = min(min_value, eval)
            beta = min(beta, min_value)
            if min_value <= beta:
                node.best_state = child
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
    #child_nodes = findChildNodes(node, turns)
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

            #count = 0
            #multiplier = 1
            #while largest_prime < num_of_tokens:
                #count += 1
                #multiplier += 1
                #largest_prime *= multiplier

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

            # count = 0
            # multiplier = 1
            # while largest_prime < num_of_tokens:
            # count += 1
            # multiplier += 1
            # largest_prime *= multiplier

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
                #n = num
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
test_list = generate_list(7)
test_list2 = [2, 3, 4, 7, 8, 10]




is_prime(31)
maxPrimeFactors(25)
find_multiples_or_factors(4,test_list2)

start_node = create_node(test_list, None, 0, 0)
second_node = create_node([3,6,7,9,12], start_node, 1, 1)
third_node = create_node([3,4,5,7], start_node, 1, 1)

# test find_prime_multiples
nodes = [second_node, third_node]
find_prime_multiples(3, nodes, True)
find_prime_multiples(3, nodes, False)
print()

# e(n)
#test_node = create_node(test_list2, None, 0, 0)
#test_node.children = nodes
#evaluation(3, test_node, 5)

# PNT
if __name__ == '__main__':
# global variable
    # tree depth
    max_tree_depth = 0

    #input1 = [1, 2, 3]
    #input2 = [2, 3, 4, 5, 6, 7]
    input3 = [1, 3, 5, 7, 8, 9, 10]
    #input4 = [3, 5, 6, 7]

    total = 10
    if len(input3) == total:
        turn = True
    else:
        turn = False

    #start1 = create_node(input1, None, 0, 0)
    #start2 = create_node(input2, None, 1, 0)
    start3 = create_node(input3, None, 6, 0)
    #start4 = create_node(input4, None, 2, 0)

# find the children node in depth = 1
    #c1 = findChildNodes(start1, turn)
    #c2 = findChildNodes(start2, turn)
    c3 = findChildNodes(start3, True)
    #c4 = findChildNodes(start4, turn)
    if len(c3) > 0:
        max_tree_depth += 1

    #depth = build_tree(start1, c1)
    #depth = build_tree(start2, c2)
    depth = build_tree(start3, c3)
    print()

    #isMaxTurn = is_max_turn([])
    #isMaxTurn = is_max_turn([1])
    isMaxTurn = is_max_turn([2,4,6])
    #isMaxTurn = is_max_turn([1, 2, 4])

    #e2 = alpha_beta_search(start2, 2, ALPHA, BETA, isMaxTurn)
    e3 = alpha_beta_search(start3, 4, ALPHA, BETA, isMaxTurn)
    #e4 = alpha_beta_search(start4, 3, ALPHA, BETA, isMaxTurn)

    limit_depth = 4

    avg_factor = (num_nodes_visited - 1) / (num_nodes_visited - num_of_e)
    print(start3.best_state.last_move)
    print("Value:", e3)
    print("Number of Nodes Visited:", num_nodes_visited)
    print("Number of Nodes Evaluated:",num_of_e)
    print("Max Depth Reached:", min(max_tree_depth,limit_depth))
    print("Avg Effective Branching Factor:", avg_factor)