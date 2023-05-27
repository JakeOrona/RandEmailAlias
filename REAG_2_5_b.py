# v2.5.1-beta
# Feature Update: Load and save alias history as a .csv file

import random
import string
import tkinter as tk
import threading
import datetime
import re
import csv
from tkinter import filedialog, messagebox

class RandomEmailAliasGenerator:
    def __init__(self, master):
        """Initializes the GUI"""
        self.master = master
        self.master.title("R.E.A.G. ʕ º ᴥ ºʔ")

        # create alias history array
        self.alias_history = []

        # Set window size for responsive window
        self.master.rowconfigure((0,1,2), weight=1, minsize=30)
        self.master.columnconfigure((0), weight=1, minsize=30)

        # Create new frame for base input
        base_email_frame = tk.Frame(self.master, relief="groove")
        base_email_frame.grid(row=0, column=0, columnspan=1, padx=5, pady=3)

        # Create new frame for all buttons
        buttons_frame = tk.Frame(self.master, relief="groove")
        buttons_frame.grid(row=1, column=0, columnspan=1, padx=5, pady=3)

        # Create new frame for feeling lucky output
        feeling_lucky_output_frame = tk.Frame(self.master,  relief="groove")
        feeling_lucky_output_frame.grid(row=2, column=0, columnspan=1, padx=2, pady=3)

        # Base email input field in base_email_frame
        self.base_email = tk.Entry(base_email_frame, width=25)
        self.base_email.grid(row=0, column=0, padx=10, pady=5)
        self.base_email.insert(0, "Enter Base Email")
        self.base_email.focus()
        self.base_email.select_range(0, tk.END)  # Select the entire text in the Entry widget

        # Base alias input field
        self.base_alias = tk.Entry(base_email_frame, width=25)
        self.base_alias.grid(row=1, column=0, padx=5, pady=5)
        self.base_alias.insert(0, "Enter Base Alias")

         # Toggle for timestamp alias
        ts_toggle = tk.BooleanVar()
        checkbutton = tk.Checkbutton(base_email_frame, text=f"Timestamp Alias Override", variable=ts_toggle, onvalue=True, offvalue=False)
        checkbutton.grid(row=2, column=0, padx=5, pady=2)

        # Generated email alias label and output field
        tk.Label(buttons_frame, text="Magic Output:").grid(row=4, column=0, padx=5, pady=5)
        self.email_alias = tk.Entry(buttons_frame, width=25)
        self.email_alias.grid(row=5, column=0, padx=5, pady=5)

        # Random email button info
        tk.Label(buttons_frame, text="ie: jake+abc123@gmail.com").grid(row=1, column=0, columnspan=1, padx=5, pady=1)

        # Generate random email button
        self.generate_button = tk.Button(buttons_frame, text="Generate Random Alias", command=self.generate_random_email_alias)
        self.generate_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        # Generate email base alias button
        self.generate_alias_button = tk.Button(buttons_frame, text="Generate Using Base Alias", command=lambda: self.generate_base_alias_email_alias(ts_toggle))
        self.generate_alias_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        
        # Base alias email button info
        tk.Label(buttons_frame, text="ie: jake+TEST.abc123@gmail.com").grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        # Copy to Clipboard button
        self.copy_button = tk.Button(buttons_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Label to display confirmation message
        self.confirmation_label = tk.Label(buttons_frame, text="waiting for input..", fg="White", bg="Green")
        self.confirmation_label.grid(row=7, column=0, padx=5, pady=5)

        # Generate 10 aliases button info
        tk.Label(feeling_lucky_output_frame, text="Generate 10 aliases using base alias").grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        # Generate 10 aliases button
        self.lucky_button = tk.Button(feeling_lucky_output_frame, text="Feeling Lucky", command=self.feeling_lucky)
        self.lucky_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        
        # Feeling lucky output field
        self.feeling_lucky_output = tk.Text(feeling_lucky_output_frame, height=10, width=30)
        self.feeling_lucky_output.grid(row=2, column=0, padx=5, pady=10)

        # Show Alias History button
        self.alias_history_button = tk.Button(self.master, text=">>\n\n\n>>\n\n\n>>", font="bold", command=self.show_alias_history)
        self.alias_history_button.grid(row=1, column=1, padx=5, pady=10)

    def show_alias_history(self):

        # Check if history frame already exists
        if hasattr(self, 'history_frame'):
            self.toggle_history()
        else:
            # Update History Button to toggle the visibility of the history section
            self.alias_history_button.config(text="<<\n\n\n<<\n\n\n<<")

            # Create a Frame for the collapsible history section
            self.history_frame = tk.Frame(self.master, relief="groove")
            self.history_frame.grid(row=0, column=2, rowspan=4, padx=2, pady=3, sticky="nsew")

            # Configure the row and column to fill vertical space
            self.history_frame.grid_rowconfigure(1, weight=1)
            self.history_frame.grid_columnconfigure(0, weight=1)

             # Create new frame for alias history save/load buttons in history frame
            history_function_frame = tk.Frame(self.history_frame, relief="groove")
            history_function_frame.grid(row=0, column=0, columnspan=1, padx=2, pady=3)

            # Create a Text widget to display the history
            self.history_text = tk.Text(self.history_frame, height=15, width=75)
            self.history_text.grid(row=1, column=0, columnspan=1, padx=2, pady=3, sticky="nsew")

            # Save alias history button
            self.save_history_button = tk.Button(history_function_frame, text="Save Alias History", command=self.save_alias_history)
            self.save_history_button.grid(row=0, column=0, padx=5, pady=5)

            # Load alias history button
            self.load_history_button = tk.Button(history_function_frame, text="Load Alias History", command=self.load_alias_history)
            self.load_history_button.grid(row=0, column=1, padx=5, pady=5)

            # Insert the history into the Text widget
            for alias in self.alias_history:
                self.history_text.insert(tk.END, alias + "\n")

    def update_history_display(self):
        if hasattr(self, 'history_text'):  # Check if history_text attribute exists
            self.history_text.delete("1.0", tk.END)
            for alias in self.alias_history:
                self.history_text.insert(tk.END, alias + "\n")

    def toggle_history(self):
        # Toggle the visibility of the history section
        if self.history_frame.winfo_ismapped():
            self.history_frame.grid_forget()
            self.alias_history_button.config(text=">>\n\n\n>>\n\n\n>>")
        else:
            self.history_frame.grid(row=0, column=2, rowspan=3, padx=2, pady=3, sticky="nsew")
            self.alias_history_button.config(text="<<\n\n\n<<\n\n\n<<")

    def save_alias_history(self):
        # Prompt the user for a custom file name
        file_name = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if file_name:
            with open(file_name, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Alias", "Timestamp"])  # Write the header
                for alias in self.alias_history:
                    match = re.search(r"(.*) \| Timestamp: (.*?)( \*|$)", alias)
                    if match:
                        email, ts, fl_flag = match.group(1), match.group(2), match.group(3)
                        fl_flag = "*" if fl_flag.strip() == "*" else ""  # Check if alias ends with "*"
                        writer.writerow([email, ts, fl_flag])
                    else:
                        writer.writerow([alias, "", ""])  # Write empty values if pattern not matched

            self.confirmation_label.config(text="Alias History Saved", fg="White", bg="Green")
            t = threading.Timer(2.0, self.reset_confirmation)
            t.start()

    def load_alias_history(self):
        if messagebox.askyesno("Warning", "Loading a file will overwrite the current alias history. Do you want to proceed?"):
            file_name = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_name:
                self.alias_history.clear()
                with open(file_name, 'r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip the header row

                    self.alias_history = []  # Clear the existing alias history
                    for row in reader:
                        alias = row[0]
                        timestamp = row[1].replace("Timestamp: ", "")
                        fl_flag = row[2] if len(row) > 2 else ""
                        formatted_alias = f"{alias} | Timestamp: {timestamp}{fl_flag}"
                        self.alias_history.append(formatted_alias)

                self.confirmation_label.config(text="Alias History Loaded", fg="White", bg="Green")
                if self.history_text.get("1.0", tk.END) != "\n":
                    self.history_text.delete("1.0", tk.END)
                for alias in self.alias_history:
                    self.history_text.insert(tk.END, alias + "\n")

    def is_valid_base_email(self, email):
        # Regular expression for email validation
        if email != '':
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        else: return False
        
    def is_base_alias_not_null(self, alias):
        # Check if the base alias is not null using regular expression
        if alias != '':
            pattern = r'^[a-zA-Z0-9._%-]*$'
            return bool(re.match(pattern, alias))
        else: return False
    
    def generate_random_email_alias(self, copy_to_clipboard=True):
        """Generates a random email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("%y-%m-%d-%H.%M.%S")
        # check for valid base email
        if self.is_valid_base_email(base_email):
            username, domain = base_email.split('@')
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            self.email_alias.delete(0, tk.END)
            self.email_alias.insert(0, f"{username}+{random_string}@{domain}")

            if copy_to_clipboard:
                self.copy_to_clipboard()
                self.generate_click_confirmation(self.generate_button)
                # Add alias to history
                self.alias_history.append(self.email_alias.get() + " | Timestamp: " + timestamp)

                 # Check if the history window exists before updating the display
                if hasattr(self, 'history_text'):
                    if self.history_text.winfo_exists():  # Check if history_text widget exists and is open
                        self.update_history_display()
                    else:
                        delattr(self, 'history_text')  # Remove the attribute if the history window is closed
        else:
            self.email_alias.delete(0, tk.END)
            self.email_alias.insert(0, f"ENTER A VALID BASE EMAIL")
            self.error_confirmation()

    def generate_base_alias_email_alias(self, ts_toggle, copy_to_clipboard=True):
        """Generates a random email alias based on a base email and base alias. 6 chars"""
        base_email = self.base_email.get()
        base_alias = self.base_alias.get()
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("%y-%m-%d-%H.%M.%S")
        # check for base alias not null
        if self.is_base_alias_not_null(base_alias):
            # Check for valid base email
            if self.is_valid_base_email(base_email):
                username, domain = base_email.split('@')

                if ts_toggle.get():
                    random_string = ''.join(timestamp)
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_string}@{domain}")
                else:
                    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_string}@{domain}")

                if copy_to_clipboard:
                    self.copy_to_clipboard()
                    self.generate_click_confirmation(self.generate_alias_button)
                    self.alias_history.append(self.email_alias.get() + " | Timestamp: " + timestamp)
                    # Update History Display
                    self.update_history_display()
            else:
                # Display error message
                self.email_alias.delete(0, tk.END)
                self.email_alias.insert(0, f"ENTER A VALID BASE EMAIL")
                self.error_confirmation()
        else:
            # Display error message
            self.email_alias.delete(0, tk.END)
            self.email_alias.insert(0, f"ENTER A VALID BASE ALIAS")
            self.error_confirmation()

    def feeling_lucky(self):
        """Generates 10 random email aliases at once using base_alias"""
        base_email = self.base_email.get()
        base_alias = self.base_alias.get()
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("%y-%m-%d-%H.%M.%S")
        # check for base alias not null
        if self.is_base_alias_not_null(base_alias):
            # Check for valid base email
            if self.is_valid_base_email(base_email):
                username, domain = base_email.split('@')
                random_aliases = [f"{username}+{base_alias}.{''.join(random.choices(string.ascii_letters + string.digits, k=6))}@{domain}" for i in range(10)]
                self.feeling_lucky_output.delete('1.0', tk.END)
                self.feeling_lucky_output.insert('1.0', '\n'.join(random_aliases))
                # Click confirmation prompt
                self.generate_click_confirmation(self.lucky_button)
                index='1.0'
                for alias in random_aliases:
                    self.alias_history.append(alias + " | Timestamp: " + timestamp + "*")
                    index = self.feeling_lucky_output.index(f"{index}+1c")  # Increment index to the next line
                # Update History Display after appending lucky output
                self.update_history_display()
            else:
                # Display error message
                self.feeling_lucky_output.delete('1.0', tk.END)
                self.feeling_lucky_output.insert('1.0', f"ENTER A VALID BASE EMAIL")
                self.error_confirmation()
        else:
            # Display error message
            self.feeling_lucky_output.delete('1.0', tk.END)
            self.feeling_lucky_output.insert('1.0', f"ENTER A VALID BASE ALIAS")
            self.error_confirmation()

    def copy_to_clipboard(self):
        """Copies the generated email alias to the clipboard"""
        if self.is_valid_base_email(self.email_alias.get()):
            self.email_alias.clipboard_clear()  # Clear the clipboard
            self.email_alias.clipboard_append(self.email_alias.get())  # Append the email alias to the clipboard
            self.email_alias.update()  # Update the clipboard
            self.confirmation_label.config(text="EMAIL COPIED", fg="White", bg="Green")
            # Reset label text after 2 seconds
            t = threading.Timer(2.0, self.reset_confirmation)
            t.start()

    def generate_click_confirmation(self, button):
        """When button clicked display confirmation"""
        button.config(text="ʕ º ᴥ ºʔ", fg="White", bg="Blue")
        # Reset label text after 0.1 second
        self.master.after(100, self.reset_button, button)

    def error_confirmation(self):
        """When invalid base email or null base alias display error"""
        self.confirmation_label.config(text="(ノಠ益ಠ)ノ彡┻━┻", fg="White", bg="Red")
        t = threading.Timer(1.0, self.reset_confirmation)
        t.start()

    def reset_button(self, button):
        """Reset generate email button text"""
        if button == self.generate_button:
            button.config(text="Generate Random Alias", fg= "Black", bg= "White")
        elif button == self.generate_alias_button:
            button.config(text="Generate Using Base Alias", fg= "Black", bg= "White")
        elif button == self.lucky_button:
            button.config(text="Feeling Lucky", fg= "Black", bg= "White")
        elif button == self.copy_button:
            button.config(text="Copy to Clipboard", fg= "Black", bg= "White")
        else:
            return
        
    def reset_confirmation(self):
        """Reset confirmation label text"""
        self.confirmation_label.config(text="waiting for input..")

def main():
    root = tk.Tk()
    app = RandomEmailAliasGenerator(root)
    root.mainloop()


if __name__ == '__main__':
    main()
