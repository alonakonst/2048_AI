import copy
def calculate_reward(board):
    reward = 0
    max_value=0
    count_of_two = 0
    count_of_four = 0
    count_of_zero = 0
    count_of_max = 0


    for row in range(4):
        for col in range(4):
            if board.board_values[row][col]==max_value:
                count_of_max += 1
            if board.board_values[row][col]==2:
                count_of_two += 1
            if board.board_values[row][col]==4:
                count_of_four += 1
            if board.board_values[row][col]==0:
                count_of_zero += 1
            if board.board_values[row][col]>max_value:
                count_of_max = 1
                max_value=board.board_values[row][col]


    #most valuable of the reward is max value
    if max_value==2048:
        reward += 30
    elif max_value==1024:
        reward += 25
    elif max_value == 512:
        reward += 15
    elif max_value == 256:
        reward -= 15
    elif max_value == 128:
        reward -= 30
    elif max_value == 64:
        reward -= 30
    elif max_value == 32:
        reward -= 30
    elif max_value == 16:
        reward -= 30
    elif max_value == 8:
        reward += 0
    elif max_value == 4:
        reward += 0
    elif max_value == 2:
        reward += 0


    #another component is concentration of zero:
    reward += (count_of_zero/(16-count_of_max))*10

    reward -= (count_of_two+count_of_four)*0.1*board.score

    w = [[4 ** 15, 4 ** 14, 4 ** 13, 4 ** 12],
         [4 ** 8, 4 ** 9, 4 ** 10, 4 ** 11],
         [4 ** 7, 4 ** 6, 4 ** 5, 4 ** 4],
         [4 ** 0, 4 ** 1, 4 ** 2, 4 ** 3]]

    eval = 0

    for i in range(4):
        for j in range(4):
            eval += w[i][j] * board.board_values[i][j]

    # print('eval', eval)



    reward += (board.score * eval * 0.00001)

    return reward
    

def monoticity_calculation(sequence):


    if all(sequence[i] >= sequence[i + 1] for i in range(len(sequence) - 1)):
        return 10  # Increasing monotonicity
    elif all(sequence[i] <= sequence[i + 1] for i in range(len(sequence) - 1)):
        return 10  # Decreasing monotonicity

    else:
        return 0

def list_moniticity(sequence, increasing):
    if increasing:
        return all(sequence[i] > sequence[i + 1] for i in range(len(sequence) - 1))
    else:
        return all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))
    

