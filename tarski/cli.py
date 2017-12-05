"""
A module that holds all the material needed for running the script.
"""
from argparse import ArgumentParser
import pkg_resources
import sys

from tarski.model import Model
from tarski.read.tarski import TarskiWorldReader

def get_plugins(group):
    """
    Get all the registered plugins.
    """
    return [entry.load() for entry in pkg_resources.iter_entry_points(group)]

def get_input_plugins():
    """
    Get all the plugins for loading files.
    """
    return get_plugins("tarski.readers")

def list_input_formats():
    """
    List all the input formats that the program understands.
    """
    format_string = "{:<20}{}"
    print(format_string.format("Format", "Description"))
    print('-' * 80)
    for plugin in get_input_plugins():
        print(format_string.format(plugin.format_name, plugin.format_description))

def find_plugin(format_):
    """
    Find the plugin with name `format_`.
    """
    for plugin in get_input_plugins():
        if plugin.format_name == format_:
            return plugin

def read_file(format_, file_):
    """
    Read in the world as specified in `file`.
    """
    with open(file_) as stream:
        reader = format_(stream=stream)
        world = reader.read_world()
        return Model(world=world)

def convert(files, iformat, output, use_header=None):
    """
    Convert all the files in `files` into the corresponding first order structures and write them to
    the output.

    :param list[string] files: A list of file names that need to be converted.
    :param output: The stream to write the output to.
    :param bool use_header: Whether or not to write a header for each file.
    """
    if len(files) > 1 and use_header is None:
        use_header = True
    for file_ in files:
        model = read_file(iformat, file_)
        if use_header:
            output.write('# {}\n'.format(file_))
        output.write(str(model))
        output.write('\n')

def main():
    """
    The main entrypoint for the script.
    """
    parser = ArgumentParser(description="""
    A utility for translating Tarski's World files into their corresponding first order structures.
    """)
    parser.add_argument("files", help="The Tarski's World file to convert.", nargs='*')
    parser.add_argument("--list-input-formats", action="store_true",
                        help="Give a list of the accepted input formats and exit")
    parser.add_argument("-f", "--format", default='tarski',
                        help="The format of the input file, defaults to tarski")
    args = parser.parse_args()
    if args.list_input_formats:
        list_input_formats()
        return 0
    if not args.files:
        parser.error("the following arguments are required: files")
    plugin = find_plugin(args.format)
    if plugin is None:
        parser.error("unrecognized format: {}".format(args.format))
    use_header = None
    convert(args.files, TarskiWorldReader, sys.stdout, use_header)

if __name__ == '__main__':
    main()
