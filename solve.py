#!/usr/bin/env python3

import argparse
import parse
import clingo
import logging
import sys
import os.path

from dataclasses import dataclass

logging.basicConfig()
log = logging.getLogger("solver")
log.setLevel(logging.INFO)


@dataclass
class Model:
    assignment: dict()
    errors: list


class Solver:

    def __init__(self, threads=1):
        self.model = None
        self.threads = threads

    def new_model(self, model):
        assignment = dict()
        errors = []
        for symbol in model.symbols(shown=True):
            if symbol.name == 'assign':
                assignment[str(symbol.arguments[0])] = str(symbol.arguments[1])
            elif symbol.name == 'error':
                errors.append(symbol)
        self.model = Model(assignment, errors)
        log.info("New model:")
        for k, v in self.model.assignment.items():
            log.info(f'{k}: {v}')
        log.info("-------------------")

    def solve(self, program):
        control = clingo.Control()
        control.add('base', [], program)
        control.ground([('base', [])])
        log.info(f"Solving with {self.threads} threads...")
        control.configuration.solve.parallel_mode = self.threads
        res = control.solve(on_model=self.new_model)

    def get_model(self):
        return self.model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--topics',
                        help='The file containing the topics')
    parser.add_argument('-o', '--output', help='The output file')
    parser.add_argument('-p',
                        '--program',
                        help='Output file for the final program')
    parser.add_argument('-n',
                        '--threads',
                        help='Number of threads',
                        type=int,
                        default=1)
    parser.add_argument(
        'preferences',
        help='The file containing the preferences of the students',
        nargs='+')
    args = parser.parse_args()
    parsed_input = parse.parse(args.topics, args.preferences)
    programfile = open(os.path.dirname(__file__) + '/solve.lp', 'r')
    program = programfile.read()
    program += '\n' + parsed_input
    if args.program:
        programfile = open(args.program, 'w')
        programfile.write(program)
    solver = Solver(args.threads)
    solver.solve(program)
    model = solver.get_model()
    if model.errors:
        for error in model.errors:
            log.error(error)
        sys.exit(1)
    if args.output:
        with open(args.output, 'w') as outputfile:
            for k, v in model.assignment.items():
                outputfile.write(f'{k}: {v}\n')


if __name__ == '__main__':
    main()
