import re
import glob
import json
import jinja2
import argparse
import os

def parse_msgs(msg_files):
    field_pattern = re.compile(
        '\s*'
        '(?P<type>(uint32|float32|uint64|bool))'
        '(\[(?P<num>\d+)\])?'
        '\s+'
        '(?P<name>\w+)'
        '\s+'
        '#\s*(?P<comment>.+)'
        )


    topic_pattern = re.compile(
        '\s*'
        '# TOPICS'
        '\s+'
        '(?P<topic>(\w+\s+)*)'
        )

    data = {}

    for msg_file in msg_files:
        msg_name = msg_file.split('.')[0]
        data[msg_name] = {
            'fields': {},
            'topics': [],
        }
        with open(msg_file, 'r') as f:
            for l in f.readlines():

                # try to read line as field
                m = re.match(field_pattern, l)
                if m is not None:
                    if m.group('num') is None:
                        num = 1
                    else:
                        num = int(m.group('num'))
                    data[msg_name]['fields'][m.group('name')] = {
                        'comment':  m.group('comment'),
                        'type':  m.group('type'),
                        'len':  num,
                    }
                    continue

                # try to read line as topic
                m = re.match(topic_pattern, l)
                if m is not None:
                    print('topic', m.group('topic'))
                    data[msg_name]['topics'] += [m.group('topic').strip().split(' ')]
                    continue
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser('msg parser')
    parser.add_argument('msg_dir')
    args = parser.parse_args()
    msg_files = glob.glob(os.path.join(os.path.abspath(args.msg_dir), '*.msg'))
    data = parse_msgs(msg_files)
    print(json.dumps(data, indent=2))
