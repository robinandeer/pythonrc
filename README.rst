pythonrc
=========
**pythonrc** adds a config parser that works well with the [docopt](http://docopt.org/) command line parser.

Drop-in augmenter.

User's Guide
--------------
These are the nessesary steps to use **pythonrc**:

1. Install the package

.. code-block:: console

  $ pip install rc

2. Import into your project

```python
from docopt import docopt
import rc
import myscript
```

3. Run docopt to parse the command line arguments

```python
args = docopt(__doc__, version='MyScript {v}'.format(v=myscript.__version__))
```

4. Set up your script level defaults (lowest priority)

.. code-block:: python

  defaults = {
    'url': 'news.layervault.com',
    'category': 'news',
    'votes': 0
  }

5. Parse potential config-files, both in user home and in the current directory (will simply return empty `dict` if files are missing)

.. code-block:: python

  options = rc.extend_args(args, __file__, defaults)

That's it. We have now merged the defaults <= user configs <= command line arguments.


Background & Motivation
-------------------------
Config files can unburden the command line and allow users to set user/project specific defaults. A common practice is to name such files `.<script_name>rc`, e.g. '.bashrc', '.bowerrc'.

The values in such an rc-file should take precedence over script level defaults but be overwritten by command line arguments.

I needed a very simple script that would parse both global (user), local (project), and custom config files and play nice with the excellent docopt package.

Flaws & Limitations
-------------------------
My solution has three flaws:

1. *docopt*, as great as it is, does come with a few limitations when trying to integrate with a config file. Particularly boolean options (flags) become a major issue. There isn't any built in way to flag `False` and [probably won't be](https://github.com/docopt/docopt/issues/51) either.

2. *docopt* provides a useful way to set defaults. Problem is only that I couldn't find a way to grab those defaults to compare what values where user supplied and which values where defaults. I therefore require all defaults to be set in a separate `dict` outside of the docstring.

3. The intuative syntax for `<position argument>`, `--option`, `command` works great *in-script* but would be awkward as a requirement for user authored config files. Q.E.D.: I require that **no two argument/option/command names can be the same**.


Guiding principles
-------------------

1. DO NOT define your own defaults in the document string
2. DO define defaults in a separate dictionary
3. DOES look for a config file ".<myapp>rc" in the current or user directory
4. DOES support YAML and JSON file formats ("JSON is YAML")
5. DO use the same argument names as in docopt
6. DO NOT use boolean arguments (flags) if you need to overwrite default/config `True` values.
7. DO use `--flag=<bool>` where 'bool' = 'yes'/'no' instead of flags
8. DOES convert docopt args to simpler versions by removing '--' and '<>'
9. DO NOT use positional arguments with the the same name as other arguments (ref. 8)
