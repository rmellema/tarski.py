"""
A module that holds all the material needed for running the script.
"""
from argparse import ArgumentParser

from tarski.model import Model
from tarski.read.tarski import TarskiWorldReader

def read_file(file):
    """
    Read in the world as specified in `file`.
    """
    with open(file) as stream:
        reader = TarskiWorldReader(stream=stream)
        world = reader.read_world()
        return Model(world=world)

def main():
    """
    The main entrypoint for the script.
    """
    parser = ArgumentParser(description="""
    A utility for translating Tarski's World files into their corresponding first order structures.
    """)
    parser.add_argument("files", help="The Tarski's World file to convert.", nargs="+")
    args = parser.parse_args()
    use_header = True
    for file in args.files:
        model = read_file(file)
        if use_header:
            print('# {}'.format(file))
        print(str(model))

if __name__ == '__main__':
    main()
