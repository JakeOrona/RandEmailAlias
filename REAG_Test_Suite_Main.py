# Main file for test suite

import unittest
import tkinter as tk
import threading
from REAG import RandomEmailAliasGenerator as REAG

class AppFunctionalityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.top = tk.Toplevel()  # Create a new top-level window
        cls.app = REAG(cls.top)  # Instantiate app with the top-level window argument

    @classmethod
    def tearDownClass(cls):
        cls.top.destroy()  # Destroy the top-level window

    def test_generate_random_email_alias(self):
        # Simulate user input
        self.app.base_email.delete(0, tk.END)
        self.app.base_email.insert(0, "test@example.com")
        self.app.generate_button.invoke()

        # Validate the generated alias
        generated_alias = self.app.email_alias.get()
        self.assertNotEqual(generated_alias, "", "Failed to generate random email alias")
        # Add more assertions to validate the format or specific properties of the generated alias
        self.app.top.after(0, lambda: print("Test 'generate_random_email_alias' passed. Generated alias:", generated_alias))

    def test_generate_alias_using_base_alias(self):
        # Simulate user input
        self.app.base_email.delete(0, tk.END)
        self.app.base_email.insert(0, "test@example.com")
        self.app.base_alias.delete(0, tk.END)
        self.app.base_alias.insert(0, "TEST")
        self.app.generate_alias_button.invoke()

        # Validate the generated alias
        generated_alias = self.app.email_alias.get()
        self.assertNotEqual(generated_alias, "", "Failed to generate email alias using base alias")
        # Add more assertions to validate the format or specific properties of the generated alias
        self.app.top.after(0, lambda: print("Test 'generate_alias_using_base_alias' passed. Generated alias:", generated_alias))

    # Implement the remaining test functions for other test cases...

def run_tests():
    unittest.main()

if __name__ == '__main__':
    # Run the test suite in a separate thread
    test_thread = threading.Thread(target=run_tests)
    test_thread.start()
