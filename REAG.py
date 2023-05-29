# v3.1-beta
# Feature Update: 
# Options Frame: alias generation now uses Faker to generate alias with full name or company name using toggle. Dropped random char generation.
# Save default aliases in info window. App will load defaults so user does not need to edit inputs on each startup.

import random
import string
import tkinter as tk
import threading
import datetime
import re
import csv
import os
from faker import Faker
from tkinter import filedialog, messagebox

class RandomEmailAliasGenerator:
    def __init__(self, master):
        """Initializes the GUI"""
        self.master = master
        self.master.title("R.E.A.G. ʕ º ᴥ ºʔ")

        # create alias history array
        self.alias_history = []

        # create default input file path
        self.default_input_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'REAG_default_input.txt')

        # Set window size for responsive window
        self.master.rowconfigure((0,1,2,3), weight=1, minsize=30)
        self.master.columnconfigure((0,1,2), weight=1, minsize=30)

        # Create new frame for base input
        base_email_frame = tk.Frame(self.master, relief="groove")
        base_email_frame.grid(row=0, column=0, columnspan=1, padx=2, pady=3)

        # Create new frame for customize options settings
        options_frame = tk.Frame(self.master,  relief="sunken", borderwidth=1)
        options_frame.grid(row=1, column=0, columnspan=1, rowspan=1, padx=2, pady=3)

        # Create new frame for function buttons
        buttons_frame = tk.Frame(self.master, relief="groove")
        buttons_frame.grid(row=2, column=0, columnspan=1, padx=2, pady=3)

        # Create new frame for feeling lucky
        feeling_lucky_frame = tk.Frame(self.master,  relief="groove")
        feeling_lucky_frame.grid(row=3, column=0, columnspan=1, padx=2, pady=3)

        # Base email input field
        self.base_email = tk.Entry(base_email_frame, width=25)
        self.base_email.grid(row=0, column=0, padx=2, pady=3)
        # self.base_email.insert(0, "Enter Base Email")
        self.base_email.focus()
        self.base_email.select_range(0, tk.END)  # Select the entire text in the Entry widget

        # Base alias input field
        self.base_alias = tk.Entry(base_email_frame, width=25)
        self.base_alias.grid(row=1, column=0, padx=2, pady=3)
        # self.base_alias.insert(0, "Enter Base Alias")

        # Label to display confirmation message
        self.confirmation_label = tk.Label(buttons_frame, text="waiting for input..", fg="White", bg="Green")
        self.confirmation_label.grid(row=7, column=0, padx=2, pady=3)

        # Load default input focus and select all
        self.load_default_input()
        self.base_email.focus()
        self.base_email.select_range(0, tk.END)

        # Label for Options Frame
        self.options_label = tk.Label(options_frame, text="Alias Options:").grid(row=0, column=0, columnspan=1, padx=2, pady=1)

        # Toggle for full name alias
        # self.default_alias_label = tk.Label(options_frame, text="Name Alias (Default)")
        # self.default_alias_label.grid(row=1, column=0, padx=2, pady=2)
        # fn_toggle = tk.BooleanVar()
        # fn_checkbutton = tk.Checkbutton(options_frame, text=f"Name Alias (Default)", variable=fn_toggle, onvalue=True, offvalue=False)
        # fn_checkbutton.grid(row=1, column=0, padx=2, pady=2)

        # Toggle for timestamp alias
        ts_toggle = tk.BooleanVar()
        ts_checkbutton = tk.Checkbutton(options_frame, text=f"Timestamp Alias", variable=ts_toggle, onvalue=True, offvalue=False)
        ts_checkbutton.grid(row=2, column=0, padx=2, pady=2)

        # Toggle for company name alias
        cn_toggle = tk.BooleanVar()
        cn_checkbutton = tk.Checkbutton(options_frame, text=f"Company Alias", variable=cn_toggle, onvalue=True, offvalue=False)
        cn_checkbutton.grid(row=3, column=0, padx=2, pady=2)

        # Generated email alias output field and label
        tk.Label(buttons_frame, text="Magic Output:").grid(row=4, column=0, padx=5, pady=5)
        self.email_alias = tk.Entry(buttons_frame, width=25)
        self.email_alias.grid(row=5, column=0, padx=5, pady=5)

        # Random email button info
        tk.Label(buttons_frame, text="ie: edit+TomJones@this.com").grid(row=1, column=0, columnspan=1, padx=2, pady=1)

        # Generate random email button
        self.generate_button = tk.Button(buttons_frame, text="Generate Random Alias", command=lambda :self.generate_random_email_alias(ts_toggle, cn_toggle))
        self.generate_button.grid(row=0, column=0, columnspan=1, padx=2, pady=3)

        # Generate email base alias button
        self.generate_alias_button = tk.Button(buttons_frame, text="Generate Using Base Alias", command=lambda: self.generate_base_alias_email_alias(ts_toggle, cn_toggle))
        self.generate_alias_button.grid(row=2, column=0, columnspan=1, padx=2, pady=3)
        
        # Base alias email button info
        tk.Label(buttons_frame, text="ie: edit+TEST.TomJones@this.com").grid(row=3, column=0, columnspan=1, padx=2, pady=1)

        # Copy to Clipboard button
        self.copy_button = tk.Button(buttons_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=6, column=0, columnspan=2, padx=2, pady=3)

        # Generate 10 aliases button info
        tk.Label(feeling_lucky_frame, text="Generate 10 aliases using base alias").grid(row=1, column=0, columnspan=1, padx=5, pady=1)

        # Generate 10 aliases button
        self.lucky_button = tk.Button(feeling_lucky_frame, text="Feeling Lucky", command=lambda: self.feeling_lucky(cn_toggle))
        self.lucky_button.grid(row=0, column=0, columnspan=1, padx=5, pady=3)
        
        # Feeling lucky output field
        # self.feeling_lucky_output = tk.Text(feeling_lucky_output_frame, height=10, width=30)
        # self.feeling_lucky_output.grid(row=2, column=0, padx=5, pady=10)

        # Show Alias History button
        self.alias_history_button = tk.Button(self.master, text=">>\n\n\n>>\n\n\n>>", font="bold", command=self.show_alias_history)
        self.alias_history_button.grid(row=1, column=1, rowspan=3, padx=2, pady=10)

        # Info button
        self.info_button = tk.Button(self.master, text="info", command=self.open_info)
        self.info_button.grid(row=0, column=1, columnspan=1, padx=2, pady=3)

    def load_default_input(self):
        if os.path.isfile(self.default_input_file):
            with open(self.default_input_file, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    base_email = lines[0].strip()
                    base_alias = lines[1].strip()
                    self.base_email.delete(0, tk.END)
                    self.base_email.insert(0, base_email)
                    self.base_alias.delete(0, tk.END)
                    self.base_alias.insert(0, base_alias)
                    self.confirmation_label.config(text="Defaults Loaded")
                    t = threading.Timer(3.0, self.reset_confirmation)
                    t.start()
                    
        else:
            with open(self.default_input_file, 'w') as file:
                file.write('edit@this.com\n')
                file.write('baseAlias\n')
                self.base_email.delete(0, tk.END)
                self.base_email.insert(0, "edit@this.com")
                self.base_alias.delete(0, tk.END)
                self.base_alias.insert(0, 'baseAlias')
                self.confirmation_label.config(text="Defaults Created")
                t = threading.Timer(3.0, self.reset_confirmation)
                t.start()

    def save_default_input(self):
        with open(self.default_input_file, 'w') as file:
            file.write(self.base_email.get() + '\n')
            file.write(self.base_alias.get() + '\n')
        self.confirmation_label.config(text="Defaults Saved", fg="White", bg="Blue")
        # Reset label text after 2 seconds
        t = threading.Timer(2.0, self.reset_confirmation)
        t.start()


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

             # Create new frame for alias history clear/save/load buttons in history frame
            history_function_frame = tk.Frame(self.history_frame, relief="groove")
            history_function_frame.grid(row=0, column=0, columnspan=2, padx=2, pady=3)

            # Create a Text widget to display the history
            self.history_text = tk.Text(self.history_frame, height=15, width=75)
            self.history_text.grid(row=1, column=0, columnspan=1, rowspan=3, padx=2, pady=3, sticky="nsew")

            # Save alias history button
            self.save_history_button = tk.Button(history_function_frame, text="Save History", command=self.save_alias_history)
            self.save_history_button.grid(row=0, column=0, padx=5, pady=5)

            # Load alias history button
            self.load_history_button = tk.Button(history_function_frame, text="Load History", command=self.load_alias_history)
            self.load_history_button.grid(row=0, column=1, padx=5, pady=5)

            # Clear alias history button
            self.clear_history_button = tk.Button(history_function_frame, text="Clear History", command=self.clear_alias_history)
            self.clear_history_button.grid(row=0, column=2, padx=5, pady=5)

            # Insert the history into the Text widget
            for alias in self.alias_history:
                self.history_text.insert(tk.END, alias + "\n")

    def update_history_display(self):
        if hasattr(self, 'history_text'):  # Check if history_text attribute exists
            self.history_text.delete("1.0", tk.END)
            for alias in self.alias_history:
                self.history_text.insert(tk.END, alias + "\n")
            self.history_text.see(tk.END)  # Scroll to the end of the text

    def toggle_history(self):
        # Toggle the visibility of the history section
        if self.history_frame.winfo_ismapped():
            self.history_frame.grid_forget()
            self.alias_history_button.config(text=">>\n\n\n>>\n\n\n>>")
        else:
            self.history_frame.grid(row=0, column=2, rowspan=3, padx=2, pady=3, sticky="nsew")
            self.alias_history_button.config(text="<<\n\n\n<<\n\n\n<<")

    def clear_alias_history(self):
        #prompt user to confirm clear alias history
        if messagebox.askyesno("Warning", "You are about to clear Alias History. Do you want to proceed?"):
            self.alias_history.clear()
            self.update_history_display()
            self.confirmation_label.config(text="Alias History Cleared", fg="White", bg="Blue")
            t = threading.Timer(2.0, self.reset_confirmation)
            t.start()

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

            self.confirmation_label.config(text="Alias History Saved", fg="White", bg="Blue")
            t = threading.Timer(2.0, self.reset_confirmation)
            t.start()

    def load_alias_history(self):
        if messagebox.askyesno("Warning", "Loading a file will overwrite the current alias history. Do you want to proceed?"):
            self.alias_history.clear()
            file_name = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_name:
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

                if self.history_text.get("1.0", tk.END) != "\n":
                    self.history_text.delete("1.0", tk.END)
                for alias in self.alias_history:
                    self.history_text.insert(tk.END, alias + "\n")
                self.history_text.see(tk.END)  # Scroll to the end of the text
                # update confrimation
                self.confirmation_label.config(text="Alias History Loaded", fg="White", bg="Blue")
                t = threading.Timer(2.0, self.reset_confirmation)
                t.start()

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
    
    def generate_random_email_alias(self, ts_toggle, cn_toggle, copy_to_clipboard=True):
        """Generates a random email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("%y-%m-%d-%H.%M.%S")
        # check for valid base email
        if self.is_valid_base_email(base_email):
            username, domain = base_email.split('@')

            if ts_toggle.get() and cn_toggle.get():
                random_string = ''.join(timestamp)
                fake_name = Faker()
                random_company_name = fake_name.company()
                random_company = "".join(random_company_name.replace(' ', '').replace(',', ''))
                self.email_alias.delete(0, tk.END)
                self.email_alias.insert(0, f"{username}+{random_company}.{random_string}@{domain}")

            elif ts_toggle.get():
                random_string = ''.join(timestamp)
                self.email_alias.delete(0, tk.END)
                self.email_alias.insert(0, f"{username}+{random_string}@{domain}")

            # check for company name override
            elif cn_toggle.get():
                # Generate fake company name
                fake_name = Faker()
                random_company_name = fake_name.company()
                random_company = "".join(random_company_name.replace(' ', '').replace(',', ''))
                self.email_alias.delete(0, tk.END)
                self.email_alias.insert(0, f"{username}+{random_company}@{domain}")

            else:
                # Generate fake name
                fake_name = Faker()
                random_full_name = fake_name.name()
                random_name = "".join(random_full_name.split())
                self.email_alias.delete(0, tk.END)
                self.email_alias.insert(0, f"{username}+{random_name}@{domain}")

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

    def generate_base_alias_email_alias(self, ts_toggle, cn_toggle, copy_to_clipboard=True):
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

                if ts_toggle.get() and cn_toggle.get():
                    random_string = ''.join(timestamp)
                    fake_name = Faker()
                    random_company_name = fake_name.company()
                    random_company = "".join(random_company_name.replace(' ', '').replace(',', ''))
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_company}.{random_string}@{domain}")

                elif ts_toggle.get():
                    random_string = ''.join(timestamp)
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_string}@{domain}")

                elif cn_toggle.get():
                    # Generate fake company name
                    fake_name = Faker()
                    random_company_name = fake_name.company()
                    random_company = "".join(random_company_name.replace(' ', '').replace(',', ''))
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_company}@{domain}")
                else:
                    # Generate fake name
                    fake_name = Faker()
                    random_full_name = fake_name.name()
                    random_name = "".join(random_full_name.split())
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_name}@{domain}")

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

    def feeling_lucky(self, cn_toggle):
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
                fake_name = Faker()

                if cn_toggle.get():
                    #random_full_name = fake_name.name()
                    #random_name = "".join(random_full_name.split())
                    random_aliases = [f"{username}+{base_alias}.{''.join(fake_name.company().replace(' ', '').replace(',', ''))}@{domain}" for i in range(10)]
                    # self.feeling_lucky_output.delete('1.0', tk.END)
                    # self.feeling_lucky_output.insert('1.0', '\n'.join(random_aliases))
                    
                    for alias in random_aliases:
                        self.alias_history.append(alias + " | Timestamp: " + timestamp + "*")

                    # Click confirmation prompt
                    self.generate_click_confirmation(self.lucky_button)
                    self.confirmation_label.config(text="10x Alias", fg="White", bg="Green")
                    t = threading.Timer(1.0, self.reset_confirmation)
                    t.start()

                    # Update History Display after appending lucky output
                    self.update_history_display()

                else:
                    #random_full_name = fake_name.name()
                    #random_name = "".join(random_full_name.split())
                    random_aliases = [f"{username}+{base_alias}.{''.join(fake_name.name().split())}@{domain}" for i in range(10)]
                    # self.feeling_lucky_output.delete('1.0', tk.END)
                    # self.feeling_lucky_output.insert('1.0', '\n'.join(random_aliases))

                    for alias in random_aliases:
                        self.alias_history.append(alias + " | Timestamp: " + timestamp + "*")

                    # Click confirmation prompt
                    self.generate_click_confirmation(self.lucky_button)
                    self.confirmation_label.config(text="10x Alias", fg="White", bg="Green")
                    t = threading.Timer(1.0, self.reset_confirmation)
                    t.start()

                    # Update History Display after appending lucky output
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

    def open_info(self):
        # Create a Frame for the collapsible settings section
        self.info_window = tk.Toplevel(self.master)
        self.info_window.title("-REAG Info-")
        self.info_window.focus_force()

        # Create and configure widgets in the info window
        title_label = tk.Label(self.info_window, 
                              text=f"Thanks for downloading REAG (Random Email Alias Generator).\n"
                              " This application generates random email aliases based on a few generation rules.\n")
        title_label.pack()

        input_validation_Title = tk.Label(self.info_window, text=f"Input Validation:", font="bold")
        input_validation_Title.pack()
        input_validation_info = tk.Label(self.info_window, text=
                              "There is no character limit validation to input, user beware.\n"
                              "Base email input will check for a string in the following format: '<username>@<domain>.<TLD>'.\n"
                              "Base alise input will check for a string in the following format: '[a-zA-Z0-9._%-]'.\n"
                              "(Any uppercase or lowercase letter (a-z, A-Z), digit (0-9), period (.), underscore (_), percent symbol (%), or hyphen (-))\n")
        input_validation_info.pack()

        options_Title = tk.Label(self.info_window, text=f"Customization Options:", font="bold")
        options_Title.pack()
        options_info = tk.Label(self.info_window, text=
                                 "Default alias generation creates an email with random first and last name.\n"
                                 "Timestamp Alias will override alias generation with the current timestamp.\n"
                                 "Company Alias will generate company names instead of first and last name aliases.\n"
                                 "Save current base email and alias as defaults for app launch. File saved to desktop.\n")
        options_info.pack()
        
        default_email_label = tk.Label(self.info_window, text="Save current base email and alias", font="bold")
        default_email_label.pack()

        default_email_button = tk.Button(self.info_window, text="Save Defaults", command=self.save_default_input)
        default_email_button.pack()

        program_info = tk.Label(self.info_window, text=f"\nProgram Description:")
        program_info.pack()

        version_label = tk.Label(self.info_window, text="Version: 0.3.1-beta")
        version_label.pack()

        version_text = tk.Label(self.info_window, text=f"Maintained and Programed by Jake.\n"
                                "Stay up to date at:")
        version_text.pack()

        url_text = tk.Text(self.info_window, height=1, width=52)
        url_text.insert(tk.END, "https://github.com/JakeOrona/RandEmailAlias/releases")
        url_text.pack()
        
        # Run the info window's event loop
        self.info_window.mainloop()

    """def toggle_settings(self):
        # Toggle the visibility of the settings section
        if self.info.winfo_ismapped():
            self.settings_options_frame.grid_forget()
            self.settings_button.config(text="View Settings")
        else:
            self.settings_options_frame.grid(row=4, column=0, rowspan=2, padx=2, pady=3, sticky="nsew")
            self.settings_button.config(text="Hide Settings")"""

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
        button.config(text="ʕ º ᴥ ºʔ")
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
            button.config(text="Generate Random Alias")
        elif button == self.generate_alias_button:
            button.config(text="Generate Using Base Alias")
        elif button == self.lucky_button:
            button.config(text="Feeling Lucky")
        elif button == self.copy_button:
            button.config(text="Copy to Clipboard")
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
