from src.pylejandria.gui import Window, FlatButton, PhoneEntry

window = Window('Gui Style')

phone = PhoneEntry(window, text='Phone Entry', regex='^\+[0-9]{1,3}[0-9]{10,20}$')
phone.pack(side='left', anchor='w')

window.mainloop()