# v2.4.1-beta-macOS

import random
import string
import tkinter as tk
import threading
import datetime
import re
# import io
#from urllib.request import urlopen
#from PIL import ImageTk, Image
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

class RandomEmailAliasGenerator:
    def __init__(self, master):
        """Initializes the GUI"""
        self.master = master
        self.master.title("R.E.A.G. ʕ º ᴥ ºʔ")

        # Set window size for responsive window
        self.master.rowconfigure((0,1,2), weight=1, minsize=30)
        self.master.columnconfigure((0), weight=1, minsize=30)

        """# Load the image
        # url = "https://i.imgur.com/yzC0PES.jpeg"
        # image_data = urlopen(url).read()
        image = Image.open('resources/REAG-BG.jpg')
        background_image = ImageTk.PhotoImage(image)

        # Create a label for the image
        background_label = tk.Label(self.master, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image"""

        # Create new frame for base input
        base_email_frame = tk.Frame(self.master, borderwidth=2, relief="groove")
        base_email_frame.grid(row=0, column=0, columnspan=1, padx=5, pady=3)

        # Create new frame for all buttons
        buttons_frame = tk.Frame(self.master, borderwidth=2, relief="groove")
        buttons_frame.grid(row=1, column=0, columnspan=1, padx=5, pady=3)

        # Create new frame for feeling lukcy output
        feeling_lucky_output_frame = tk.Frame(self.master, borderwidth=2, relief="groove")
        feeling_lucky_output_frame.grid(row=2, column=0, columnspan=1, padx=2, pady=3)

        # Base email label and input field in base_email_frame
        tk.Label(base_email_frame, text="Base Email:").grid(row=0, column=0, padx=5, pady=5)
        self.base_email = tk.Entry(base_email_frame, width=25)
        self.base_email.grid(row=1, column=0, padx=10, pady=5)
        self.base_email.focus()

        # Base alias label and input field
        tk.Label(base_email_frame, text="Base Alias: IE: 'TEST'").grid(row=2, column=0, padx=5, pady=5)
        self.base_alias = tk.Entry(base_email_frame, width=25)
        self.base_alias.grid(row=3, column=0, padx=5, pady=5)

         # Toggle for timestamp alias
        ts_toggle = tk.BooleanVar()
        checkbutton = tk.Checkbutton(base_email_frame, text=f"Timestamp Alias Override\nYY-MM-DD-HH.MM.SS\n('Base Alias Email' button only)", variable=ts_toggle, onvalue=True, offvalue=False)
        checkbutton.grid(row=4, column=0, padx=5, pady=5)

        # Generated email alias label and output field
        tk.Label(buttons_frame, text="Magic Output:").grid(row=4, column=0, padx=5, pady=5)
        self.email_alias = tk.Entry(buttons_frame, width=25)
        self.email_alias.grid(row=5, column=0, padx=7, pady=5)

        # Generate random email button
        self.generate_button = tk.Button(buttons_frame, text="Random Email", command=self.generate_random_email_alias)
        self.generate_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        # Random email button info
        tk.Label(buttons_frame, text="Generate random alias\nie: jake+abc123@gmail.com").grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        # Generate test email alias button
        self.generate_test_button = tk.Button(buttons_frame, text="Base Alias Email", command=lambda: self.generate_base_alias_email_alias(ts_toggle))
        self.generate_test_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        # Test  email button info
        tk.Label(buttons_frame, text="Generate using base alias\n ie: jake+TEST.abc123@gmail.com").grid(row=2, column=0, columnspan=1, padx=5, pady=5)

        # Copy to Clipboard button
        self.copy_button = tk.Button(buttons_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Generate 10 aliases button
        self.lucky_button = tk.Button(feeling_lucky_output_frame, text="Feeling Lucky", command=self.feeling_lucky)
        self.lucky_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        # Generate 10 aliases button info
        tk.Label(feeling_lucky_output_frame, text="Generate 10 aliases using base alias").grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        # Feeling lucky output field
        self.feeling_lucky_output = tk.Text(feeling_lucky_output_frame, height=10, width=30)
        self.feeling_lucky_output.grid(row=2, column=0, padx=5, pady=5)

        # Label to display copy confirmation message
        self.copy_label = tk.Label(buttons_frame, text="")
        self.copy_label.grid(row=7, column=0, padx=5, pady=5)

        # Label to display button click confirmation message
        self.click_confirmation_label = tk.Label(buttons_frame, text="")
        self.click_confirmation_label.grid(row=7, column=0, padx=5, pady=5)

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
    
    def generate_random_email_alias(self):
        """Generates a random email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        # check for valid base email
        if self.is_valid_base_email(base_email):
            username, domain = base_email.split('@')
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            self.email_alias.delete(0, tk.END)
            self.email_alias.insert(0, f"{username}+{random_string}@{domain}")
            # Click confirmation prompt
            self.click_confirmation()
            # Reset the copy label
            self.copy_label.config(text="")
        else:
            # Display error message
            self.email_alias.delete(0, tk.END)
            self.email_alias.insert(0, f"ENTER A VALID BASE EMAIL")
            self.error_confirmation()

    def generate_base_alias_email_alias(self, ts_toggle):
        """Generates a test email alias based on a base email. 6 chars"""
        base_email = self.base_email.get()
        base_alias = self.base_alias.get()
        # check for base alias not null
        if self.is_base_alias_not_null(base_alias):
            # Check for valid base email
            if self.is_valid_base_email(base_email):
                username, domain = base_email.split('@')

                if ts_toggle.get():
                    now = datetime.datetime.utcnow()
                    timestamp = now.strftime("%y-%m-%d-%H.%M.%S")
                    random_string = ''.join(timestamp)
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_string}@{domain}")
                    # Click confirmation prompt
                    self.click_confirmation()
                    # Reset the copy label
                    self.copy_label.config(text="")

                else:
                    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                    self.email_alias.delete(0, tk.END)
                    self.email_alias.insert(0, f"{username}+{base_alias}.{random_string}@{domain}")
                    # Click confirmation prompt
                    self.click_confirmation()
                    # Reset the copy label
                    self.copy_label.config(text="")
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
        base_alias = self.base_alias.get()
        # check for base alias not null
        if self.is_base_alias_not_null(base_alias):
            # Check for valid base email
            if self.is_valid_base_email(base_email):
                username, domain = base_email.split('@')
                random_aliases = [f"{username}+{base_alias}.{''.join(random.choices(string.ascii_letters + string.digits, k=6))}@{domain}" for i in range(10)]
                self.feeling_lucky_output.delete('1.0', tk.END)
                self.feeling_lucky_output.insert('1.0', '\n'.join(random_aliases))
                # Click confirmation prompt
                self.click_confirmation()
            else:
                # Display error message
                self.feeling_lucky_output.delete('1.0', tk.END)
                self.feeling_lucky_output.insert('1.0', f"ENTER A VALID BASE EMAIL")
                self.error_confirmation()
        else:
            # Display error message
            self.feeling_lucky_output.delete('1.0', tk.END)
            self.feeling_lucky_output.insert('1.0', f"ENTER A BASE ALIAS")
            self.error_confirmation()

    def copy_to_clipboard(self):
        """Copies the generated email alias to the clipboard"""
        self.master.clipboard_clear()
        self.master.clipboard_append(self.email_alias.get())
        self.copy_label.config(text="EMAIL - COPIED", fg="green")
        # Reset label text after 2 seconds
        t = threading.Timer(2.0, self.reset_copy_confirmation)
        t.start()


    def click_confirmation(self):
        """When button clicked display confirmation"""
        self.click_confirmation_label.config(text="ʕ º ᴥ ºʔ", fg="green")
        # Reset label text after 1 second
        t = threading.Timer(1.0, self.reset_click_confirmation)
        t.start()

    def error_confirmation(self):
        """When invalid base email or null base alias display error"""
        self.click_confirmation_label.config(text="(ノಠ益ಠ)ノ彡┻━┻", fg="Red")

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
