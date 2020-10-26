# Importing
import tkinter as tk
from tkinter.messagebox import askokcancel, showinfo, showerror, showwarning
from subprocess import call
import os
import datetime as dt
import time
import csv
import urllib.request
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory, askopenfile, asksaveasfile

logs_lq = []
csv_things = []

# Function to install a package

logs = []
answers_prov = []
marks_obt = []
def next_q(q_id):
    if types[q_id] == 'mcq':
        try:

            if options[q_id].split(';')[opts_var.get()-1] in answers[q_id].split(';'):
                if answers[q_id] == '':
                    answers_prov.append(options[q_id].split(';')[opts_var.get()-1])
                    showwarning('Alert', 'Since you just answered a question without an answer, we cannot grade it. Sorry about the inconvinience. Your invidulator can use your end result and grade you.')
                    logs.append('Manual')
                    marks_obt.append('?')
                elif options[q_id].split(';')[opts_var.get()-1] != '' and opts_var.get()-1 > -1:
                    answers_prov.append(options[q_id].split(';')[opts_var.get()-1])
                    showinfo('Correct!', 'Your answer is correct!')
                    logs.append('Auto: Correct')
                    marks_obt.append(marks[q_id])
                else:
                    answers_prov.append('')
                    showerror('Sorry!', 'You did not provide any info!')
                    logs.append('Auto: Wrong')
                    marks_obt.append('0')
            else:
                answers_prov.append(options[q_id].split(';')[opts_var.get()-1])
                showerror('Sorry!', 'Your answer is incorrect!')
                logs.append('Auto: Wrong')
                marks_obt.append('0')
        except:
            answers_prov.append(options[q_id].split(';')[opts_var.get()-1])
            showerror('Sorry!', 'Your answer is incorrect!')
            logs.append('Auto: Wrong')
            marks_obt.append('0')


    elif types[q_id] == 'sq':
        answers_prov.append(field.get())
        if field.get() in answers[q_id].split(';'):
            if answers[q_id] == '':
                logs.append('Manual')
                marks_obt.append('?')
                showwarning('Alert', 'Since you just answered a question without an answer, we cannot grade it. Sorry about the inconvinience. Your invidulator can use your end result and grade you.')
            else:
                showinfo('Correct!', 'Your answer is correct!')
                logs.append('Auto: Correct')
                marks_obt.append(marks[q_id])
        else:
            showerror('Sorry!', 'Your answer is incorrect!')
            logs.append('Auto: Wrong')
            marks_obt.append('0')


    elif types[q_id] == 'lq':
        answers_prov.append('Check the Text File')
        logs.append('Manual')
        showwarning('Alert', 'Since you just answered a long answer question, we cannot grade it. Sorry about the inconvinience. Your invidulator can use your end result and grade you.')
        logs_lq.append('\nQUESTION '+str(q_id+1)+'\n\n'+field.get('1.0', 'end-1c')+'\n')
        marks_obt.append('?')
    root.destroy()

    make_quiz(q_id+1)
    

def make_quiz(q_id):
    try:
        global root
        root = tk.Tk()
        root.title('Quiz - PyQuiz')
        q = tk.Label(root, text=questions[q_id])
        q.pack()
        if types[q_id] == 'mcq':
            global opts_var
            global field
            opts_var = tk.IntVar()
            option = options[q_id].split(';')
            for x in range(len(option)):
                exec('global opt'+str(x)+'; opt'+str(x)+' = tk.Radiobutton(root, text="'+option[x]+'", variable=opts_var, value='+str(x+1)+')')
                exec('opt'+str(x)+'.pack()')
        elif types[q_id] == 'sq':
            field = tk.Entry(root, width = 20)
            field.pack()
        elif types[q_id] == 'lq':
            field = ScrolledText(root)
            field.pack()
        next_but = tk.Button(root, text='Submit and Continue', command = lambda:next_q(q_id ))
        next_but.pack()
        root.mainloop()
    except IndexError:
        showinfo('Quiz Completed!', 'You have successfully completed your quiz! You will now be prompted to save your answer CSV. Please save it!')
        file_dir = askdirectory()
        try: os.remove(file_dir+'/Long Answers.txt')
        except: pass
        try: os.remove(file_dir+'/results.csv')
        except: pass
        csv_file = open(file_dir+'/results.csv', 'a')
        long_q = open(file_dir+'/Long Answers.txt', 'a')
        csv_file.write('Question No.,Type,Question,Correct Answer,Given Answer,Correction,Marks\n')
        x = 0
        for x in range(q_id):
            csv_file.write(str(x+1)+','+types[x]+','+questions[x]+','+answers[x]+','+answers_prov[x]+','+logs[x]+','+marks_obt[x]+'/'+marks[x]+'\n')
        #long_q.write(str(logs_lq))
        for b in logs_lq:
            long_q.write(b)
        csv_file.close()
        long_q.close()

# Class to organise the introductory code
def init_array(subject):
    welcome_window.destroy()
    table = list(csv.reader(open(subject)))
    global types
    global questions
    global options
    global answers
    global marks
    types = []
    questions = []
    options = []
    answers = []
    marks = []
    for x in range(len(table)):
        types.append(table[x][0])
        questions.append(table[x][1])
        options.append(table[x][2])
        answers.append(table[x][3])
        marks.append(table[x][4])
    make_quiz(0)
        
    
class Intro:
    def cont(self):
        pass
    def open_quiz_csv(self):
        file_loc = askopenfile(title = "Select Quiz File",filetypes = (("Comma Separated Values","*.csv"),))
        init_array(file_loc.name)
    def ask_name(self):
        global welcome_window
        welcome_window = tk.Tk()
        welcome_window.title("Choose a Subject")

        welcome_msg = tk.Label(welcome_window, text = "Welcome To PyQuiz! Which Quiz Do You Want To Continue With?").grid(row = 0, columnspan = 4)

        py_but = tk.Button(welcome_window, command=lambda: init_array('Python.csv') ,text = "Python").grid(row = 1, column = 0)
        code_but = tk.Button(welcome_window,command=lambda: init_array('Coding.csv'), text = "Coding").grid(row = 1, column = 1)
        gk_button = tk.Button(welcome_window,command=lambda: init_array('GK.csv'), text = "General Knowledge").grid(row = 1, column = 2)
        file_button = tk.Button(welcome_window,command=self.open_quiz_csv, text = "External Quiz").grid(row = 1, column = 3)

        welcome_window.mainloop()


intro_handle = Intro()

intro_handle.ask_name()