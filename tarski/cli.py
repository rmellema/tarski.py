"""
A module that holds all the material needed for running the script.
"""
import sys
from argparse import ArgumentParser
import pkg_resources

import tarski
from tarski.model import Model

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

def get_output_plugins():
    """
    Get all the plugins for outputting models.
    """
    return get_plugins("tarski.writers")

def list_input_formats():
    """
    List all the input formats that the program understands.
    """
    format_string = "{:<20}{}"
    print(format_string.format("Format", "Description"))
    print('-' * 80)
    for plugin in get_input_plugins():
        print(format_string.format(plugin.format_name, plugin.format_description))

def list_output_formats():
    """
    List all the output formats that the program understands.
    """
    format_string = "{:<20}{}"
    print(format_string.format("Format", "Description"))
    print('-' * 80)
    for plugin in get_output_plugins():
        print(format_string.format(plugin.format_name, plugin.format_description))

def find_input_plugin(format_):
    """
    Find the plugin with name `format_`.
    """
    for plugin in get_input_plugins():
        if plugin.format_name == format_:
            return plugin

def find_output_plugin(format_):
    """
    Find the output plugin with name `format_`.
    """
    for plugin in get_output_plugins():
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

def convert(files, iformat, output, oformat, use_header=None):
    """
    Convert all the files in `files` into the corresponding first order structures and write them to
    the output.

    :param list[string] files: A list of file names that need to be converted.
    :param output: The stream to write the output to.
    :param bool use_header: Whether or not to write a header for each file.
    """
    if len(files) > 1 and use_header is None:
        use_header = True
    writer = oformat(stream=output)
    for file_ in files:
        model = read_file(iformat, file_)
        if use_header:
            output.write('# {}\n'.format(file_))
        writer.write_model(model)

def main():
    """
    The main entrypoint for the script.
    """
    parser = ArgumentParser(description="""
    A utility for translating Tarski's World files into their corresponding first order structures.
    """)
    parser.add_argument("files", help="The Tarski's World file to convert.", nargs='*')
    parser.add_argument("--version", action="version",
                        version="tarski.py {}".format(tarski.__VERSION__))
    parser.add_argument("--list-input-formats", action="store_true",
                        help="Give a list of the accepted input formats and exit")
    parser.add_argument("--list-output-formats", action="store_true",
                        help="Give a list of the accepted output formats and exit")
    parser.add_argument("-f", "--from", default='tarski', dest="from_",
                        help="The format of the input file, defaults to tarski")
    parser.add_argument("-t", "--to", default='plain',
                        help="The output format, defaults to plain")
    args = parser.parse_args()
    if args.list_input_formats:
        list_input_formats()
        return 0
    if args.list_output_formats:
        list_output_formats()
        return 0
    if not args.files:
        parser.error("the following arguments are required: files")
    in_plugin = find_input_plugin(args.from_)
    if in_plugin is None:
        parser.error("unrecognized input format: {}".format(args.from_))
    out_plugin = find_output_plugin(args.to)
    if out_plugin is None:
        parser.error("unrecognized output format: {}".format(args.to))
    use_header = None
    convert(args.files, in_plugin, sys.stdout, out_plugin, use_header)

if __name__ == '__main__':
    main()
