#!/usr/bin/python3

""" A GUI application that manages players of a secret gift game

    Copyright riban (brian@riban.co.uk)
    Released under MIT license
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class SecureAssignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Random Assigner 2025")
        
        # Setup Fullscreen
        self.root.update_idletasks()
        self.root.attributes('-fullscreen', True)
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        # Data Management
        self.users = [] 
        self.draw_history = [] 
        self.history_index = -1
        self.assignments = {} 
        self.draw_pool = []
        self.counter = 1
        self.game_started = False

        self.container = tk.Frame(self.root, bg="#2c3e50")
        self.container.pack(expand=True, fill="both")
        
        self.show_main_menu()

    def confirm_exit(self):
        answer = simpledialog.askstring("Exit Confirmation", "Type 'yes' to close the application:", parent=self.root)
        if answer and answer.lower() == "yes":
            self.root.destroy()

    def clear_view(self):
        self.root.unbind("<Return>")
        self.root.unbind("<Control-Return>")
        self.root.unbind("<Escape>")
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_view()
        self.root.bind("<Return>", lambda e: self.show_add_screen())
        self.root.bind("<Escape>", lambda e: "break")

        tk.Label(self.container, text="Gift Exchange System", font=("Arial", 40, "bold"), 
                 fg="white", bg="#2c3e50").pack(pady=60)

        # Prominent Add Player Button
        tk.Button(self.container, text="ADD PLAYER (Enter)", font=("Arial", 32, "bold"), 
                  width=25, height=2, bg="#27ae60", fg="white", activebackground="#2ecc71",
                  command=self.show_add_screen).pack(pady=30)

        if len(self.users) >= 2:
            self.root.bind("<Control-Return>", lambda e: self.draw_new_random_user())
            btn_text = "Continue Game (Ctrl+Enter)" if self.game_started else "Start Game (Ctrl+Enter)"
            # Less prominent Start Game button
            tk.Button(self.container, text=btn_text, font=("Arial", 20), 
                      width=30, bg="#e67e22", fg="white", 
                      command=self.draw_new_random_user).pack(pady=10)

        tk.Button(self.container, text="Exit App", command=self.confirm_exit, 
                  bg="#95a5a6", font=("Arial", 14)).pack(side="bottom", pady=40)

    def show_add_screen(self):
        self.clear_view()
        self.root.bind("<Escape>", lambda e: self.show_main_menu())

        tk.Label(self.container, text="Enter Your Name:", font=("Arial", 30), 
                 fg="white", bg="#2c3e50").pack(pady=100)
        
        entry = tk.Entry(self.container, font=("Arial", 36), justify='center')
        entry.pack(pady=20)
        entry.focus_set()

        def confirm(event=None):
            name = entry.get().strip()
            for n in self.users:
                if name.lower() == n["name"].lower():
                    messagebox.showwarning("Error", f"The name '{name}' has already been added!")
                    return
            if name:
                uid = self.counter
                new_user = {"id": uid, "name": name}
                self.users.append(new_user)
                self.counter += 1
                if self.game_started:
                    self.integrate_new_user(new_user)
                
                self.show_large_split_display(f"Welcome {name}!\nWrite this number on your gift:", str(uid), "#f1c40f")
            else:
                messagebox.showwarning("Error", "Name cannot be empty.")
        
        entry.bind("<Return>", confirm)
        btn_frame = tk.Frame(self.container, bg="#2c3e50")
        btn_frame.pack(pady=40)
        tk.Button(btn_frame, text="Cancel (Esc)", font=("Arial", 20), width=15, 
                  command=self.show_main_menu, bg="#c0392b", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Register (Enter)", font=("Arial", 20), width=15, 
                  command=confirm, bg="#27ae60", fg="white").pack(side="left", padx=10)

    def prepare_assignments(self):
        ids = [u['id'] for u in self.users]
        assigned = ids.copy()
        while any(ids[i] == assigned[i] for i in range(len(ids))):
            random.shuffle(assigned)
        self.assignments = dict(zip(ids, assigned))
        self.draw_pool = self.users.copy()
        random.shuffle(self.draw_pool)
        self.game_started = True

    def integrate_new_user(self, new_user):
        self.draw_pool.append(new_user)
        random.shuffle(self.draw_pool)
        all_ids = [u['id'] for u in self.users]
        assigned = all_ids.copy()
        while any(all_ids[i] == assigned[i] for i in range(len(all_ids))):
            random.shuffle(assigned)
        self.assignments = dict(zip(all_ids, assigned))

    def draw_new_random_user(self):
        if not self.game_started:
            self.prepare_assignments()

        if self.draw_pool:
            user = self.draw_pool.pop()
            assigned_num = self.assignments[user['id']]
            self.draw_history.append((user['name'], assigned_num))
            self.history_index = len(self.draw_history) - 1
            self.show_random_display()
        else:
            if self.draw_history:
                self.show_random_display()
            else:
                messagebox.showinfo("Done", "All registered users have been drawn.")

    def navigate_history(self, delta):
        new_index = self.history_index + delta
        if 0 <= new_index < len(self.draw_history):
            self.history_index = new_index
            self.show_random_display()

    def show_random_display(self):
        self.clear_view()
        has_more_history = self.history_index < len(self.draw_history) - 1
        can_draw_new = len(self.draw_pool) > 0
        
        if has_more_history:
            self.root.bind("<Return>", lambda e: self.navigate_history(1))
            self.root.bind("<Right>", lambda e: self.navigate_history(1))
        elif can_draw_new:
            self.root.bind("<Return>", lambda e: self.draw_new_random_user())
            self.root.bind("<Right>", lambda e: self.draw_new_random_user())
        else:
            self.root.bind("<Return>", lambda e: self.show_main_menu())

        if self.history_index > 0:
            self.root.bind("<Left>", lambda e: self.navigate_history(-1))
        self.root.bind("<Escape>", lambda e: self.show_main_menu())

        name, num = self.draw_history[self.history_index]
        
        info_frame = tk.Frame(self.container, bg="#2c3e50")
        info_frame.pack(expand=True)
        
        # Updated text as requested
        tk.Label(info_frame, text=f"{name}\nOpen gift:", 
                 font=("Arial", 60, "bold"), fg="#2ecc71", bg="#2c3e50").pack()
        
        # MEGA NUMBER
        tk.Label(info_frame, text=str(num), font=("Arial", 250, "bold"), 
                 fg="#2ecc71", bg="#2c3e50").pack()

        nav_frame = tk.Frame(self.container, bg="#2c3e50")
        nav_frame.pack(pady=20)
        tk.Button(nav_frame, text="< Previous (Left)", font=("Arial", 18),
                  state="normal" if self.history_index > 0 else "disabled",
                  command=lambda: self.navigate_history(-1)).pack(side="left", padx=20)
        tk.Button(nav_frame, text="Main Menu (Esc)", font=("Arial", 18), bg="#34495e", 
                  fg="white", command=self.show_main_menu).pack(side="left", padx=20)
        
        next_text = "Next (Enter/Right) >" if has_more_history else "Draw Next (Enter/Right)"
        can_go_forward = has_more_history or can_draw_new
        tk.Button(nav_frame, text=next_text, font=("Arial", 18),
                  state="normal" if can_go_forward else "disabled",
                  command=lambda: self.navigate_history(1) if has_more_history else self.draw_new_random_user()).pack(side="left", padx=20)

    def show_large_split_display(self, top_text, big_number, color):
        self.clear_view()
        self.root.bind("<Return>", lambda e: self.show_main_menu())
        self.root.bind("<Escape>", lambda e: self.show_main_menu())

        display_frame = tk.Frame(self.container, bg="#2c3e50")
        display_frame.pack(expand=True)

        tk.Label(display_frame, text=top_text, font=("Arial", 50, "bold"), 
                 fg=color, bg="#2c3e50", justify="center").pack()
        
        # MEGA NUMBER
        tk.Label(display_frame, text=big_number, font=("Arial", 250, "bold"), 
                 fg=color, bg="#2c3e50").pack()

        tk.Button(self.container, text="Return to Main Menu (Enter)", font=("Arial", 24),
                  command=self.show_main_menu, bg="#34495e", fg="white", 
                  padx=40, pady=20).pack(pady=60)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureAssignerApp(root)
    root.mainloop()
