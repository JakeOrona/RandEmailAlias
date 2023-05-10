import random
import string
import tkinter as tk
# from ttkthemes import ThemedTk
import pyperclip
import threading


class RandomEmailAliasGenerator:
    def __init__(self, master):
        """Initializes the GUI"""
        self.master = master
        self.master.title("Random Email Alias Generator - BearBones")


        """# Create new frame for base email input
        base_email_frame = tk.Frame(self.master)
        base_email_frame.grid(row=0, column=0, padx=10, pady=10)"""

        # Base email label and input field
        tk.Label(self.master, text="Base email:").grid(row=0, column=0, padx=10, pady=10)
        self.base_email = tk.Entry(self.master, width=30)
        self.base_email.grid(row=0, column=1, padx=10, pady=10)
        self.base_email.focus()

        # Base alias label and input field
        tk.Label(self.master, text="Base alias: IE: 'oek-123'").grid(row=1, column=0, padx=10, pady=10)
        self.base_alias = tk.Entry(self.master, width=30)
        self.base_alias.grid(row=1, column=1, padx=10, pady=10)

        # Generated email alias label and output field
        tk.Label(self.master, text="Generated email alias:").grid(row=6, column=0, padx=10, pady=10)
        self.email_alias = tk.Entry(self.master, width=50)
        self.email_alias.grid(row=6, column=1, padx=10, pady=10)

        # Generate random email alias button
        self.generate_button = tk.Button(self.master, text="Generate Random Email", command=self.generate_random_email_alias)
        self.generate_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        # Random email button info
        tk.Label(self.master, text="Generate a random email alias with 6 charaters").grid(row=2, column=0, columnspan=1, padx=10, pady=10)

        # Generate test email alias button
        self.generate_test_button = tk.Button(self.master, text="Generate alias Email", command=self.generate_base_alias_email_alias)
        self.generate_test_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
        # Test  email button info
        tk.Label(self.master, text="Generate email alias with base alias and 6 charaters appended. ie: jake+oek-123-abc123@gmail.com",wraplength=300).grid(row=3, column=0, columnspan=1, padx=10, pady=10)

        # Copy to Clipboard button
        self.copy_button = tk.Button(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=6, column=3, columnspan=2, padx=10, pady=10)

        # Generate 10 aliases button
        self.lucky_button = tk.Button(self.master, text="Feeling Lucky", command=self.feeling_lucky)
        self.lucky_button.grid(row=8, column=1, columnspan=1, padx=10, pady=10)
        # Generate 10 aliases button info
        tk.Label(self.master, text="Generate 10 random email aliases at once using base alias").grid(row=8, column=0, columnspan=1, padx=10, pady=10)
        # Feeling lucky output field
        self.feeling_lucky_output = tk.Text(self.master, height=10, width=50)
        self.feeling_lucky_output.grid(row=9, column=1, padx=10, pady=10)

        # Label to display copy confirmation message
        self.copy_label = tk.Label(self.master, text="")
        self.copy_label.grid(row=7, column=1, padx=10, pady=10)

        # Label to display button click confirmation message
        self.click_confirmation_label = tk.Label(self.master, text="")
        self.click_confirmation_label.grid(row=7, column=1, padx=10, pady=10)
    

    def generate_random_email_alias(self):
        """Generates a random email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        username, domain = base_email.split('@')
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.email_alias.delete(0, tk.END)
        self.email_alias.insert(0, f"{username}+{random_string}@{domain}")
        # Click confirmation prompt
        self.click_confirmation()
        # Reset the copy label
        self.copy_label.config(text="")

    def generate_base_alias_email_alias(self):
        """Generates a test email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        username, domain = base_email.split('@')
        base_alias = self.base_alias.get()
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.email_alias.delete(0, tk.END)
        self.email_alias.insert(0, f"{username}+{base_alias}.{random_string}@{domain}")
        # Click confirmation prompt
        self.click_confirmation()
        # Reset the copy label
        self.copy_label.config(text="")
    
    def generate_email_alias(self):
        """Generates a random email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        username, domain = base_email.split('@')
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        self.email_alias.delete(0, tk.END)
        self.email_alias.insert(0, f"{username}+{random_string}@{domain}")
        self.email_alias.select_range(0, tk.END)
        # Click confirmation prompt
        self.click_confirmation()
        # Reset the copy label
        self.copy_label.config(text="")

    def feeling_lucky(self):
        """Generates 10 random email aliases at once using base_alias"""
        base_email = self.base_email.get()
        username, domain = base_email.split('@')
        base_alias = self.base_alias.get()
        random_aliases = [f"{username}+{base_alias}.{''.join(random.choices(string.ascii_letters + string.digits, k=6))}@{domain}" for i in range(10)]
        self.feeling_lucky_output.delete('1.0', tk.END)
        self.feeling_lucky_output.insert('1.0', '\n'.join(random_aliases))
        # Click confirmation prompt
        self.click_confirmation()

    def copy_to_clipboard(self):
        """Copies the generated email alias to the clipboard"""
        pyperclip.copy(self.email_alias.get())
        self.copy_label.config(text="Copied to clipboard!", fg="green")
        # Reset label text after 2 seconds
        t = threading.Timer(2.0, self.reset_copy_confirmation)
        t.start()

    def click_confirmation(self):
        """When button clicked display confirmation"""
        self.click_confirmation_label.config(text="uWu uWu", fg="pink")
        # Reset label text after 2 seconds
        t = threading.Timer(2.0, self.reset_click_confirmation)
        t.start()

    def reset_click_confirmation(self):
        """Reset confirmation label text"""
        self.click_confirmation_label.config(text="")

    def reset_copy_confirmation(self):
        """Reset copy confirmation label text"""
        self.copy_label.config(text="")




def main():
    root = tk.Tk()
    app = RandomEmailAliasGenerator(root)
    root.mainloop()


if __name__ == '__main__':
    main()
