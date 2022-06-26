"""
this is not suposed to be a function of the module, but it makes simpler
the task of uploading the project to GitHub and PyPi. Anyway it will be
documented for practicing. Feel free to change it.

params:
--version   it overrides the next version of the module, by default the version
            x.x.x would be incremented to x.x.x+1, but it can be changed.
--github    this argument is to disable the GitHub updating, it can be because
            you already updated the repository but not uploaded to PyPi.
--pypi      same as --github but with PyPi.
--commit    the default commit message is "version x.x.x" but can happen that
            you want a different name so use --commit "your message".
"""

import re, os, argparse

with open('setup.cfg', 'r') as f:                               # we open the setup.cfg file to read it
    text = f.read()                                             # we get the text
    old_version = [                                             # this list comprehension finds the current version
        line.replace('version = ', '')                          # we replace the beggining of the version
        for line in text.split('\n')                            # for each line in the text
        if line.startswith('version = ')                        # if the line starts with "version"
    ]
    digits = old_version[0].split('.')                          # we get the digits of the version by splitting between "."
    version = f'{".".join(digits[:-1])}.{int(digits[-1])+1}'    # we join the 2 first digits with ".", increment the last by 1 and added too

parser = argparse.ArgumentParser()                                                          # the parser takes the optional arguments from terminal
parser.add_argument('--version', type=str, required=False, default=version)                 # we add version argument and others
parser.add_argument('--github', type=str, required=False, default='')                       
parser.add_argument('--pypi', type=str, required=False, default='')
parser.add_argument('--commit', type=str, required=False, default=f'version {version}')
args = parser.parse_args()                                                                  # we get the values

version_pattern = '^[0-9]+\.[0-9]+\.[0-9]+$'            # this is a regular expression, is used to validate the version in format x.x.x
if not re.match(version_pattern, args.version):         # if the version doesnt match our expression
    raise Exception(f"Invalid version {args.version}")  # then we raise an error

abort = input(f'upload v{args.version}?\n{args.commit} (Enter to upload) ') # we ask the user if its sure about upload
if abort:                                                                   # if we dont press enter then we abort
    print('aborted')                                                        # we print a message
    exit()                                                                  # and stop everything by exiting python

if not args.github.lower().startswith('f'):         # if the argument --github is not "false"
    os.system('git add .')                          # we run "git add ." to add the files to stage
    os.system(f'git commit -m "{args.commit}"')     # then we make a commit to save the changes and add our message
    os.system('git push')                           # we send to GitHub
    print(f'{10*"-"}uploaded to GitHub{10*"-"}')    # print message for the user

if not args.pypi.lower().startswith('f'):               # if the argument --pypi is not "false"
    with open('setup.cfg', 'w') as f:                   
        f.write(text.replace(old_version[0], version))  # we open the file setup.cfg to overwrite the version 

    os.system('python -m build')                        # we build the version
    os.system('twine upload dist/*')                    # upload with Twine to PyPi
    print(f'{10*"-"}uploaded to Pypi{10*"-"}')          # print message for the user