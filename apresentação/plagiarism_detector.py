import os


try:
    from thefuzz import fuzz
except:
    os.system('pip install thefuzz')
    from thefuzz import fuzz

try:
    import tkinter as tk
except:
    os.system('pip install tkinter')
    import tkinter as tk

try:
    import customtkinter as ctk
except:
    os.system('pip install customtkinter')
    import customtkinter as ctk


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return ('break')


def lev_iterativo(a, b):
    d = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + cost
            )
    return d[len(a)][len(b)]


class PopUp:
    def __init__(self, parent, title, msgs: list, callback):
        self.callback = callback
        top = self.top = ctk.CTkToplevel(parent)
        top.attributes('-topmost', 'true')
        top.title('')
        width, height = 200, 200
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/1.5))
        top.geometry(f'{width}x{height}+{x}+{y}')
        top.resizable(False, False)
        self.info = ctk.CTkLabel(
            top, 
            text=title,
            font=('Roboto', 25)
        )
        self.info.pack()
        y_space = 50
        plagium = False
        for msg in msgs:
            label = ctk.CTkLabel(
                top, 
                text=msg,
                font=('Roboto', 15),
                anchor=ctk.S
            )
            label.place(relx=0, anchor='w') # move the text to the left side of frame
            if msg == 'It\'s a plagium':
                plagium = True
                label.place(x=60, y=y_space)
            else:    
                label.place(x=10, y=y_space)
            y_space += 30
        self.ok_btn = ctk.CTkButton(
            top, 
            text='Ok', 
            command=self.close
        )
        self.ok_btn.place(relx=0, anchor='w')
        self.ok_btn.place(x=30, y=y_space + 10 if plagium else y_space)

    def close(self):
        self.top.destroy()
        self.callback()


def show_results(parent, text1, text2, callback):
    text1, text2 = text1.strip(), text2.strip()
    if len(text1) == 0 or len(text2) == 0:
        return
    lev_dist = lev_iterativo(text1, text2)
    sort_ratio = fuzz.partial_token_sort_ratio(text1.strip(), text2)
    set_ratio = fuzz.partial_token_set_ratio(text1, text2)
    msg1 = f'Levenshtein Distance: {lev_dist}'
    msg2 = f'Partial token sort ratio: {sort_ratio}'
    msg3 = f'Partial token set ratio: {set_ratio}'
    PopUp(
        parent,
        'Analysis Result',
        [
            msg1,
            msg2,
            msg3,
            'It\'s a plagium' if sort_ratio >= 60 or set_ratio >= 60 else ''
        ],
        callback
    )


class TextInputFrame(ctk.CTkFrame):
    def __init__(self, *args, header_name='TextInputFrame', placeholder_text='placeholder text', **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.placeholder_text = placeholder_text
        self.header = ctk.CTkLabel(self, text=self.header_name)
        self.header.pack()
        self.text_input = ctk.CTkTextbox(self)
        self.text_input.bind('<Tab>', focus_next_widget)
        self.text_input.pack(fill='both', expand=True, padx=20, pady=20)

    def get_value(self):
        return self.text_input.get('1.0', tk.END)

    def clean_value(self):
        self.text_input.delete('1.0', tk.END)

    def focus_input(self):
        self.text_input.focus_set()


class VerticalScrolledFrame(ctk.CTkFrame):
    def __init__(self, parent, *args, **kw):
        ctk.CTkFrame.__init__(self, parent, *args, **kw)
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        self.interior = interior = ctk.CTkFrame(
            canvas,
            bg_color='black'
        )
        interior_id = canvas.create_window(
            0, 
            0, 
            window=interior,
            anchor=ctk.NW
        )
        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{w}x{h}+0+0')
        self.title('Plagiarism Detector')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.board = VerticalScrolledFrame(
            self, 
            width=w, 
            height=h,
            bg_color='black'
        )
        self.board.pack(fill='both', expand=True, padx=10, pady=10)
        self.frame_1 = TextInputFrame(self.board.interior, header_name='Text 1')
        self.frame_1.pack(fill='both', expand=True, padx=20, pady=20)
        self.frame_2 = TextInputFrame(self.board.interior, header_name='Text 2')
        self.frame_2.pack(fill='both', expand=True, padx=20, pady=20)
        self.button = ctk.CTkButton(
            self.board.interior,
            text='Analyze',
            width=100,
            height=30,
            command=lambda:
                show_results(
                    self,
                    self.frame_1.get_value(), 
                    self.frame_2.get_value(),
                    lambda: [
                        self.frame_1.clean_value(), 
                        self.frame_2.clean_value(),
                        self.frame_1.focus_input()
                    ]
                )
        )
        self.button.pack(fill='both', expand=True, padx=20, pady=20)


if __name__ == '__main__':
    app = App()
    app.mainloop()