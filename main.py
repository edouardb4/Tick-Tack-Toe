from graphics import *
from board import *
import time

board = Board("gray", 375 // 2, 375 // 2, 375, 375)
controller = BoardController(board)
logic = BoardLogic(board)


def main():
    win = GraphWin("Test", 750, 750)
    win.setBackground("black")
    win.bind_all("<Button-1>", click_callback)
    while 1:
        play(win)
        win.mainloop(1)
    win.close()


def click_callback(event):
    if not controller.player_turn:
        return
    if controller.is_winner():
        return
    indexes = determine_index(event)
    print(indexes)
    if indexes == -1:
        return
    if logic.is_slot_taken(indexes[1], indexes[0]):
        return
    board.push(1, indexes[0], indexes[1])
    controller.player_turn = 0


def determine_index(event):
    if board.x + board.width < event.x or board.x > event.x:
        return -1
    if board.y + board.height < event.y or board.y > event.y:
        return -1
    return [(3 * (event.x - board.x)) // board.width, (3 * (event.y - board.y)) // board.height]


def play(win):
    if len(logic.get_free_slots()) == 0 or controller.is_winner():
        board.render(win)
        return
    if not controller.is_player_turn():
        logic.play_turn()
        controller.player_turn = 1
    board.render(win)


main()
