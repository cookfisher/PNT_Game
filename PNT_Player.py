import sys
# Read command line arguments
#parser = argparse.ArgumentParser(description='Process input path parameter')
#Read the player
#parser.add_argument('PNT_Player', help='PNT Player')
#parser.add_argument('num_token', type=int, help='The total number of tokens in the game')
#parser.add_argument('taken_token', type=int, help='The total number of tokens that have already been taken in the previous moves.')

# python PNT_Player.py PNT_Player 7 2 3 6 0
# output: 7, 2, [3, 6], 0
def read_arg():
    arg_length = len(sys.argv)
    num_token = 0
    num_taken_token = 0
    taken_token = 0
    depth = 0
    #print('num of taken token')
    #print(sys.argv[4:len(sys.argv)-1])

    # python PNT_Player.py PNT_Player 7 2 3 6 0
    # output: 'PNT_Player', '2', [3, 6], '0'
    # based on the assumption from the assignment mentioned, we don't need to verify the input valid (assume it's always valid.)
    if arg_length > 4:
        num_token = sys.argv[2]
        num_taken_token = sys.argv[3]
        # print(num_taken_token)
        taken_token = sys.argv[4:arg_length-1]
        # print(taken_token)
        depth = sys.argv[arg_length - 1]
    else:
        depth = sys.argv[arg_length - 1]

    # convert to int list
    list_taken_token = []
    if arg_length > 4:
        for item in taken_token:
            list_taken_token.append(int(item))

    # return all values
    return int(num_token), int(num_taken_token), list_taken_token, int(depth)

# python PNT_Player.py 7 2 3 6 0
# output: 7, 2, [3, 6], 0
def read_arg_without_player():
    arg_length = len(sys.argv)
    num_token = 0
    num_taken_token = 0
    taken_token = 0
    depth = 0
    #print('num of taken token')
    #print(sys.argv[4:len(sys.argv)-1])

    # python PNT_Player.py PNT_Player 7 2 3 6 0
    # output: 'PNT_Player', '2', [3, 6], '0'
    # based on the assumption from the assignment mentioned, we don't need to verify the input valid (assume it's always valid.)
    if arg_length > 3:
        num_token = sys.argv[1]
        num_taken_token = sys.argv[2]
        # print(num_taken_token)
        taken_token = sys.argv[3:arg_length-1]
        # print(taken_token)
        depth = sys.argv[arg_length - 1]
    else:
        depth = sys.argv[arg_length - 1]

    # convert to int list
    list_taken_token = []
    if arg_length > 3:
        for item in taken_token:
            list_taken_token.append(int(item))

    # return all values
    return int(num_token), int(num_taken_token), list_taken_token, int(depth)

num_token, num_taken_token, taken_token, depth = read_arg()
print(read_arg())
# 2nd method without pnt player input
#print('The second method')
#print(read_arg_without_player())

