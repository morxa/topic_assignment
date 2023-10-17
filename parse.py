#!/usr/bin/env python3

import argparse
import os.path


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

    topicfile = open(args.topics, 'r')
    topics = []
    output = open(args.output, 'w')
    for topic in topicfile:
        topics.append(topic.strip())
    for topic in topics:
        output.write(f'topic("{topic}").\n')
    for studentfile in args.preferences:
        student = os.path.basename(studentfile)
        student = os.path.splitext(student)[0]
        output.write(f'student({student}).\n')
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
                output.write(f'team({student}, {val}).\n')
            else:
                topic = val.strip()
                pref = key.strip()
                assert topic in topics, f'Student {student}: unknown topic {topic}, available topics: {topics}'
                output.write(f'pref({student}, "{topic}", {pref}).\n')


if __name__ == '__main__':
    main()
