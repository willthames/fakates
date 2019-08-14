import argparse


def create_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000,
                        help='port on which to listen')
    parser.add_argument('--host', default='127.0.0.1',
                        help='address on which to listen')
    parser.add_argument('--database', default='/tmp/db.json',
                        help='where to store the data')
    return parser.parse_args()
