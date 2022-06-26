import re, os, argparse

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
parser.add_argument('--commit', type=str, required=False, default=f'version {version}')
args = parser.parse_args() 

version_pattern = '^[0-9]+\.[0-9]+\.[0-9]+$'
if not re.match(version_pattern, args.version):
    raise Exception(f"Invalid version {args.version}")

abort = input(f'upload v{args.version}?\n{args.commit} (Enter to upload) ')
if abort: 
    print('aborted')
    exit()

if not args.github.lower().startswith('f'):
    os.system('git add .')
    os.system(f'git commit -m {str(args.commit)}')
    os.system('git push')
    print(f'{10*"-"}uploaded to GitHub{10*"-"}')

if not args.pypi.lower().startswith('f'):
    with open('setup.cfg', 'w') as f:
        f.write(text.replace(old_version[0], version))

    os.system('python -m build')
    os.system('twine upload dist/*')
    os.system('TheCodingStudent')
    os.system('Chaparropy2003')
    print(f'{10*"-"}uploaded to Pypi{10*"-"}')