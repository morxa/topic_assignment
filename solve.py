#!/usr/bin/env python3

import argparse
import parse
import clingo
import logging
import sys

from dataclasses import dataclass

logging.basicConfig()
log = logging.getLogger("solver")


@dataclass
class Model:
    assignment: dict()
    errors: list


class Solver:

    def __init__(self):
        self.model = None

    def new_model(self, model):
        assignment = dict()
        errors = []
        for symbol in model.symbols(shown=True):
            if symbol.name == 'assign':
                assignment[str(symbol.arguments[0])] = str(symbol.arguments[1])
            elif symbol.name == 'error':
                errors.append(symbol)
        self.model = Model(assignment, errors)

    def solve(self, program):
        control = clingo.Control()
        control.add('base', [], program)
        control.ground([('base', [])])
        res = control.solve(on_model=self.new_model)

    def get_model(self):
        return self.model


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
    model = solver.get_model()
    if model.errors:
        for error in model.errors:
            log.error(error)
        sys.exit(1)
    for k, v in model.assignment.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    main()
