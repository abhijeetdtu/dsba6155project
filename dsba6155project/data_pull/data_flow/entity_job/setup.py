import setuptools

from distutils.command.build import build as _build  # type: ignore

import os
import logging
import subprocess

import setuptools.command.build_py
import distutils.cmd
import distutils.log
import setuptools

class build(_build):  # pylint: disable=invalid-name
  sub_commands = _build.sub_commands + [('CustomCommands', None)]

# CUSTOM_COMMANDS = [
# ["wget" ,"'https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz'"],
# ["tar","-xvzf" ,"en_core_web_md-2.2.5.tar.gz" , "-C" , "/usr/spacy_model" ],
# #['pip', 'install', 'https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz']
# ]

CUSTOM_COMMANDS = [["easy_install" , "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz"]]

class CustomCommands(setuptools.Command):
  """A setuptools Command class able to run arbitrary commands."""
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def RunCustomCommand(self, command_list):
    print('Running command: %s' % command_list)
    p = subprocess.Popen(
        command_list,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    # Can use communicate(input='y\n'.encode()) if the command run requires
    # some confirmation.
    stdout_data, _ = p.communicate()
    print('Command output: %s' % stdout_data)
    if p.returncode != 0:
      raise RuntimeError(
          'Command %s failed: exit code: %s' % (command_list, p.returncode))

  def run(self):
    for command in CUSTOM_COMMANDS:
      self.RunCustomCommand(command)


setuptools.setup(
    name='entity-job',
    version='1.0',
    install_requires=[
        "spacy",
        "spacy-lookups-data",
        "apache-beam",
        "apache_beam[gcp]"
        #"spacy-model @ https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz"
    ],
    # dependency_links=[
    #     "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz"
    # ],
    packages=setuptools.find_packages(),
    cmdclass={
        # Command class instantiated and run during pip install scenarios.
        'build': build,
        'CustomCommands': CustomCommands,
    }
)


#os.system("pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz")
