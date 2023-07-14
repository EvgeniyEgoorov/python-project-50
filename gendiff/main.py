import argparse
from gendiff.scripts.generate_diff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output', default='stylish')

    args = vars(parser.parse_args())
    return generate_diff(args['first_file'], args['second_file'], args['format'])


if __name__ == "__main__":
    print(main())
