import tkinter as tk
from tkinter import messagebox
import json


# Define functions for the To-Do application
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do  List Application")

        # Initialize tasks list
        self.tasks = self.load_tasks()

        # GUI Components
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Task Entry
        self.task_input = tk.Entry(self.frame, width=40)
        self.task_input.grid(row=0, column=0, padx=10)

        # Add Task Button
        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1)

        # Task List
        self.tasks_listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.tasks_listbox.pack(pady=10)

        # Buttons for managing tasks
        self.complete_button = tk.Button(root, text="Mark as Complete", command=self.mark_complete)
        self.complete_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(root, text="Remove the Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(root, text="Exit and Save", command=self.exit_and_save)
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        # Populate listbox with tasks
        self.refresh_tasks_listbox()

    def add_task(self):
        task = self.task_input.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.refresh_tasks_listbox()
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning!", "Task description must contain user input")

    def mark_complete(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]["completed"] = True
            self.refresh_tasks_listbox()
        else:
            messagebox.showwarning("Warning!", "Please select a task to mark as complete.")

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.refresh_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def refresh_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            try:
                status = "✓" if task["completed"] else "✗"
                self.tasks_listbox.insert(tk.END, f"{task['task']} [{status}]")
            except KeyError as e:
                print(f"Task at index {i} is missing key: {e}")
                messagebox.showerror("Error", f"Task data is corrupted at index {i}.")


    def exit_and_save(self):
        self.save_tasks()
        self.root.destroy()

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
            # Ensure all tasks have correct structure
                return [
                    {"task": t.get("task", ""), "completed": t.get("completed", False)}
                    for t in tasks
            ]
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return an empty list if the file doesn't exist or is invalid


# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
