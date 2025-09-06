
import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, messagebox, simpledialog, colorchooser, Toplevel
import json
import os
import webbrowser
from pygments.lexers import PythonLexer
from pygments import lex
from pygments.token import Token



def update_line_numbers(event=None):
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete(1.0, tk.END)
    line_count = int(text_area.index('end-1c').split('.')[0])
    line_numbers.insert(tk.END, '\n'.join(str(i) for i in range(1, line_count + 1)))
    line_numbers.config(state=tk.DISABLED)

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f)

def show_welcome_message():
    welcome_window = Toplevel(window)
    welcome_window.title("Welcome to MaybeCode")
    welcome_window.geometry("400x250")
    
    tk.Label(welcome_window, text="Welcome to MaybeCode by Andreas Agouridis!", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(welcome_window, text="This versatile text editor lets you create and edit text files easily.", wraplength=380, justify="center").pack(pady=5)
    
    tk.Label(welcome_window, text="Features:\n- Create, open, and save text files\n- Change font and background colors\n"
                                  "- Search and replace text\n- Undo and redo actions\n", wraplength=380, justify="center").pack(pady=5)

    def open_link():
        webbrowser.open("https://nextapps.store")

    link_button = tk.Button(welcome_window, text="Visit Next-Apps Website", font=("Arial", 10), fg="blue", cursor="hand2", command=open_link)
    link_button.pack(pady=10)

   


    close_button = tk.Button(welcome_window, text="Close", command=welcome_window.destroy)
    close_button.pack(pady=10)


def apply_syntax_highlighting(event=None):
    text_area.tag_remove("keyword", "1.0", "end")
    text_area.tag_remove("string", "1.0", "end")
    text_area.tag_remove("comment", "1.0", "end")
    text_area.tag_remove("builtin", "1.0", "end")

    data = text_area.get("1.0", tk.END)
    index = "1.0"

    for token, content in lex(data, PythonLexer()):
        end_index = text_area.index(f"{index}+{len(content)}c")
        if token in Token.Keyword:
            text_area.tag_add("keyword", index, end_index)
        elif token in Token.String:
            text_area.tag_add("string", index, end_index)
        elif token in Token.Comment:
            text_area.tag_add("comment", index, end_index)
        elif token in Token.Name.Builtin:
            text_area.tag_add("builtin", index, end_index)
        index = end_index


def login():
    global login_window
    login_window = Toplevel(window)
    login_window.title("Login")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=lambda: perform_login(username_entry.get(), password_entry.get()))
    login_button.pack(pady=10)

def perform_login(username, password):
    if username and username in users:
        if users[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login_window.destroy()
            
            def hide_login_signup():
                user_menu.entryconfig(0, state='disabled')
                user_menu.entryconfig(1, state='disabled')
            show_user_options()
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    else:
        messagebox.showerror("Login Failed", "User not found.")

def signup():
    global signup_window
    signup_window = Toplevel(window)
    signup_window.title("Sign Up")
    signup_window.geometry("300x200")

    tk.Label(signup_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(signup_window)
    username_entry.pack(pady=5)

    tk.Label(signup_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(signup_window, show='*')
    password_entry.pack(pady=5)

    signup_button = tk.Button(signup_window, text="Sign Up", command=lambda: perform_signup(username_entry.get(), password_entry.get()))
    signup_button.pack(pady=10)

def perform_signup(username, password):
    if username and username not in users:
        users[username] = password
        save_users(users)
        messagebox.showinfo("Sign Up Successful", f"User {username} created successfully!")
        signup_window.destroy()
    else:
        messagebox.showerror("Sign Up Failed", "User already exists or invalid username.")


def show_user_options():
    user_menu.entryconfig(0, label="Logout", command=logout)

def logout():
    hide_user_options()
    show_login_signup()

def hide_user_options():
    user_menu.entryconfig(0, label="Login", command=login)
    user_menu.entryconfig(0, state='normal')

def new_file():
    text_area.delete("1.0", tk.END)
    window.title("MaybeCode - New File")
    update_line_numbers()

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt;*.py;*.html;*.java;*.c;*.cpp;*.bas"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())
            apply_syntax_highlighting()
            update_line_numbers()

def save_file_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt;*.py;*.html;*.java;*.c;*.cpp;*.bas"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))

def change_font_size():
    new_size = simpledialog.askinteger("Font Size", "Enter new font size:", minvalue=1, maxvalue=100)
    if new_size:
        text_area.config(font=("Arial", new_size))

def change_font_family():
    new_family = simpledialog.askstring("Font Family", "Enter new font family:")
    if new_family:
        text_area.config(font=(new_family, text_area.cget("font").split()[1]))

def change_bg_color():
    color = colorchooser.askcolor()[1]
    if color:
        text_area.config(bg=color)

def run_code():
    code = text_area.get("1.0", tk.END)
    try:
        exec(code)
    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

window = tk.Tk()
window.title("MaybeCode - Enhanced Editor")
users = load_users()
FONT_SIZES = [8, 10, 12, 14, 16, 18, 20]
FONT_FAMILIES = ["Consolas", "Arial", "Courier New", "Times New Roman"]


menu_bar = Menu(window)
window.config(menu=menu_bar)

frame = tk.Frame(window)
frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

line_numbers = tk.Text(frame, width=4, bg="lightgray", state=tk.DISABLED)
line_numbers.pack(side=tk.LEFT, fill=tk.Y)

text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, undo=True)
text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

text_area.bind("<KeyRelease>", lambda event: [apply_syntax_highlighting(event), update_line_numbers(event)])

menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save As", command=save_file_as)
file_menu.add_separator()
menu_bar.add_cascade(label="File", menu=file_menu)

code_menu = Menu(menu_bar, tearoff=0)
code_menu.add_command(label="Run Code", command=run_code)
menu_bar.add_cascade(label="Code", menu=code_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Copy", command=lambda: window.clipboard_clear() or window.clipboard_append(text_area.get(tk.SEL_FIRST, tk.SEL_LAST)))
edit_menu.add_command(label="Paste", command=lambda: text_area.insert(tk.INSERT, window.clipboard_get()))
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=text_area.edit_undo)
edit_menu.add_command(label="Redo", command=text_area.edit_redo)
menu_bar.add_cascade(label="Edit", menu=edit_menu)


user_menu = Menu(menu_bar, tearoff=0)
user_menu.add_command(label="Login", command=login)
user_menu.add_command(label="Sign Up", command=signup)
menu_bar.add_cascade(label="User", menu=user_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Welcome Message", command=show_welcome_message)
menu_bar.add_cascade(label="Help", menu=help_menu)

settings_menu = Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Change Font Size", command=change_font_size)
settings_menu.add_command(label="Change Font Family", command=change_font_family)
settings_menu.add_command(label="Change Background Color", command=change_bg_color)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

show_welcome_message()
window.config(menu=menu_bar)
users = load_users()

update_line_numbers()
window.mainloop()



