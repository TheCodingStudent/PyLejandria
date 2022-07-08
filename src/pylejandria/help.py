import pkgutil
import importlib
from pylejandria.tools import pretty_dict

class Package:
    def __init__(self, name):
        self.name = name
        self.package = importlib.import_module(f'{name}')
        self.attribs = []
        for attrib in dir(self.package):
            if not attrib.startswith('_'):
                real_attrib = getattr(self.package, attrib)
                if isinstance(real_attrib, str | int | float | complex):
                    self.attribs.append(f'{attrib}: ({type(real_attrib)})\n{real_attrib}\n')
                elif isinstance(real_attrib, dict):
                    self.attribs.append(pretty_dict(real_attrib, _print=False) + '\n')
                elif isinstance(real_attrib, object):
                    doc = real_attrib.__doc__
                    self.attribs.append(f'{attrib}\n{doc if doc else "No info."}\n')
                else:
                    self.attribs.append(f'{attrib} {type(real_attrib)}' + '\n')
    
    def __repr__(self):
        return f'{self.name}\n' + '\n'.join(self.attribs)

packages = []
for _, name, ispkg in pkgutil.iter_modules():
    if ispkg and name != 'asyncio':
        try:
            package = Package(name)
            if name == 'pylejandria': print(package)
            packages.append(package)
        except ModuleNotFoundError:
            print(f'not found {name}')

# print('\n'.join([package.name for package in packages]))