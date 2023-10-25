import tkinter as tk
import tkinter.ttk as ttk
import re

class EmailInfoExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Information Extractor")
        self.root.geometry('800x600')  # Initial window size
        self.root.configure(background="#303030")

        # Create a Panedwindow for input and output
        self.paned_window = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(expand=True, fill=tk.BOTH)

        # Create input field (responsive)
        self.text_input = tk.Text(self.paned_window, height=10, width=40, bg="#EFEFEF", fg="#000000")
        self.paned_window.add(self.text_input)

        # Create a frame for task selection
        task_frame = ttk.LabelFrame(self.paned_window, text="Choose Your Task")
        self.paned_window.add(task_frame, weight=1)  # Set expand=True for the label frame

        # Custom buttons for tasks (responsive)
        style = ttk.Style()
        style.configure("Bold.TButton", font=('Helvetica', 12, 'bold'))
        style.map("Bold.TButton",
                  foreground=[('pressed', '#FF6969'), ('active', 'black')],
                  background=[('pressed', '!disabled', 'yellow'), ('active', 'red')])

        self.create_button(task_frame, "Find Emails", self.find_emails, 1, 0)
        self.create_button(task_frame, "Find Dates & Subjects", self.find_dates_subjects, 2, 0)
        self.create_button(task_frame, "Find URLs", self.find_urls, 3, 0)
        self.create_button(task_frame, "Find Keywords", self.find_keywords, 4, 0)
        self.create_button(task_frame, "Extract Message Body", self.extract_message_body, 5, 0)

        # Create result display area (responsive)
        self.result_display = tk.Text(self.paned_window, height=10, width=40, bg="#D8D9DA", fg="#1AACAC", font=("Bold", 15))
        self.paned_window.add(self.result_display)

        # Set the weights for the panes
        self.paned_window.grid_rowconfigure(0, weight=1)
        self.paned_window.grid_columnconfigure(0, weight=1)
        self.paned_window.grid_rowconfigure(1, weight=1)
        self.paned_window.grid_columnconfigure(1, weight=1)

    def create_button(self, parent, text, command, row, column):
        button = ttk.Button(parent, text=text, command=command, style="Bold.TButton")
        button.grid(row=row, column=column, padx=10, pady=5, sticky="ew")

    def find_emails(self):
        email_pattern = r'\S+@\S+'
        emails = re.findall(email_pattern, self.text_input.get(1.0, tk.END))
        self.display_results("Emails", emails)

    def find_dates_subjects(self):
        date_subject_pattern = r'Subject: (.*?)\nDate: (.*?)\n'
        matches = re.findall(date_subject_pattern, self.text_input.get(1.0, tk.END))
        self.display_results("Dates & Subjects", matches)

    def find_urls(self):
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, self.text_input.get(1.0, tk.END))
        self.display_results("URLs", urls)

    def find_keywords(self):
        keywords = ["innovative", "limited-time offer"]
        text = self.text_input.get(1.0, tk.END).lower()
        found_keywords = [keyword for keyword in keywords if keyword in text]
        self.display_results("Keywords", found_keywords)

    def extract_message_body(self):
        text = self.text_input.get(1.0, tk.END)
        start_index = text.find("Dear all")
        if start_index != -1:
            message_body = text[start_index:]
            self.display_results("Message Body", [message_body])
        else:
            self.display_results("Message Body", ["No 'Dear all' found in the text"])

    def display_results(self, title, results):
        self.result_display.delete(1.0, tk.END)
        if results:
            self.result_display.insert(tk.END, f"{title}:\n")
            for result in results:
                self.result_display.insert(tk.END, f"{result}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailInfoExtractorApp(root)
    root.mainloop()
