"""
This is a simple tool to upload the Pylejandria package to Pypi and GitHub with
a UI
"""

import os
import re
import threading
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import ttk

REGEX = '[0-9]+\.[0-9]+\.[0-9]+'
PATH = os.getcwd()

with open(os.path.join(PATH, 'setup.cfg'), 'r') as f:
    text = f.read()
    old_version = re.search(REGEX, text).group()
    match old_version.split('.'):
        case(x, y, z):
            VERSION = f'{x}.{y}.{int(z) + 1}'


COMMIT = f'version {VERSION}'


def validate_version():
    text = version_entry.get()
    if re.match(f'^{REGEX}$', text):
        version_status['fg'] = '#00ff00'
        version_status['text'] = 'Valid version'
    else:
        version_status['fg'] = '#ff0000'
        version_status['text'] = 'Invalid version'
        version_entry.delete(0, tk.END)


def upload():
    if PYPI is True:
        with open(os.path.join(PATH, 'setup.cfg'), 'w') as f:
            f.write(text.replace(old_version, VERSION))

        os.system('python -m build')
        file1 = os.path.join(
            PATH, f'dist/pylejandria-{VERSION}-py3-none-any.whl'
        )
        file2 = os.path.join(PATH, f'dist/pylejandria-{VERSION}.tar.gz')
        os.system(f'twine upload {file1} {file2}')
        print(f'{10*"-"}uploaded to Pypi{10*"-"}')

    if GITHUB is True:
        os.system('git add .')
        os.system(f'git commit -m "{COMMIT}"')
        os.system('git push')
        print(f'{10*"-"}uploaded to GitHub{10*"-"}')


def get_values():
    global COMMIT, VERSION, GITHUB, PYPI
    COMMIT = commit_entry.get()
    VERSION = version_entry.get()
    GITHUB = git_combobox.current() == 0
    PYPI = pypi_combobox.current() == 0
    thread = threading.Thread(target=upload)
    thread.start()


def change_path():
    global PATH
    tk.Tk().withdraw()
    PATH = askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, PATH)


def update_git(event):
    if git_combobox.current():
        commit_entry['state'] = 'disabled'
    else:
        commit_entry['state'] = 'normal'

def update_pypi(event):
    if pypi_combobox.current():
        version_entry['state'] = 'disabled'
        commit_entry.delete(0, tk.END)
        commit_entry.insert(0, '')
    else:
        version_entry['state'] = 'normal'
        commit_entry.delete(0, tk.END)
        commit_entry.insert(0, COMMIT)

root = tk.Tk()
root.title('Uploader By Armando Chaparro')

path_label = tk.Label(root, text='Folder')
path_label.grid(row=0, column=0, padx=5, sticky='w')
path_entry = tk.Entry(root, width=50)
path_entry.insert(0, PATH)
path_entry.grid(row=0, column=1, padx=5, sticky='w')
path_button = tk.Button(root, text='Change', command=change_path)
path_button.grid(row=0, column=2, padx=5, sticky='w')

version_label = tk.Label(root, text='Version')
version_label.grid(row=1, column=0, padx=5, sticky='w')
version_entry = tk.Entry(root, width=15)
version_entry.insert(0, VERSION)
version_entry.grid(row=1, column=1, padx=5, sticky='w')
version_button = tk.Button(root, text='Validate', command=validate_version)
version_button.grid(row=1, column=2, padx=5)
version_status = tk.Label(root, text='')
version_status.grid(row=1, column=3, padx=5)

git_label = tk.Label(root, text='Upload to GIT')
git_label.grid(row=2, column=0, padx=5, sticky='w')
git_combobox = ttk.Combobox(root, width=15)
git_combobox['values'] = ['True', 'False']
git_combobox['state'] = 'readonly'
git_combobox.bind("<<ComboboxSelected>>", update_git)
git_combobox.current(0)
git_combobox.grid(row=2, column=1, padx=5, sticky='w')

commit_label = tk.Label(root, text='Commit')
commit_label.grid(row=3, column=0, padx=5, sticky='w')
commit_entry = tk.Entry(root, width=30)
commit_entry.insert(0, COMMIT)
commit_entry.grid(row=3, column=1, padx=5, sticky='w')

pypi_label = tk.Label(root, text='Upload to Pypi')
pypi_label.grid(row=4, column=0, padx=5, sticky='w')
pypi_combobox = ttk.Combobox(root, width=15)
pypi_combobox.bind("<<ComboboxSelected>>", update_pypi)
pypi_combobox['values'] = ['True', 'False']
pypi_combobox['state'] = 'readonly'
pypi_combobox.current(0)
pypi_combobox.grid(row=4, column=1, padx=5, sticky='w')

upload_button = tk.Button(root, text='Upload', command=get_values)
upload_button.grid(row=5, column=1, padx=5, pady=10, sticky='ew')

root.mainloop()
