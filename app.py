import tkinter as tk
from tkinter import messagebox
from core import generate_questions, generate_pdf
import pandas as pd

df = pd.read_csv('sample_questions/Questions100_Abstractions.csv')
df['question'] = df['question'].replace('\n','<br />', regex=True)

class QuestionGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Question Paper Generator Abstraction")
        self.radio_var = tk.StringVar()
        self.radio_var.set("Easy")  # Set the default value

        self.create_widgets()

    def generate_pdf(self):
        pdf_name = self.output_name_entry.get().strip()
        
        
        
        if pdf_name:
            selected_option = self.radio_var.get()
            ques = df[df['level'] == selected_option]
            # Add code here to generate the PDF with the selected option and the pdf_name
            number_of_papers = int()
            if self.num_papers_entry.get().strip():
                if self.num_papers_entry.get().strip().isdigit():
                    number_of_papers = int(self.num_papers_entry.get().strip())
                    print("number of")
                else:
                    messagebox.showerror("Error", "Please enter a valid number of papers.")
            else:
                number_of_papers = 1
            print(number_of_papers)
            for i in range(0, number_of_papers):
                questions = generate_questions.generate_question(input_ques=ques)
                
                generate_pdf.generate_pdf(questions, pdf_name=f'{pdf_name}_{i+1}')
        else:
            messagebox.showerror("Error", "Please enter a valid PDF name.")

    def create_widgets(self):
        # Radio buttons
        option1_radio = tk.Radiobutton(self.root, text="Easy", variable=self.radio_var, value="easy")
        option2_radio = tk.Radiobutton(self.root, text="Medium", variable=self.radio_var, value="medium")
        option3_radio = tk.Radiobutton(self.root, text="Hard", variable=self.radio_var, value="hard")


        num_papers_label = tk.Label(self.root, text="Number of papers you want to generate:")
        self.num_papers_entry = tk.Entry(self.root)
        
        # Output PDF name entry field
        output_name_label = tk.Label(self.root, text="Output PDF Name:")
        self.output_name_entry = tk.Entry(self.root)

        # Generate Button
        generate_button = tk.Button(self.root, text="Generate PDF", command=self.generate_pdf)

        # Layout using grid
        option1_radio.grid(row=0, column=0, padx=10, pady=5)
        option2_radio.grid(row=1, column=0, padx=10, pady=5)
        option3_radio.grid(row=2, column=0, padx=10, pady=5)

        num_papers_label.grid(row=3, column=0, padx=10, pady=5)
        self.num_papers_entry.grid(row=3, column=1, padx=10, pady=5)
        
        output_name_label.grid(row=4, column=0, padx=10, pady=5)
        self.output_name_entry.grid(row=4, column=1, padx=10, pady=5)

        generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def run(self):
        # Start the main event loop
        self.root.mainloop()


