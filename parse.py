#!/usr/bin/env python3

import argparse
import os.path
import logging

logging.basicConfig()
log = logging.getLogger("parser")


def parse(topic_path, student_paths):
    topicfile = open(topic_path, 'r')
    topics = []
    output = ""
    for topic in topicfile:
        topics.append(topic.strip())
    for topic in topics:
        output += f'topic("{topic}").\n'
    for studentfile in student_paths:
        try:
            student = os.path.basename(studentfile)
            student = int(os.path.splitext(student)[0])
        except (ValueError, IndexError):
            log.error(f'Invalid student file name: {studentfile}')
            continue
        output += f'student({student}).\n'
        for line in open(studentfile, 'r'):
            line = line.strip()
            if line == '':
                continue
            if line in topics:
                # No preference given
                continue
            try:
                key, val = line.split(' ', 1)
            except ValueError:
                print(f'Error in {studentfile}: {line}')
                continue
            if key == 'team':
                output += f'team({student}, {val}).\n'
            elif key == 'own':
                output += f'own({student}, "{val}").\n'
            else:
                topic = val.strip()
                if not topic in topics:
                    log.error(f'Student {student}: unknown topic "{topic}"')
                    continue
                try:
                    pref = int(key.strip())
                except ValueError:
                    log.error(f'Student {student}: invalid preference "{key}"')
                    continue
                output += f'pref({student}, "{topic}", {pref}).\n'
    return output


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
    output = open(args.output, 'w')
    output.write(parse(args.topics, args.preferences))


if __name__ == '__main__':
    main()
