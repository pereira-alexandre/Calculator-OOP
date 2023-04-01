"""
Creatin executable:
pyinstaller --onefile -w <fileName>
"""

import tkinter as tk


WHITE = '#FFFFFF'
DEFAULT_FONT_STYLE = ('Arial', 20)
OFF_WHITE = '#F8FAFF'
LIGH_BLUE = '#CCEDFF'
LARGE_FONT_STYLE = ('Arial', 40, 'bold')
SMALL_FONT_STYLE = ('Arial', 16)
DIGITS_FONT_STYLE = ('Arial', 24, 'bold')
LIGHT_GRAY = '#F5F5F5'
LABEL_COLOR = '#2526E5'


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('375x667')
        self.window.resizable(0,0)
        self.window.title('Calculator')
        self.total_expression = ''
        self.current_expression = ''
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.digits = {
            7: (1, 1), 
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2), 
            '.': (4, 1)
                }
        self.operations = {                                         # Maps the Arithmetic Operation in python to the operator sumbols
                                                                    # Ex: the unicode value "\u00F7" represents the "/" symbol
            "/": "\u00F7", 
            "*": "x", 
            "-": "-", 
            "+": "+"
                    }
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)                # Ajust the wight of each row
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()                                 # Adding the digit Buttons
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()                                            # Biding de keyboard to the program



    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate()) # Pressing the enter key is the same as pressing equals button

        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit)) # Pressing Digits buttons

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))



    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_sqrt_button()
        self.create_square_button()


    def create_display_labels(self):                                # Adding the Display Labels
        total_label = tk.Label(
            self.display_frame, text=self.total_expression, 
            anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, 
            padx=24, font=SMALL_FONT_STYLE)                         # "anchor=tk.E" East
        total_label.pack(expand=True, fill='both')

        label = tk.Label(
            self.display_frame, text=self.current_expression, 
            anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, 
            padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label


    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill='both')
        return frame


    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()


    def create_digit_buttons(self):
        for digit, grid_values in self.digits.items():
            button = tk.Button(
                self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, 
                font=DIGITS_FONT_STYLE, borderwidth=0, 
                command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_values[0], column=grid_values[1], sticky=tk.NSEW)


    def append_operator(self, operetor):
        self.current_expression += operetor
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()


    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(
                self.buttons_frame, text=symbol, bg=OFF_WHITE, 
                fg=LABEL_COLOR, borderwidth=0,
                command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1


    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()


    def create_clear_button(self):
        button = tk.Button(
            self.buttons_frame, text="C", bg=WHITE, fg=LABEL_COLOR, 
            font=DIGITS_FONT_STYLE, borderwidth=0, 
            command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)


    def square(self):
        self.current_expression = str(eval(f'{self.current_expression}**2'))
        self.update_label()


    def create_square_button(self):
        button = tk.Button(
            self.buttons_frame, text="x\u00b2", bg=WHITE, fg=LABEL_COLOR, 
            font=DIGITS_FONT_STYLE, borderwidth=0, 
            command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)


    def sqrt(self):
        self.current_expression = str(eval(f'{self.current_expression}**0.5'))
        self.update_label()


    def create_sqrt_button(self):
        button = tk.Button(
            self.buttons_frame, text="\u221ax", bg=WHITE, fg=LABEL_COLOR, 
            font=DIGITS_FONT_STYLE, borderwidth=0, 
            command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)


    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""

        except Exception as e:
            self.current_expression = "Error"

        finally:
            self.update_label()
                                                                    # eval() evaluates and returns the 
                                                                    # value of a valid Python expressoin
                                                                    # Ex: eval('2*3+3') Returns 9


    def create_equals_button(self):
        button = tk.Button(
            self.buttons_frame, text="=", bg=LIGH_BLUE, fg=LABEL_COLOR, 
            font=DIGITS_FONT_STYLE, borderwidth=0, 
            command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)


    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame


    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)


    def update_label(self):
        self.label.config(text=self.current_expression[:11])


    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    calc = Calculator()
    calc.run()

