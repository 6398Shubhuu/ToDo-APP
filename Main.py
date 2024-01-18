from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
from tkinter import messagebox

class ToDoWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("ToDo App")
        self.geometry('600x450')
        self.resizable(False, False)

        self.configure_styles()

        self.create_header()
        self.create_content()

        self.con = connect('todo.db')
        self.cur = self.con.cursor()

        self.fill_tasks_treeview()

        self.is_any_task_selected = False

    def configure_styles(self):
        style = Style()
        style.configure('Header.TFrame', background='blue')
        style.configure('Header.TLabel', background='blue', foreground='white', font=('Arial', 25))
        style.configure('Content.TFrame', background='white')
        style.configure('Content.TLabel', background='white', foreground='blue', font=('Arial', 15))
        style.configure('Add.TButton', foreground='blue', font=('Arial', 15))
        style.configure('Treeview.Heading', foreground='blue', font=('Arial', 15))
        style.configure('Treeview', font=('Arial', 12))
        style.configure('Delete.TButton', foreground='red', font=('Arial', 15))

    def create_header(self):
        header_frame = Frame(self, style='Header.TFrame')
        header_frame.pack(fill=X)

        header_label = Label(header_frame, text="ToDo App", style='Header.TLabel')
        header_label.pack(pady=10)

    def create_content(self):
        content_frame = Frame(self, style='Content.TFrame')
        content_frame.pack(fill=BOTH, expand=TRUE)

        new_task_label = Label(content_frame, text='New Task:', style='Content.TLabel')
        new_task_label.grid(row=0, column=0, padx=5, pady=10)

        self.new_task_entry = Entry(content_frame, font=('Arial', 15), width=30)
        self.new_task_entry.grid(row=0, column=1, pady=10)

        add_button = Button(content_frame, text='Add', style='Add.TButton', command=self.add_button_click)
        add_button.grid(row=0, column=2, padx=5, pady=10)

        self.tasks_treeview = Treeview(content_frame, columns=('title',), show='headings', height=12)
        self.tasks_treeview.grid(row=1, column=0, columnspan=2, pady=10)
        self.tasks_treeview.heading('title', text="Title", anchor=W)
        self.tasks_treeview.column('title', width=440)
        self.tasks_treeview.bind('<<TreeviewSelect>>', self.tasks_treeview_row_selection)

        delete_button = Button(content_frame, text='Delete', style='Delete.TButton', command=self.delete_button_click)
        delete_button.grid(row=1, column=2, padx=5, pady=10, sticky=N)

    def fill_tasks_treeview(self):
        self.tasks_treeview.delete(*self.tasks_treeview.get_children())

        self.cur.execute("SELECT * FROM Task")
        tasks = self.cur.fetchall()

        for task in tasks:
            self.tasks_treeview.insert("", END, values=task)

    def add_button_click(self):
        if self.new_task_entry.get() != "":
            self.cur.execute("SELECT * FROM Task WHERE Title = ?", (self.new_task_entry.get(),))
            if self.cur.fetchone() is None:
                self.cur.execute("INSERT INTO Task(Title) VALUES(?)", (self.new_task_entry.get(),))
                self.con.commit()
                messagebox.showinfo("Success Message", 'Task is added successfully')
                self.fill_tasks_treeview()
            else:
                messagebox.showerror("Error Message", 'Task is already added')
        else:
            messagebox.showerror("Error Message", 'Please enter the Task')

    def tasks_treeview_row_selection(self, event):
        self.is_any_task_selected = True
        self.task = self.tasks_treeview.item(self.tasks_treeview.selection())['values']

    def delete_button_click(self):
        if self.is_any_task_selected:
            if messagebox.askquestion('Confirmation Message', 'Are you sure to delete?') == 'yes':
                self.cur.execute("DELETE FROM Task WHERE Title = ?", (self.task[0],))
                self.con.commit()
                self.fill_tasks_treeview()
                messagebox.showerror("Error Message", 'Task is deleted added')
                self.is_any_task_selected = False
        else:
            messagebox.showerror("Error Message", 'Please select the Task')

tdw = ToDoWindow()
tdw.mainloop()
