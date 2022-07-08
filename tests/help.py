from pylejandria.gui import Hierarchy
import tkinter as tk

root = tk.Tk()

info = {
    'Mate': [
        {'Aritmetica': 'Numeros'},
        {
            'Algebra': [
                'Variables',
                {
                    'Monomios': 'Un solo termino',
                    'Polinomio': [
                        'Conjunto de monomios',
                        {'Grado': 'Valor del exponente mas alto'}
                    ]
                }
            ],
            'Calculo': [
                {
                    'infinitesimal': [
                        'utiliza el concepto de limite',
                        {
                            'diferencial': 'Derivadas',
                            'integral': 'integrales'
                        }
                    ]
                },
                {'Vectorial': 'utiliza el concepto de vectores'}
            ]
        }
    ],
    'Filosofia': 'aburre'
}

hierarchy = Hierarchy(root, info, 'Conocimiento')
hierarchy.pack(expand=True, fill='both')

root.mainloop()
