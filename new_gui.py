from src.pylejandria.gui import Window, PhoneEntry

window = Window('Gui Style')

def validate():
    phone.validate()
    print(phone.get(), phone.is_valid)

phone = PhoneEntry(
    window,
    extensions=True,
    text='Phone Entry',
    regex='^\+[0-9]{1,3}[0-9]{10,20}$',
    button='Validate',
    command=validate
)
phone.pack(side='left', anchor='w', ipadx=10)

window.mainloop()