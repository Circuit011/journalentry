import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from datetime import datetime

class JournalApp:
    def __init__(self):
        self.user_name = self.get_user_name()
        if self.user_name:
            self.create_main_window()
    
    def get_user_name(self):
        """Prompt for username with persistence"""
        # Check for saved username
        if os.path.exists("user_config.txt"):
            with open("user_config.txt", "r") as f:
                saved_name = f.read().strip()
                if messagebox.askyesno("Welcome Back", f"Continue as {saved_name}?"):
                    return saved_name
        
        # Get new username
        name = simpledialog.askstring("Welcome", "What's your name?")
        if name:
            with open("user_config.txt", "w") as f:
                f.write(name)
            return name
        else:
            messagebox.showerror("Error", "Name is required")
            return None
    
    def create_main_window(self):
        """Main application window"""
        self.root = tk.Tk()
        self.root.title(f"{self.user_name}'s Journal")
        
        # Configure layout
        self.root.columnconfigure(0, weight=1)
        
        # Header
        tk.Label(
            self.root,
            text=f"User: {self.user_name}",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Journal button
        tk.Button(
            self.root,
            text="New Journal Entry",
            command=self.open_journal,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        ).grid(row=1, column=0, pady=20, ipadx=10, ipady=5)
        
        # Window sizing
        self.root.update_idletasks()
        self.root.minsize(400, 200)
        self.root.mainloop()
    
    def open_journal(self):
        """Journal entry window"""
        journal_window = tk.Toplevel(self.root)
        journal_window.title(f"New Entry - {self.user_name}")
        journal_window.geometry("600x400")
        
        # Text area with scrollbar
        text_frame = tk.Frame(journal_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        self.text_area = tk.Text(
            text_frame,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        scrollbar.config(command=self.text_area.yview)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = tk.Frame(journal_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="Save Entry",
            command=self.save_entry,
            bg="#2196F3",
            fg="white"
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=journal_window.destroy,
            bg="#f44336",
            fg="white"
        ).pack(side=tk.RIGHT)
    
    def save_entry(self):
        """Save journal entry to file"""
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty", "Entry not saved - no content!")
            return
        
        # Create journals directory if needed
        os.makedirs("journals", exist_ok=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"journals/{self.user_name}_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(content)
        
        messagebox.showinfo("Saved", f"Entry saved to:\n{filename}")
        self.text_area.delete("1.0", tk.END)  # Clear after saving

# Run the application
if __name__ == "__main__":
    app = JournalApp()