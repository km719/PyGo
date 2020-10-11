# 10/5/2020: Board, place stones, click on existing stones to remove
# 10/6/2020: Capture indication and suicide prevention
# 10/8/2020: Piece removal on capture

# BUG  "Captured!" not showing up when captured pieces removed
# TODO Show current player
# TODO Avoid infinite loop of stone captures
# TODO Add a button to pass turn
# TODO Fade text out after some time
# TODO Enable online playign with sockets

from tkinter import *
import tkinter.font as tkFont
import time
master = Tk()

w = Canvas(master, width=500, height=500, bg="#ffc878")
w.pack()

titleFont = tkFont.Font(family='Helvetica', size=32, weight='bold')
captureFont = tkFont.Font(family='Helvetica', size=18)

w.create_text(250, 20, text="Go!", font=titleFont)

for i in range(9):
    w.create_line(50+(i*50), 50, 50+(i*50), 450)
    w.create_line(50, 50+(i*50), 450, 50+(i*50))
w.create_oval(146, 146, 154, 154, fill="black")
w.create_oval(346, 146, 354, 154, fill="black")
w.create_oval(146, 346, 154, 354, fill="black")
w.create_oval(346, 346, 354, 354, fill="black")
w.create_oval(246, 246, 254, 254, fill="black")

moves = 0

board = [
    [999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999]
]

stones = [
    [999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999],
    [999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999]
]


captureIndicate = [999, 999]

white = True
currentPlayer = w.create_oval


def draw(event):
    global white
    global board
    global stones
    global captureIndicate
    global moves
    w.delete(captureIndicate[1])
    captureIndicate[1] = 999
    w.delete(captureIndicate[0])
    captureIndicate[0] = 999
    numX = event.x
    numY = event.y
    numX = 50 * round(numX/50)
    numY = 50 * round(numY/50)
    if numX >= 50 and numX <= 450 and numY >= 50 and numY <= 450:
        r = int(numY/50)
        c = int(numX/50)
        if board[r][c] == 0:
            sui = suicide(r, c, white)
            if sui:
                captureIndicate[0] = w.create_text(
                    250, 480, text="That's suicidal", font=captureFont)  # display suicide warning
            elif white:
                color = "white"
                board[r][c] = 1
                white = False
                moves += 1
            else:
                color = "black"
                board[r][c] = -1
                white = True
                moves += 1
            if not(sui):
                x1, y1 = (numX - 15), (numY - 15)
                x2, y2 = (numX + 15), (numY + 15)
                stones[r][c] = w.create_oval(
                    x1, y1, x2, y2, fill=color, outline=color)
                if capture(r, c):
                    captureIndicate[0] = w.create_text(
                        250, 480, text="Captured!", font=captureFont)
        elif board[r][c] == 1 or board[r][c] == -1:
            w.delete(stones[r][c])
            board[r][c] = 0

# Check board for removing pieces


def suicide(r, c, w):
    global board
    if w:
        board[r][c] = 1
    else:
        board[r][c] = -1
    cap = capture(r, c)
    sui = island(r, c, [])
    board[r][c] = 0
    return sui and not(cap)


def capture(r, c):
    up = False
    down = False
    left = False
    right = False
    if board[r-1][c] == -1*board[r][c]:
        up = island(r-1, c, [])
    if board[r+1][c] == -1*board[r][c]:
        down = island(r+1, c, [])
    if board[r][c-1] == -1*board[r][c]:
        left = island(r, c-1, [])
    if board[r][c+1] == -1*board[r][c]:
        right = island(r, c+1, [])

    if up:
        removeCaptured(r-1, c)
    if down:
        removeCaptured(r+1, c)
    if left:
        removeCaptured(r, c-1)
    if right:
        removeCaptured(r, c+1)
    return up or down or left or right


def removeCaptured(r, c):
    global stones
    global board
    val = board[r][c]
    w.delete(stones[r][c])
    board[r][c] = 0
    if board[r-1][c] == val and val != 0:
        removeCaptured(r-1, c)
    if board[r+1][c] == val and val != 0:
        removeCaptured(r+1, c)
    if board[r][c-1] == val and val != 0:
        removeCaptured(r, c-1)
    if board[r][c+1] == val and val != 0:
        removeCaptured(r, c+1)


def island(r, c, checked):
    val = board[r][c]
    nVal = -1*val
    if [r, c] in checked:
        return True
    if board[r-1][c] == 0 or board[r+1][c] == 0 or board[r][c-1] == 0 or board[r][c+1] == 0:
        checked.append([r, c])
        return False
    if (board[r-1][c] != val or [r-1, c] in checked) and (board[r+1][c] != val or [r+1, c] in checked) and (board[r][c-1] != val or [r, c-1] in checked) and (board[r][c+1] != val or [r, c+1] in checked):
        checked.append([r, c])
        return True
    up = True
    down = True
    left = True
    right = True
    checked.append([r, c])
    if board[r-1][c] == val:
        up = island(r-1, c, checked)
        checked.append([r-1, c])
    if board[r+1][c] == val:
        down = island(r+1, c, checked)
        checked.append([r+1, c])
    if board[r][c-1] == val:
        left = island(r, c-1, checked)
        checked.append([r, c-1])
    if board[r][c+1] == val:
        right = island(r, c+1, checked)
        checked.append([r, c+1])
    return (up and down and left and right)


w.pack(expand=YES, fill=BOTH)
w.bind("<ButtonRelease-1>", draw)
master.title("Go!")
master.iconbitmap("GoPy/go-game-logo.ico")
mainloop()
