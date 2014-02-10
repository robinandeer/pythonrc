pythonrc
=========
**pythonrc** is a drop-in rc-file parser augmenter for [docopt](http://docopt.org/).

Quick User's Guide
-------------------
These are the nessesary steps to use **pythonrc**:

1. Install the package

.. code-block:: console

  $ pip install rc

2. Import into your project

.. code-block:: python

  from docopt import docopt
  import rc
  import myscript

3. Run docopt to parse the command line arguments

.. code-block:: python
  
  args = docopt(__doc__, version='MyScript {v}'.format(v=myscript.__version__))

4. Set up your script level defaults (lowest priority)

.. code-block:: python

  defaults = {
    'url': 'news.layervault.com',
    'category': 'news',
    'votes': 0
  }

5. Parse potential config-files, both in user home and in the current directory. Missing files are silently skipped.

.. code-block:: python

  # Merge the command line arguments with the defaults and any values
  # found in either global (`$HOME`) or local (this folder) config files.
  options = rc.extend_args(args, __file__, defaults, scopes=['global', 'local'])

That's it. We have now merged the defaults <= user configs <= command line arguments.


Documentation
----------------
For the time being I will refer you to the somewhat complete inline documentation for each function in the package.


Background & Motivation
-------------------------
Config files can unburden the command line and allow users to set user/project specific defaults. A common practice is to name such files `.<script_name>rc`, e.g. '.bashrc', '.bowerrc'. The values in such an rc-file should take precedence over script level defaults but be overwritten by command line arguments.

I needed a very simple script that would parse both global (user), local (project), and custom config files and play nice with the excellent docopt package.


Flaws & Limitations
-------------------------
*docopt*, as great as it is, does come with a few limitations when trying to integrate with a config file parser. My solution has three nagging flaws:

1. Boolean options (flags) become a major issue. There isn't any built in way to flag `False` and [probably won't be](https://github.com/docopt/docopt/issues/51) either. This means you can't override an options that defaults to `True` from a config file. The current solution is to **avoid flags in favor of `--option=<bool>`** where bool is ('yes', 'no', 'true', 'false').

2. *docopt* provides a useful way to set defaults. Problem is that I couldn't find a way to parse those defaults to compare what user supplied and default values. I therefore **require all defaults to be set in a separate `dict`** outside of the docstring.

3. The intuative syntax for `<position argument>`, `--option`, `command` works great *in-script* but would be awkward as a requirement for user authored config files. Q.E.D.: I require that **no two argument/option/command names be the same**.


Checklist
-----------

1. DOES support YAML and JSON file formats ("JSON is YAML")
2. DOES convert docopt args to simpler versions by removing '--' and '<>'
3. DO NOT define your own defaults in the document string
4. DO define defaults in a separate `dict`
5. DO NOT use boolean arguments (flags) you want to overwrite.
6. DO use `--option=<bool>` where 'bool' is 'yes'/'no' in favor of flags
7. DO expect config files to be named ".<myapp>rc"
8. DO NOT use multiple types of arguments with the the same name

License, Authors, Changelog
-----------------------------
Read LICENSE, AUTHORS, CHANGELOG.rst
