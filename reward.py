#reward of the final state of the board involves final score, 'snape-shape' evaluation and count of tiles two and four

def calculate_reward(board):
    reward = 0
    max_value=0
    count_of_two = 0
    count_of_four = 0

    for row in range(4):
        for col in range(4):
            if board.board_values[row][col]==2:
                count_of_two += 1
            if board.board_values[row][col]==4:
                count_of_four += 1

    #weighted matrix for assesing 'snape-shaped' position of the board. Taken from https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
    w = [[16, 15, 14,13],
         [9, 10, 11, 12],
         [8, 7, 6, 5],
         [1, 2, 3, 4]]

    eval = 0

    for i in range(4):
        for j in range(4):
            eval += w[i][j] * board.board_values[i][j]

    reward = (board.score) + eval - (count_of_two+count_of_four)*0.1*board.score
    return reward
