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
    cost: tuple


class Solver:

    def __init__(self, threads=1, time_limit='umax'):
        self.model = None
        self.threads = threads
        self.time_limit = time_limit

    def new_model(self, model):
        assignment = dict()
        errors = []
        for symbol in model.symbols(shown=True):
            if symbol.name == 'assign':
                assignment[str(symbol.arguments[0])] = str(symbol.arguments[1])
            elif symbol.name == 'error':
                errors.append(symbol)
        self.model = Model(assignment, errors, model.cost)
        log.debug(f"New model with cost {model.cost}:")
        for k, v in self.model.assignment.items():
            log.debug(f'{k}: {v}')
        log.debug("-------------------")

    def solve(self, program):
        control = clingo.Control()
        control.add('base', [], program)
        control.ground([('base', [])])
        log.info(f"Solving with {self.threads} threads...")
        control.configuration.solve.parallel_mode = self.threads
        log.info(f"Setting time limit to {self.time_limit}")
        control.configuration.solve.solve_limit = self.time_limit
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
    parser.add_argument('-l',
                        '--time-limit',
                        help='Time limit',
                        type=str,
                        default='umax')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument(
        'preferences',
        help='The file containing the preferences of the students',
        nargs='+')
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    parsed_input = parse.parse(args.topics, args.preferences)
    programfile = open(os.path.dirname(__file__) + '/solve.lp', 'r')
    program = programfile.read()
    program += '\n' + parsed_input
    if args.program:
        with open(args.program, 'w') as programfile:
            programfile.write(program)
    solver = Solver(args.threads, args.time_limit)
    solver.solve(program)
    model = solver.get_model()
    if not model:
        log.error("No model found!")
        sys.exit(1)
    if model.errors:
        for error in model.errors:
            log.error(error)
    log.info(f'Final model with cost {model.cost}:')
    for k, v in model.assignment.items():
        log.info(f'{k}: {v}')
    if args.output:
        with open(args.output, 'w') as outputfile:
            for k, v in model.assignment.items():
                outputfile.write(f'{k}: {v}\n')


if __name__ == '__main__':
    main()
