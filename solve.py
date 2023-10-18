#!/usr/bin/env python3

import argparse
import parse
import clingo


class Solver:

    def __init__(self):
        self.assignment = dict()

    def new_model(self, model):
        self.assignment = dict()
        for symbol in model.symbols(shown=True):
            if symbol.name == 'assign':
                self.assignment[str(symbol.arguments[0])] = str(
                    symbol.arguments[1])

    def solve(self, program):
        control = clingo.Control()
        control.add('base', [], program)
        control.ground([('base', [])])
        res = control.solve(on_model=self.new_model)

    def get_assignment(self):
        return self.assignment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--topics',
                        help='The file containing the topics')
    parser.add_argument('-o', '--output', help='The output file')
    parser.add_argument(
        'preferences',
        help='The file containing the preferences of the students',
        nargs='+')
    args = parser.parse_args()
    parsed_input = parse.parse(args.topics, args.preferences)
    programfile = open('solve.lp', 'r')
    program = programfile.read()
    program += '\n' + parsed_input
    solver = Solver()
    solver.solve(program)
    assignment = solver.get_assignment()
    for k, v in assignment.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
