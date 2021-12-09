from graphics import *


class Board:
    def __init__(self, color, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board = [[-3, -3, -3], [-3, -3, -3], [-3, -3, -3]]
        self.color = color

    def render_line(self, win, line):
        line.setFill(self.color)
        line.setWidth(2)
        line.draw(win)

    def push(self, type, column, row):
        arr = self.board[row]
        arr[column] = type

    def render(self, win):
        for i in range(1, 3) :
            x = int(self.x + self.width * i / 3.0)
            y = self.y + self.height
            line = Line(Point(x, self.y), Point(x, y))
            self.render_line(win, line)
            x = self.x + self.width
            y = int(self.y + self.height * i / 3.0)
            line = Line(Point(self.x, y), Point(x, y))
            self.render_line(win, line)
        for i in range(0, len(self.board)):
            arr = self.board[i]
            for j in range(0, len(arr)):
                if arr[j] <= -1:
                    continue
                self.render_type(win, arr[j], i, j)

    def render_type(self, win, type, row, column):
        x = self.x + self.width * column / 3.0
        y = self.y + self.height * (row + 1) / 3.0
        if type == 0 :
            self.render_circle(win, x, y, self.width / 6.0)
        elif type == 1:
            self.render_x(win, x, y, self.width / 3.0, self.height / 3.0)

    def render_circle(self, win, x, y, radius):
        circle = Circle(Point(x + radius - 1, y - radius - 1), radius - 1)
        circle.setFill("black")
        circle.setOutline("red")
        circle.setWidth(2)
        circle.draw(win)

    def render_x(self, win, x, y, width, height):
        lines = [Line(Point(x, y), Point(x + width, y - height)), Line(Point(x, y - height), Point(x + width, y))]
        for i in range(0, len(lines)) :
            line = lines[i]
            line.setWidth(2)
            line.setFill("blue")
            line.draw(win)


class BoardController :

    def __init__(self, board):
        self.board_object = board
        self.board = board.board
        self.player_turn = 1

    def get_winner(self):
        for i in range(0, len(self.board)):
            sum_board = [0, 0]
            for j in range(0, len(self.board[0])):
                sum_board[0] += self.board[i][j]
                sum_board[1] += self.board[j][i]
            if sum_board[0] == 0 or sum_board[1] == 0:
                return 0
            elif sum_board[0] == 3 or sum_board[1] == 3:
                return 1
        sum_board = [0, 0]
        for i in range(0, len(self.board[0])):
            sum_board[0] += self.board[i][i]
            j = len(self.board[0]) - (i + 1)
            sum_board[1] += self.board[j][i]
        if sum_board[0] == 0 or sum_board[1] == 0:
            return 0
        elif sum_board[0] == 3 or sum_board[1] == 3:
            return 1
        return -1

    def is_winner(self):
        return self.get_winner() != -1

    def is_player_turn(self):
        return self.player_turn


class BoardLogic:

    def __init__(self, board):
        self.board = board

    def play_turn(self):
        free_slots = self.get_free_slots()
        remaining_slots = []
        for i in range(0, len(self.board.board)):
            sum_board = [0, 0]
            for j in range(0, len(self.board.board[0])):
                if self.board.board[i][j] == 1:
                    sum_board[0] += 1
                if self.board.board[j][i] == 1:
                    sum_board[1] += 1
            if sum_board[0] == 2:
                slot = self.find_free_slot(i, 0)
                if slot != -1:
                    self.board.push(0, slot, i)
                    return
            if sum_board[1] == 2:
                slot = self.find_free_slot(i, 1)
                if slot != -1:
                    self.board.push(0, i, slot)
                    return
            if sum_board[0] == 1:
                slot = self.find_free_slot(i, 0)
                if slot != -1:
                    remaining_slots.append([i, slot])
            if sum_board[1] == 1:
                slot = self.find_free_slot(i, 1)
                if slot != -1:
                    remaining_slots.append([slot, i])
        sum_board = [0, 0]
        for i in range(0, len(self.board.board)):
            if self.board.board[i][i] == 1:
                sum_board[0] += 1
            j = len(self.board.board) - (i + 1)
            if self.board.board[j][i] == 1:
                sum_board[1] += 1
        if sum_board[0] == 2:
            slot = self.find_free_slot(0, 2)
            if slot != -1:
                self.board.push(0, slot, slot)
                return
        if sum_board[1] == 2:
            slot = self.find_free_slot(0, 3)
            if slot != -1:
                self.board.push(0, slot[1], slot[0])
                return
        if sum_board[0] == 1:
            if slot != -1:
                slot = self.find_free_slot(0, 2)
                remaining_slots.append(slot)
        if sum_board[1] == 1:
            if slot != -1:
                slot = self.find_free_slot(0, 3)
                remaining_slots.append(slot)

        if len(remaining_slots) > 0:
            self.board.push(0, remaining_slots[0][0], remaining_slots[0][1])
            return
        #last resort yolo
        self.board.push(0, free_slots[0][1], free_slots[0][0])

    def find_free_slot(self, index, direction):
        if direction == 0:
            for i in range(0, len(self.board.board[0])):
                if self.board.board[index][i] <= -1:
                    return i
        elif direction == 1:
            for i in range(0, len(self.board.board)):
                if self.board.board[i][index] <= -1:
                    return i
        elif direction == 2:
            for i in range(0, len(self.board.board)):
                if self.board.board[i][i] <= -1:
                    return i
        elif direction == 3:
            for i in range(0, len(self.board.board)):
                j = len(self.board.board) - (i + 1)
                if self.board.board[j][i] <= -1:
                    return [j, i]
        return -1


    def get_free_slots(self):
        board = self.board.board
        free_slots = []
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] <= -1:
                    free_slots.append([i, j])
        return free_slots

    def is_slot_taken(self, row, column):
        free_slots = self.get_free_slots()
        for i in range(0, len(free_slots)):
            if row == free_slots[i][0] and column == free_slots[i][1]:
                return 0
        return 1



