from src.pylejandria.gui import load, TextSpan, ask
import sys
import re
import os
from threading import Thread

sys.dont_write_bytecode = True

VALID_REGEX = '[0-9]+\.[0-9]+\.[0-9]+'

def update_path(path_entry, version_entry=None, commit_entry=None):
    global TEXT, OLD_VERSION
    path = ask('directory')
    if not path:
        return
    with open(f'{path}/setup.cfg', 'r') as f:
        TEXT = f.read()
        if match := re.search(VALID_REGEX, TEXT):
            OLD_VERSION = match.group()
            match OLD_VERSION.split('.'):
                case(x, y, z):
                    version = f'{x}.{y}.{int(z) + 1}'
            if version_entry:
                version_entry.delete(0, 'end')
                version_entry.insert(0, version)
    if commit_entry:
        commit_entry.delete(0, 'end')
        commit_entry.insert(0, f'Version {version}')

    path_entry.delete(0, 'end')
    path_entry.insert(0, path)

def validate_version(entry):
    version = entry.get()
    if re.match(f'^{VALID_REGEX}$', version):
        entry['fg'] = '#00ff00'
    else:
        entry['fg'] = '#ff0000'

def reset_entry(entry):
    entry['fg'] = 'black'

def get_values(*args):
    thread = Thread(target=upload, args=args)
    thread.start()

def upload(path_entry, version_entry, commit_entry, pypi_combobox, github_combobox, delete_combobox):
    path = path_entry.get()
    delete = delete_combobox.current() == 0
    github = github_combobox.current() == 0
    pypi = pypi_combobox.current() == 0
    version = version_entry.get()
    commit = commit_entry.get()

    if pypi is True:
        if delete is True:
            for file in os.listdir(f'{path}/dist'):
                os.remove(os.path.join(path, file))

        with open(f'{path}/setup.cfg', 'w') as f:
            f.write(TEXT.replace(OLD_VERSION, version))

        os.system('python -m build')
        file1 = f'{path}/dist/pylejandria-{version}-py3-none-any.whl'
        file2 = f'{path}/dist/pylejandria-{version}.tar.gz'
        os.system(f'twine upload {file1} {file2}')
        print(f'{10*"-"}uploaded to Pypi{10*"-"}')

    if github is True:
        os.system('git add .')
        os.system(f'git commit -m "{commit}"')
        os.system('git push')
        print(f'{10*"-"}uploaded to GitHub{10*"-"}')


style = {
    'option_combobox': {
        'width': 15,
        'values': ['True', 'False'],
        'state': 'readonly',
        '.current': 0
    }
}

TEXT_VALUES = [
    {'text': 'Folder'},
    {'text': 'Version'},
    {'text': 'Upload to GIT'},
    {'text': 'Commit'},
    {'text': 'Upload to PyPi'},
    {'text': 'Delete Previews Dist'}
]

if __name__ == '__main__':    
    window = load('new_uploader.tk', __file__, style_dict=style)
    window.mainloop()