# -*- coding: utf-8 -*- 
import cv2
import sys
from SudokuExtractor import extract_sudoku
from NumberExtractor import extract_number
from SolveSudoku import sudoku_solver
import random


f = open("sol.txt", 'w')

def output(a):
    sys.stdout.write(str(a))

def display_sudoku(sudoku,flag):
    if flag == True:

        for i in range(9):
            for j in range(9):
                cell = sudoku[i][j]
                if cell == 0 or isinstance(cell, set):
                    output('.')
                    f.write('.')
                else:
                    output(cell)
                    f.write(str(cell))
                if (j + 1) % 3 == 0 and j < 8:
                    output(' |')
                    f.write(' |')

                if j != 8:
                    output('  ')
                    f.write('  ')
            output('\n')
            f.write('\n')
            if (i + 1) % 3 == 0 and i < 8:
                output("--------+----------+---------\n")
                f.write("------+------+------\n")

    if flag == False:

        for i in range(9):
            for j in range(9):
                cell = sudoku[i][j]
                if cell == 0 or isinstance(cell, set):
                    output('.')
                else:
                    output(cell)
                if (j + 1) % 3 == 0 and j < 8:
                    output(' |')

                if j != 8:
                    output('  ')
            output('\n')
            if (i + 1) % 3 == 0 and i < 8:
                output("--------+----------+---------\n")


def demain(image_path):

    image = extract_sudoku(image_path)
    grid = extract_number(image)
    g_image = cv2.bitwise_not(image)
    cv2.imwrite('smu.jpg', g_image)
    print('Sudoku:')
    display_sudoku(grid.tolist(),False)
    solution = sudoku_solver(grid)
    print('Solution:') 
    f.write('Solution: \n')
    display_sudoku(solution.tolist(),True)

#demain(image_path = sys.argv[1])
demain('from_telegram.jpg')