# Connor Ren ICS 3U CPT GAME 2048-"64Version" JUNE 16 2020

import os
import random
import itertools
from sys import exit


print('For this game, you will win if you got a 32(16 + 16)')


def trim(seqs, direction=0):
    return ([0, 0, 0, 0] + [n for n in seqs if n])[-4:] if direction else ([n for n in seqs if n] + [0, 0, 0, 0])[:4]


def sum_seqs(seqs, direction=0):
    if seqs[1] and seqs[2] and seqs[1] == seqs[2]:
        return trim([seqs[0], seqs[1] * 2, 0, seqs[3]], direction=direction)
    if seqs[0] and seqs[1] and seqs[0] == seqs[1]:
        seqs[0], seqs[1] = seqs[0] * 2, 0
    if seqs[2] and seqs[3] and seqs[2] == seqs[3]:
        seqs[2], seqs[3] = seqs[2] * 2, 0
    return trim(seqs, direction=direction)


def up(grid):
    for col in [0, 1, 2, 3]:

        for _idx, n in enumerate(sum_seqs(trim([row[col] for row in grid]))):
            grid[_idx][col] = n

    return grid


def down(grid):
    for col in [0, 1, 2, 3]:

        for _idx, n in enumerate(sum_seqs(trim([row[col] for row in grid], direction=1), direction=1)):
            grid[_idx][col] = n

    return grid


def left(grid):
    return [sum_seqs(trim(row)) for row in grid]


def right(grid):
    return [sum_seqs(trim(row, direction=1), direction=1) for row in grid]


'''
The Main code of the game
'''


class Game:
    grid = []
    controls = ["w", "a", "s", "d"]

    def game_field(self):
        number = random.choice([4, 2, 4, 2, 4, 2, 4, 2, 4, 2, 4, 2])

        x, y = random.choice([(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.grid[x][y] == 0])
        self.grid[x][y] = number

    def print_screen(self):
        os.system('clear')
        print('-' * 21)
        for row in self.grid:
            print('|{}|'.format("|".join([str(col or ' ').center(4) for col in row])))
            print('-' * 21)

    def logic(self, control):
        grid = {'w': up, 'a': left, 's': down, 'd': right}[control]([[c for c in r] for r in self.grid])

        if grid != self.grid:
            del self.grid[:]
            self.grid.extend(grid)
            if [n for n in itertools.chain(*grid) if n >= 64]:
                return 1, '''
  Congratulations!
(*^__^*) YOU WIN!!!!
                '''
            self.game_field()

        else:
            if not [1 for g in [f(grid) for f in [up, down, left, right]] if g != self.grid]:
                return -1, '''
I'm so sorry, but you can start another round for free!!!
( >﹏<。)～ YOU LOST!!!!
                '''

        return 0, ''

    def main_loop(self):
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.game_field()
        self.game_field()

        while True:
            self.print_screen()
            control = input('Please use w/a/s/d to control the game:')
            if control in self.controls:
                status, info = self.logic(control)

                if status:
                    print(info)

                    if input('Start another round?[y/n]').lower() == "y":
                        break

                    else:
                        exit(0)
        self.main_loop()


if __name__ == "__main__":
    Game().main_loop()
