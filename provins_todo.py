"""
CSD-325: Programming with Python
Module 10 – Tkinter GUI To-Do Program

Student: Aaron L. Provins
Assignment: CSD-325 Tkinter Program
Description:
    This program is a GUI To-Do List built with Tkinter based on
    Listing 2.2 "Our Scrolling To-Do" from Tkinter-By-Example.

    Modifications for this assignment:
    - Window title changed to "Provins-ToDo"
    - Added a menu bar with complementary colors
    - File -> Exit menu item closes the program correctly
    - Added File / Edit / Help menus with example commands
      (Open, Save, Cut, Copy, Paste, About)
    - Tasks are deleted with RIGHT-CLICK instead of left-click
    - Label provides instructions on how to add and delete tasks

This file is submitted for the CSD-325 Tkinter Program grade item.
"""

import tkinter as tk
import tkinter.messagebox as msg


class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        # Store tasks
        if not tasks:
            self.tasks = []
        else:
            self.tasks = tasks

        # Canvas and frames for scrolling
        self.tasks_canvas = tk.Canvas(self)
        self.tasks_frame = tk.Frame(self.tasks_canvas)
        self.text_frame = tk.Frame(self)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(
            self.tasks_canvas,
            orient="vertical",
            command=self.tasks_canvas.yview
        )
        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Window title and size
        self.title("Provins-ToDo")
        self.geometry("320x420")

        # ===== MENU BAR WITH COMPLEMENTARY COLORS =====
        menu_bg = "#004488"      # dark blue
        menu_fg = "#ffd166"      # yellow

        menubar = tk.Menu(
            self,
            bg=menu_bg,
            fg=menu_fg,
            activebackground=menu_fg,
            activeforeground=menu_bg
        )

        # ----- File menu -----
        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_bg,
            fg=menu_fg,
            activebackground=menu_fg,
            activeforeground=menu_bg
        )
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)
        menubar.add_cascade(label="File", menu=file_menu)

        # ----- Edit menu -----
        edit_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_bg,
            fg=menu_fg,
            activebackground=menu_fg,
            activeforeground=menu_bg
        )
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # ----- Help menu -----
        help_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=menu_bg,
            fg=menu_fg,
            activebackground=menu_fg,
            activeforeground=menu_bg
        )
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Attach menu bar to window
        self.config(menu=menubar)
        # ===== END MENU BAR =====

        # Text box for creating tasks
        self.task_create = tk.Text(self.text_frame, height=3, bg="white", fg="black")

        # Pack canvas and scrollbar
        self.tasks_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Window inside canvas to hold tasks
        self.canvas_frame = self.tasks_canvas.create_window(
            (0, 0),
            window=self.tasks_frame,
            anchor="n"
        )

        self.task_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.task_create.focus_set()

        # Instruction label (add + delete)
        todo1 = tk.Label(
            self.tasks_frame,
            text="Type a task below and press Enter to add it.\nRight-click a task to delete it.",
            bg="lightgrey",
            fg="black",
            pady=10
        )

        # Right-click to delete
        todo1.bind("<Button-3>", self.remove_task)

        self.tasks.append(todo1)

        for task in self.tasks:
            task.pack(side=tk.TOP, fill=tk.X)

        # Bindings
        self.bind("<Return>", self.add_task)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)   # Linux scroll up
        self.bind_all("<Button-5>", self.mouse_scroll)   # Linux scroll down
        self.tasks_canvas.bind("<Configure>", self.task_width)

        # Alternating color schemes for tasks
        self.colour_schemes = [
            {"bg": "lightgrey", "fg": "black"},
            {"bg": "lavender", "fg": "black"},
        ]

    # ===== Menu command methods =====
    def open_file(self):
        print("File > Open command clicked")
        msg.showinfo("Open", "File > Open command clicked (demo only).")

    def save_file(self):
        print("File > Save command clicked")
        msg.showinfo("Save", "File > Save command clicked (demo only).")

    def cut_text(self):
        print("Edit > Cut command clicked")
        msg.showinfo("Cut", "Edit > Cut command clicked (demo only).")

    def copy_text(self):
        print("Edit > Copy command clicked")
        msg.showinfo("Copy", "Edit > Copy command clicked (demo only).")

    def paste_text(self):
        print("Edit > Paste command clicked")
        msg.showinfo("Paste", "Edit > Paste command clicked (demo only).")

    def show_about(self):
        print("Help > About command clicked")
        msg.showinfo("About", "Provins-ToDo GUI\nCSD-325 Module 10 Assignment")

    def exit_program(self):
        self.destroy()

    # ===== To-Do list behavior =====
    def add_task(self, event=None):
        """Add a new task from the text box."""
        task_text = self.task_create.get(1.0, tk.END).strip()

        if len(task_text) > 0:
            new_task = tk.Label(self.tasks_frame, text=task_text, pady=10)
            self.set_task_colour(len(self.tasks), new_task)
            new_task.bind("<Button-3>", self.remove_task)
            new_task.pack(side=tk.TOP, fill=tk.X)
            self.tasks.append(new_task)

        self.task_create.delete(1.0, tk.END)

    def remove_task(self, event):
        """Delete a task after confirming with the user."""
        task = event.widget
        if msg.askyesno("Really Delete?", "Delete '" + task.cget("text") + "'?"):
            self.tasks.remove(event.widget)
            event.widget.destroy()
            self.recolour_tasks()

    def recolour_tasks(self):
        """Re-apply alternating colors after a deletion."""
        for index, task in enumerate(self.tasks):
            self.set_task_colour(index, task)

    def set_task_colour(self, position, task):
        """Set color for a task based on its position in the list."""
        _, task_style_choice = divmod(position, 2)
        my_scheme_choice = self.colour_schemes[task_style_choice]
        task.configure(bg=my_scheme_choice["bg"])
        task.configure(fg=my_scheme_choice["fg"])

    def on_frame_configure(self, event=None):
        """Update scroll region when the window size changes."""
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))

    def task_width(self, event):
        """Keep task labels the full width of the canvas."""
        canvas_width = event.width
        self.tasks_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        """Scroll with the mouse wheel (Windows/macOS + Linux)."""
        if event.delta:
            self.tasks_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            self.tasks_canvas.yview_scroll(move, "units")


if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()
