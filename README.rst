pythonrc
=========
**pythonrc** adds a config parser that works well with the [docopt](http://docopt.org/) command line parser.

1. DO NOT define your own defaults in the document string
2. DO define defaults in a separate dictionary
3. DOES look for a config file ".<myapp>rc" in the current or user directory
4. DOES support YAML and JSON file formats ("JSON is YAML")
5. DO use the same argument names as in docopt
6. DO NOT use boolean arguments (flags) if you need to overwrite default/config `True` values.
7. DO use `--flag=<bool>` where 'bool' = 'yes'/'no' instead of flags
8. DOES convert docopt args to simpler versions by removing '--' and '<>'
9. DO NOT use positional arguments with the the same name as other arguments (ref. 8)
