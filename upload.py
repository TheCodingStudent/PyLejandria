import sys, re, os

try: version = sys.argv[1]
except IndexError:
    with open('setup.cfg', 'r') as f:
        version = [
            line.replace('version = ', '') 
            for line in f.readlines() 
            if line.startswith('version = ')
        ][0]
        digits = version.split('.')
        version = f'{".".join(digits[:-1])}.{int(digits[-1])+1}'

version_pattern = '^[0-9]+\.[0-9]+\.[0-9]+$'
if not re.match(version_pattern, version):
    raise Exception(f"Invalid version {version}")

abort = input(f'upload v{version}? (Enter to upload) ')
if abort: 
    print('aborted')
    exit()

os.system('git add .')
os.system(f'git commit -m "version {version}"')
os.system('git push')