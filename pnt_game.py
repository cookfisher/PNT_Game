import copy
import math

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



def create_node(tokens_remain, parent_node, last_move, depth):
    return Node(tokens_remain, parent_node, last_move, depth)
    # return Node(tokens_remain, parent_node, last_move, depth, e)


# all possible nodes/choices
def findChildNodes(parent_node, turns, num_of_tokens):
    tokens_remain = parent_node.tokens_remain
    last_move = parent_node.last_move
    length = len(tokens_remain)
    child_nodes = []
    # At the first move
    if turns == 1:
        for move in tokens_remain:
            if move < length/2 and move % 2 == 1:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                e = evaluation(turns, child_node, last_move, num_of_tokens)
                child_node.e = e
                child_nodes.append(child_node)
    # At subsequent moves
    else:
        possible_moves = find_multiples_or_factors(parent_node.last_move, parent_node.tokens_remain)
        for move in tokens_remain:
            if move in possible_moves:
                new_tokens_remain = copy.deepcopy(tokens_remain)
                new_tokens_remain.remove(move)
                child_node = create_node(new_tokens_remain, parent_node, move, parent_node.depth + 1)
                e = evaluation(turns, child_node, last_move, num_of_tokens)
                child_node.e = e
                child_nodes.append(child_node)
    print("Children of", parent_node.tokens_remain, "=", len(child_nodes))
    #parent_node.children = child_nodes
    return child_nodes


# return list of all multiples and factors
def find_multiples_or_factors(num, tokens_remain):
    factors_multiples = []
    # factors
    for i in range(1, num + 1):
        if num % i == 0:
            factors_multiples.append(i)
    # multiples
    multiplier = 2
    n = num
    while n < len(tokens_remain):
        n *= multiplier
        if n <= len(tokens_remain):
            factors_multiples.append(n)
            multiplier += 1
            n = num
    print(num, "'s factors and multiples in", tokens_remain, ": ", factors_multiples)
    return factors_multiples


def generate_list(number):
    tokens = []
    for i in range(number):
        tokens.append(i+1)
    print(tokens)
    return tokens


def is_max_turn(taken_tokens):
    # taken_tokens is list
    if len(taken_tokens) % 2 == 1:
        return True
    else:
        return False


def min_max(node, depth, alpha, beta, maximizingPlayer):
    child_nodes = node.children
    # If depth is 0, search to end game states and return the index of player.
    if depth == 0 or len(child_nodes) == 0:
        return maximizingPlayer

    # The player is max
    if maximizingPlayer:
        max_value = -inf
        for child in child_nodes:
            eval = min_max(child, depth - 1, alpha, beta, False)        #--------why depth-1 not+1?-----------
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


def evaluation(turns, node, last_move, num_of_tokens):
    e = 0
    # game end
    child_nodes = findChildNodes(node, turns, num_of_tokens)
    if len(node.tokens_remain) == 0 or len(child_nodes) == 0:
        #Player A (MAX) wins: 1.0, Player B (MIN) wins: -1.0
        if turns % 2 == 0:   #min's turn & game finish
            e = 1.0
        else:               #max's turn & game finish
            e = -1.0
        return e
    # max turn
    if turns % 2 == 1:
        # token 1 is not taken yet
        if 1 in node.tokens_remain:
            e = 0
            return e
        # last move was 1
        if last_move == 1:
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = 0.5
            elif len(child_nodes) % 2 == 0:
                e = -0.5
            return e
        # last move is a prime
        if is_prime(last_move):
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = 0.7
            elif len(child_nodes) % 2 == 0:
                e = -0.7
            return e
        #the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            count = 0
            multiplier = 1
            while largest_prime < num_of_tokens:
                count += 1
                multiplier += 1
                largest_prime *= multiplier

            if count % 2 == 1:
                e = 0.6
            elif count % 2 == 0:
                e = -0.6
            return e
    # min turn
    if turns % 2 == 0:
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
            return e
        # last move is a prime
        if is_prime(last_move): ##TODO: fix counts in all successors
            #child_nodes = findChildNodes(tokens_remain)
            if len(child_nodes) % 2 == 1:
                e = -0.7
            elif len(child_nodes) % 2 == 0:
                e = 0.7
            return e
        # the last move is not prime
        else:
            largest_prime = maxPrimeFactors(last_move)
            count = 0
            multiplier = 1
            while largest_prime < num_of_tokens: ##TODO: max in tokens list
                count += 1
                multiplier += 1
                largest_prime *= multiplier

            if count % 2 == 1:
                e = -0.6
            elif count % 2 == 0:
                e = 0.6
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
# test_list = [5]
# test_list = generate_list(7)
test_list = generate_list(12)
test_list2 = [1, 3, 4, 7, 8, 10]
#
is_prime(31)
maxPrimeFactors(25)
find_multiples_or_factors(4,test_list)

start_node = create_node(test_list, None, 0, 0)
children = findChildNodes(start_node, 3, len(test_list))
for i in children:
    print(i.tokens_remain)

#evaluation(1, test_list2, 2, len(test_list))

# PNT
turn = 1