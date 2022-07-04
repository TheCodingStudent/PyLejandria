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
--folder    if given then the source folder is changed and can upload any
            module, is useful because it allows to no duplicate this file.
"""

import re
import os
import argparse

with open('setup.cfg', 'r') as f:
    text = f.read()
    old_version = [
        line.replace('version = ', '')
        for line in text.split('\n')
        if line.startswith('version = ')
    ]
    digits = old_version[0].split('.')
    version = f'{".".join(digits[:-1])}.{int(digits[-1])+1}'


parser = argparse.ArgumentParser()
parser.add_argument('--version', type=str, required=False, default=version)
parser.add_argument('--github', type=str, required=False, default='')
parser.add_argument('--pypi', type=str, required=False, default='')
parser.add_argument('--folder', type=str, required=False, default=os.getcwd())
parser.add_argument(
    '--commit',
    type=str,
    required=False,
    default=f'version {version}'
)
args = parser.parse_args()

pypi = not args.pypi.lower().startswith('f')
github = not args.github.lower().startswith('f')

version_pattern = '^[0-9]+\.[0-9]+\.[0-9]+$'
if not re.match(version_pattern, args.version):
    raise Exception(f"Invalid version {args.version}")

match(github, pypi):
    case(True, True):
        print(f'commit: {args.commit}')
        abort = input(f'upload v{args.version}? (Enter to upload) ')
    case(True, False):
        print(f'commit: {args.commit}')
        abort = input(f'upload to github? (Enter to upload) ')
    case(False, True):
        abort = input(f'upload v{args.version}? (Enter to upload) ')

if abort:
    print('aborted')
    exit()

if pypi is True:
    with open(f'{args.folder}\\setup.cfg', 'w') as f:
        f.write(text.replace(old_version[0], args.version))

    os.system('python -m build')
    file1 = f'{args.folder}\\dist\\pylejandria-{args.version}-py3-none-any.whl'
    file2 = f'{args.folder}\\dist\\pylejandria-{args.version}.tar.gz'
    os.system(f'twine upload {file1} {file2}')
    print(f'{10*"-"}uploaded to Pypi{10*"-"}')

if github is True:
    os.system('git add .')
    os.system(f'git commit -m "{args.commit}"')
    os.system('git push')
    print(f'{10*"-"}uploaded to GitHub{10*"-"}')
