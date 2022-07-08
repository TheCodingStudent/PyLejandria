# PyLejandria
<img src="https://www.traveldepartment.com/media/23634/career-icons-training-and-development.png"
     alt="HTML image alt text"
     title="Optional image title"
     align="right"
     width="100px"
/>

Javier and I were bored of sending us scripts and functions by whatsapp, so we decided to make a compilation of the *most useful functions*, even create some together. The project is called **PyLejandria** thanks to the library of Alexandria, where it is said that a colossal amount of knowledge resided. The project is not at all serious, but we will try to do the best we can with our current level of programming.

# Modules 
* **GUI**
    * Compilation of widgets that take as a basis the widgets of tkinter, can add functions to make simple interfaces in a very simple way without losing flexibility or having new widgets.

* **MATH**
    * Set of functions and classes that facilitate mathematics in python, we are aware that there are specialized libraries, but the idea of this module is that it is easy and fast access.

* **MODULE**
    * A simple module consisting of an init function to easily generate a new python package. It could in the future be part of a complete tool to maintain packages.

* **TOOLS**
    * set of everyday functions, mostly for debugging, consists of variables, functions and classes that make the interaction of the program with the terminal simpler, but without needing a user interface.

* **UPLOAD**
    * Module with graphical interface for the management of python packages, has tools forEncilla upload the package to GitHub and PyPi, allows you to decide whether to upload to a GitHub repository automatically detecting if the package has one, in addition to not uploading to PyPi in case we only want to update the repository.

# Download
`pip install pylejandria` or copy from [PyPi](https://pypi.org/project/pylejandria/).

# Help

* ## **Script**
    If you need help you can import the package and use the example function, it will open an interface that will show you all the attributes of the module and its description. This are the following examples, in this case we will see the help of the "gui" module

    ```python
    # Import the module
    from pylejandria import gui

    # Run the example if we run the script directly
    if __name__ == '__main__':
        gui.example()
    ```
    
* ## **Terminal**
    Open your favorite terminal and run the following commands
    ```bash
    # Import the module
    from pylejandria import gui

    # Run the example
    gui.example()
    ```

# CREDITS
| **Name**         | **User**         |
| ---------------- | ---------------- |
| Armando Chaparro | TheCodingStudent |

# LICENSE
[PyLejandria](https://github.com/TheCodingStudent/pylejandria) by Armando Chaparro is licensed under a [MIT License](https://mit-license.org/). See LICENSE.md.

Copyright © 2022 [Armando Chaparro](https://github.com/TheCodingStudent)