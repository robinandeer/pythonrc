#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
import rc


def test_build_config_path():
  cwd = os.getcwd()
  home = os.path.expanduser('~')
  custom = '/home/clinical/tmp/'
  name = '.chanjorc'
  cwd_name = os.path.join(cwd, name)
  home_name = os.path.join(home, name)
  custom_name = os.path.join(custom, name)

  # Test standard (local, same folder) case
  assert rc.build_config_path('chanjo') == cwd_name
  # Test the case where we store the config in the user home folder
  assert rc.build_config_path('chanjo', scope='global') == home_name
  # Test case where we provide a custom path
  assert rc.build_config_path('chanjo', dir_path=custom) == custom_name
  # It shouldn't matter if we end the dir path with/without trainling '/'
  assert rc.build_config_path('chanjo', dir_path=custom[:-1]) == custom_name

  # Test that supplying a false 'scope' raises `ValueError`
  with pytest.raises(ValueError):
    rc.build_config_path('chanjo', scope='universal')


def test_convert_docopt_args():
  args = {
    '--speed': "20",
    '<name>': ['Guido', 'Kenneth'],
    'install': True,
    '--splice-sites': 'yes',
    '--force': 'no'
  }

  simple_args = {
    'speed': "20",
    'name': ['Guido', 'Kenneth'],
    'install': True,
    'splice-sites': True,
    'force': False
  }

  # Convert docopt args can be converted correctly
  converted_args = rc.convert_docopt_args(args)

  assert converted_args == simple_args
