#!/usr/bin/env python
"""
  rc
  -----

  Usage:

  .. code-block:: python

    # Parse the document string and command line arguments
    args = docopt(__doc__, version='Parser 1.0')

    # Add defaults and user configs
    options = pythonrc(args)

"""
import os
import json
import yaml
from path import path

__title__ = 'rc'
__version__ = '0.0.1'
__author__ = 'Robin Andeer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Robin Andeer'
__url__ = 'http://github.com/robinandeer/pythonrc'


class FileExistsExeption(Exception):
  pass


def build_config_path(script_name, scope='local'):
  """
  <public> Build the path to the config file.

  :param str script_name: The name of the script/program, usually `__file__`
  :param bool scope:      Whether the config file is in cwd (or $HOME)
  :param str dir_path:    Pointer to parent dir of the config file,
                          overrides 'scope' (optional)
  """
  # Figure out the default .rc config script_name
  rc_name = '.{}rc'.format(path(script_name).basename().replace('.py', ''))

  if scope == 'local':
    # Save absolute path to the current directory
    dir_path = path.getcwd()
  elif scope == 'global':
    # Assume 'global', meaning the config file is placed in the home dir.
    dir_path = path('~').expanduser()
  else:
    # Check if scope if defined as a directory
    dir_path = path(scope)

    # The path needs to be an existing directory path
    if not dir_path.isdir():
      raise ValueError("'{}' must be either 'local', 'global' or an"
                       "existing directory path.".format(scope))

  return os.path.join(dir_path, rc_name)


def convert_boolean_args(dictionary):
  """
  <public>Converts boolean-like ('yes', 'true') in a `dict` to proper
  `True`/`False` values.

  :param dict dictionary: `dict` with string values
  :returns: Updated dictionary with boolean replacement values
  """
  for key, value in dictionary.iteritems():
    # Also update fake 'boolean' arguments
    if value.lower() in ('yes', 'true'):
      dictionary[key] = True
    elif value.lower() in ('no', 'false'):
      dictionary[key] = False

  return dictionary


def merge_docopt(defaults, docopt_dict):
  """
  <public> Merges two `dict`s; one with docopt style keys and one with simple
  keys. The simple `dict` contains default values that might be
  overridden/discarded. The docopt style key names are maintained.

  :param dict defaults: default values with simple key names
  :param dict docopt_dict: higher priority values with docopt style key names
  :returns: updated/merged `dict`
  """
  for key, value in docopt_dict.iteritems():
    # If the user hasn't submitted a value for a given option
    if value is None:
      if key.startswith('--'):
        # Regular option, remove leading '--'
        simple_key = key[2:]

      elif key.startswith('<'):
        # Positional argument, remove framing '<...>'
        simple_key = key[1:-1]

      if simple_key in defaults:
        # Update (merge) the docopt_dict
        docopt_dict[key] = defaults[simple_key]

  return docopt_dict


def extend_args(args, script, defaults=None, scopes=['global', 'local']):
  """
  <public> Main function that updates the command line args with your
  sensible defaults and potential user configuration options.

  :param dict args: Command line arguments (e.g. from docopt function)
  :param str script: The name of the script (defines .<script>rc)
  :param dict defaults: (optional) Defaults for all/some of the arguments
  :param list scopes: (optional) Which config file(s) to consider: 'local'
                      (per folder), 'global' (`$HOME`), and/or custom path
  """
  # Set up options hash with provided defaults
  if defaults is None:
    defaults = {}

  for scope in scopes:
    # Get path to config file
    rc_path = build_config_path(script, scope=scope)

    # Check if the config file exists
    if rc_path.exists():
      # Open a file stream to the config file
      with rc_path.open('r') as stream:
        # Read in values from the config file
        # YAML is a superset of JSON so we can use the same parser independent
        # of how the config file is written.
        config = yaml.load(stream)

      # Merge defaults and config file options
      defaults.update(config)

  # Convert boolean-like to boolean values
  bool_args = convert_boolean_args(args)

  # Merge combo and command line options
  merged_args = merge_docopt(defaults, bool_args)

  # Serve the final options to the user
  return merged_args


def write_config(contents, out_path, type='json', overwrite=True):
  """
  <public> Writes/Overwrites a config file with (updated) values in one of
  the supported formats: JSON, YAML.

  :param dict contents: `Dict` with all options
  :param str out_path: The path to write to
  :param str type: (optional) Format to write to, options: 'json', 'yaml'
  :param bool overwrite: (optional) Set `False` to raise exception before
                         overwriting an existing file.
  """
  if type == 'json':
    dump = json.dumps(contents, indent=2)
  elif type == 'yaml':
    dump = yaml.dump(contents, allow_unicode=True, default_flow_style=False)
  else:
    raise ValueError("Only type 'json'/'yaml' are supported, not: " + type)

  if overwrite or not out_path.exists():
    # Write/Overwrite file with new contents
    out_path = path(out_path).write_text(dump)
  else:
    # The file already exists and the user has choosen not to overwrite it
    raise FileExistsExeption(out_path + ' already exists.')
