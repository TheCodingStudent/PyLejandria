"""
This is a simple tool to upload the Pylejandria package to Pypi and GitHub with
a UI. Version 1.0.3 By Armando Chaparro.
"""

import os
import re
import threading
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import ttk


class Uploader:
    def __init__(self) -> None:
        self.regex = '[0-9]+\.[0-9]+\.[0-9]+'
        self.path = os.getcwd()
        self.get_version()
        self.commit = f'version {self.version}'

    def get_version(self) -> None:
        with open(os.path.join(self.path, 'setup.cfg'), 'r') as f:
            self.text = f.read()
            self.old_version = re.search(self.regex, self.text).group()
            match self.old_version.split('.'):
                case(x, y, z):
                    self.version = f'{x}.{y}.{int(z) + 1}'

    def validate_version(self) -> None:
        """
        Checks if the current version is valid, it must follow the pattern:
        x.x.x, if it doesnt then is deleted to prevent any error. 
        """
        text = self.version_entry.get()
        if re.match(f'^{self.regex}$', text):
            self.version_status['fg'] = '#00ff00'
            self.version_status['text'] = 'Valid version'
        else:
            self.version_status['fg'] = '#ff0000'
            self.version_status['text'] = 'Invalid version'
            self.version_entry.delete(0, tk.END)

    def upload(self) -> None:
        """
        Based on the PYPI and GITHUB variables, uploads to their respective sites
        using the same commands that are used in terminal.
        """
        if self.pypi is True:
            with open(os.path.join(self.path, 'setup.cfg'), 'w') as f:
                f.write(self.text.replace(self.old_version, self.version))

            os.system('python -m build')
            file1 = os.path.join(
                self.path, f'dist/pylejandria-{self.version}-py3-none-any.whl'
            )
            file2 = os.path.join(self.path, f'dist/pylejandria-{self.version}.tar.gz')
            os.system(f'twine upload {file1} {file2}')
            print(f'{10*"-"}uploaded to Pypi{10*"-"}')

        if self.github is True:
            os.system('git add .')
            os.system(f'git commit -m "{self.commit}"')
            os.system('git push')
            print(f'{10*"-"}uploaded to GitHub{10*"-"}')

    def get_values(self) -> None:
        """
        Updates all global variables and starts a new thread to run the uploading,
        the thread is necessary to run in parallel with the UI.
        """
        self.commit = self.commit_entry.get()
        self.version = self.version_entry.get()
        self.github = self.git_combobox.current() == 0
        self.pypi = self.pypi_combobox.current() == 0
        thread = threading.Thread(target=self.upload)
        thread.start()

    def change_path(self) -> None:
        """
        Updates the path to upload from.
        """
        tk.Tk().withdraw()
        self.path = askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.path)

    def update_git(self, event: tk.Event) -> None:
        """
        Updates all the widgets related to git configuration.
        """
        if self.git_combobox.current():
            self.commit_entry['state'] = 'disabled'
        else:
            self.commit_entry['state'] = 'normal'

    def update_pypi(self, event: tk.Event) -> None:
        """
        Updates all the widgets related to Pypi configuration.
        """
        if self.pypi_combobox.current():
            self.version_entry['state'] = 'disabled'
            self.commit_entry.delete(0, tk.END)
            self.commit_entry.insert(0, '')
        else:
            self.version_entry['state'] = 'normal'
            self.commit_entry.delete(0, tk.END)
            self.commit_entry.insert(0, self.commit)

    def run(self) -> None:
        root = tk.Tk()
        root.title('Uploader By Armando Chaparro')

        path_label = tk.Label(root, text='Folder')
        path_label.grid(row=0, column=0, padx=5, sticky='w')
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.insert(0, self.path)
        self.path_entry.grid(row=0, column=1, padx=5, sticky='w')
        path_button = tk.Button(root, text='Change', command=self.change_path)
        path_button.grid(row=0, column=2, padx=5, sticky='w')

        version_label = tk.Label(root, text='Version')
        version_label.grid(row=1, column=0, padx=5, sticky='w')
        self.version_entry = tk.Entry(root, width=15)
        self.version_entry.insert(0, self.version)
        self.version_entry.grid(row=1, column=1, padx=5, sticky='w')
        version_button = tk.Button(root, text='Validate', command=self.validate_version)
        version_button.grid(row=1, column=2, padx=5)
        self.version_status = tk.Label(root, text='')
        self.version_status.grid(row=1, column=3, padx=5)

        git_label = tk.Label(root, text='Upload to GIT')
        git_label.grid(row=2, column=0, padx=5, sticky='w')
        self.git_combobox = ttk.Combobox(root, width=15)
        self.git_combobox['values'] = ['True', 'False']
        self.git_combobox['state'] = 'readonly'
        self.git_combobox.bind("<<ComboboxSelected>>", self.update_git)
        self.git_combobox.current(0)
        self.git_combobox.grid(row=2, column=1, padx=5, sticky='w')

        commit_label = tk.Label(root, text='Commit')
        commit_label.grid(row=3, column=0, padx=5, sticky='w')
        self.commit_entry = tk.Entry(root, width=30)
        self.commit_entry.insert(0, self.commit)
        self.commit_entry.grid(row=3, column=1, padx=5, sticky='w')

        pypi_label = tk.Label(root, text='Upload to Pypi')
        pypi_label.grid(row=4, column=0, padx=5, sticky='w')
        self.pypi_combobox = ttk.Combobox(root, width=15)
        self.pypi_combobox.bind("<<ComboboxSelected>>", self.update_pypi)
        self.pypi_combobox['values'] = ['True', 'False']
        self.pypi_combobox['state'] = 'readonly'
        self.pypi_combobox.current(0)
        self.pypi_combobox.grid(row=4, column=1, padx=5, sticky='w')

        upload_button = tk.Button(root, text='Upload', command=self.get_values)
        upload_button.grid(row=5, column=1, padx=5, pady=10, sticky='ew')

        root.mainloop()

if __name__ == '__main__':
    app = Uploader()
    app.run()
