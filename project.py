# Importing necessary libraries and modules
import random
import pyttsx3
from fractions import Fraction
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF


class Exam:
    """
    Class representing a math quiz.

    Attributes:
        question (str): The math question.
        _X (int): Operand X.
        _Y (int): Operand Y.
        _Z (int): Operand Z.
        _S (str): The type of operation.
        answer_actual (int): The actual answer.
        answer_actual_remainder (int): The remainder for division problems.
        answer_user (int): The user's answer.
        answer_user_remainder (int): The user's remainder for division problems.
        _score (int): The user's score.
    """
    @classmethod
    def quiz(cls, sign_list):
        """Generate a random math question based on selected operations."""
        # Remove '0' from the sign list
        while "0" in sign_list:
            sign_list.remove("0")
        S = random.choice(sign_list)
        while True:
            # Generate random numbers based on the selected operation
            X = random.randint(1, 10000)
            Y = random.randint(1, 10000)
            Z = random.randint(1, 10000)
            
            # Check if the generated question meets specific criteria
            if (S == "+" and X > 1000 and Y > 1000) or (S == "-" and X > 1000 and Y > 1000 and X > Y) or (S == "*" and X > 1000 and 100> Y > 0) or (S == "/" and X > 1000 and 1 < Y < 10 and X % Y != 0):
                quiz = f"{X} {S} {Y}"
                break
            elif S == "fraction":
                frac_ops = ["+", "-", "*", "/"]
                op = random.choice(frac_ops)
                a = random.randint(1, 9)
                b = random.randint(2, 9)
                c = random.randint(1, 9)
                d = random.randint(2, 9)
                quiz = f"{a}/{b} {op} {c}/{d}"
                X = a
                Y = b
                Z = (c, d)
                S = f"f{op}"
                break
        return cls(quiz, X, Y, Z, S)

     # Initialize Exam object
    def __init__(self, question, X, Y, Z, S):
        """
        Initialize Exam object.

        Args:
            question (str): The math question.
            X (int): Operand X.
            Y (int): Operand Y.
            Z (int): Operand Z.
            S (str): The type of operation.
        """
        self.question = question
        self._X, self._Y, self._Z, self._S = X, Y, Z, S
        
        # Calculate the actual answer based on the operation
        if self._S == "+":
            self.answer_actual = self._X + self._Y
        elif self._S == "-":
            self.answer_actual = self._X - self._Y
        elif self._S == "*":
            self.answer_actual = self._X * self._Y
        elif self._S == "/":
            self.answer_actual = int(self._X / self._Y)         # Applied 'int' Method for proper feedback dispaly on Answer Submission!
            self.answer_actual_remainder = self._X % self._Y
        elif self._S == "fraction":
            self.answer_actual = int(self._X / self._Y) * self._Z
        elif self._S in ["f+", "f-", "f*", "f/"]:
            frac1 = Fraction(self._X, self._Y)
            frac2 = Fraction(self._Z[0], self._Z[1])
            if self._S == "f+":
                self.answer_actual = frac1 + frac2
            elif self._S == "f-":
                self.answer_actual = frac1 - frac2
            elif self._S == "f*":
                self.answer_actual = frac1 * frac2
            elif self._S == "f/":
                self.answer_actual = frac1 / frac2
        self.answer_user = 0
        self.answer_user_remainder = 0
        
    @property
    def question(self):
        """Getter method for the question."""
        return self._question

    @question.setter
    def question(self, question):
        self._question = question

    @property
    def answer_actual(self):
        return self._answer_actual
    
    @answer_actual.setter
    def answer_actual(self, answer):
        self._answer_actual = answer

    @property
    def answer_actual_remainder(self):
        return self._answer_actual_remainder
    
    @answer_actual_remainder.setter
    def answer_actual_remainder(self, answer):
        self._answer_actual_remainder = answer

    @property
    def answer_user(self):
        return self._answer_user
    
    @answer_user.setter
    def answer_user(self, answer_user):
        if answer_user >=0:
                self._answer_user = answer_user

    @property
    def answer_user_remainder(self):
        return self._answer_user_remainder
    
    @answer_user_remainder.setter
    def answer_user_remainder(self, answer_user):
        if answer_user >=0:
                self._answer_user_remainder = answer_user

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, marks):
        self._score = marks


class GUI_Exam(Exam):
    """
    Class representing the graphical user interface for a math exam application.

    Attributes:
        - root: Tkinter root window
        - exam_frame: Tkinter frame for the exam interface
        - result_frame: Tkinter frame for the result interface
        - input_user_answer: Tkinter Entry widget for user input
        - input_user_answer_remainder: Tkinter Entry widget for remainder input
        - display_question: Tkinter Label for displaying math questions
        - sound_variable: Tkinter StringVar for sound option
        - grade: Tkinter StringVar for displaying the user's grade
        - grade_label: Tkinter Label for displaying the grade
        - stat_frame: Tkinter Frame for displaying exam statistics
        - quit_button: Tkinter Button for quitting the application

    Methods:
        - __init__: Initialize the GUI_Exam object and set up the initial state.
        - launch_main: Static method to launch the main GUI window.
        - generate_question: Generate and display a new math question.
        - check_answer: Check the user's answer and provide feedback.
        - launch_result_frame: Switch to the result interface after completing the exam.
        - get_grade: Calculate the user's grade based on the exam score.
        - for_correct_answer: Return a random message for correct answers.
        - for_incorrect_answer: Return a random message for incorrect answers.
        - for_failed_attempt: Return a random message for failed attempts.
        - tell_grade: Provide a random congratulatory message based on the grade.
        - store_data: Store user data in a text file during the exam.
        - make_pdf: Generate a PDF report based on user performance.

    Note: This class inherits from Tkinter's Frame class.
    """    
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')                               #getting details of current voice
    engine.setProperty('voice', voices[random.choice([0,1])].id)        #changing index, changes voices. 1 for female
    rate = engine.getProperty('rate')                                   # getting details of current speaking rate
    engine.setProperty('rate', 185)                                     # setting up new voice rate
    
    root = Tk()
    
    @classmethod
    def launch_main(cls):
        """
        Generate and display a new math question.
        """
        cls.root.title("MathQuest Adventures")
        cls.root.state('zoomed')
        cls.root.geometry("1530x775")
        cls.root.iconbitmap("Icon.ico")
        return cls()
            
    def __init__(self):
        """
        Initialize the GUI_Exam object.

        Parameters:
            - master: Parent Tkinter window (default is None)
        """
        self.home_frame = Frame(GUI_Exam.root)
        self.home_label = Label(self.home_frame, text="Welcome to the MathQuest Adventures", font=("Bell MT", 50), justify="center", width=38)
        self.aritmatic_label = Label(self.home_frame, text="Please select Arithmatics:", font=("Bell MT", 20), justify="left")
        self.add_variable = StringVar()
        self.subtract_variable = StringVar()
        self.multiply_variable = StringVar()
        self.divide_variable = StringVar()
        self.fraction_variable = StringVar()
        self.select_all_variable = StringVar()
        self.display_question = StringVar()
        self.grade = StringVar()
        self.sound_variable = StringVar()
        self.add_checkbox = Checkbutton(self.home_frame, text="Addition", variable=self.add_variable, onvalue="+", offvalue=None, font=("Bell MT", 18))
        self.subtract_checkbox = Checkbutton(self.home_frame, text="Subtraction", variable=self.subtract_variable, onvalue="-", offvalue=None, font=("Bell MT", 18))
        self.multiply_checkbox = Checkbutton(self.home_frame, text="Multiplication", variable=self.multiply_variable, onvalue="*", offvalue=None, font=("Bell MT", 18))
        self.divide_checkbox = Checkbutton(self.home_frame, text="Division", variable=self.divide_variable, onvalue="/", offvalue=None, font=("Bell MT", 18))
        self.fraction_checkbox = Checkbutton(self.home_frame, text="Fractions", variable=self.fraction_variable, onvalue="fraction", offvalue=None, font=("Bell MT", 18))
        self.select_all_checkbox = Checkbutton(self.home_frame, text="All of the above!", variable=self.select_all_variable, onvalue="select_all", offvalue=None, font=("Bell MT", 18))
        self.add_checkbox.deselect(), self.subtract_checkbox.deselect(), self.multiply_checkbox.deselect()
        self.divide_checkbox.deselect(), self.fraction_checkbox.deselect(), self.select_all_checkbox.deselect()
        self.label_num_question = Label(self.home_frame, text="Type number of Questions:", font=("Bell MT", 20), justify="left")
        self.input_num_question = Entry(self.home_frame, font=("Bell MT", 20), justify="center", width=3)
        self.start_exam_button = Button(self.home_frame, text="Start Exam!", font=("Bell MT", 14), command=self.start).grid(row=12, column=0, columnspan=5)
        self.test_checkbox = Label(self.home_frame, text="Please ensure correct slections & entry!", font=("Times", 32), bg="red")
        self.exam_frame = Frame(GUI_Exam.root)
        self.status_checkbox, self.question_to_ask = None, None
        self.question_label = Label(self.exam_frame, text=self.display_question.get(), font=("Bell MT", 35), justify="left", width=38)
        self.label_user_answer = Label(self.exam_frame, text="Type Answer Here:", font=("Bell MT", 20), justify="center")
        self.input_user_answer = Entry(self.exam_frame, font=("Bell MT", 20), justify="center", width=7)
        self.label_user_answer_remainder = Label(self.exam_frame, text="Type Remainder Here:", font=("Bell MT", 20), justify="center")
        self.input_user_answer_remainder = Entry(self.exam_frame, font=("Bell MT", 20), justify="center", width=7)
        self.question_asked, self.exam_score = 0, 0          # To keep track of the number of questions & correct answers.
        self.start_time, self.test_start, self.question_paper = None, None, None
        self.attempts_counter = 0
        self.check_button = Button(self.exam_frame, text="Submit", font=("Bell MT", 16),command=self.check_user_answer)
        self.evaluation_feedback = Label(self.exam_frame, font=("Bell MT", 20), justify="center")
        self.evaluation_result, self.end_time, self.test_end = None, None, None
        self.result_frame = Frame(self.root)
        self.grade_label = Label(self.result_frame, font=("Bell MT", 50), justify="center", width=38)
        self.stat_frame = Frame(self.result_frame, width=350, height=475, bd=5, relief="groove")
        self.quit_button = Button(self.result_frame, text="Quit!", font=("Bell MT", 16), command=self.root.quit)
        self.sound_checkbox = Checkbutton(self.exam_frame, text="Disable Sound!", variable=self.sound_variable, onvalue="", offvalue="Enable", font=("Bell MT", 20), bd=5, relief='groove')
        self.file_name = f"Practice_dated_{datetime.now().strftime('%d-%b-%y-%I%M')}"
        self.file_open_mode = None
        self.pdf = None
        self.launch_home_frame()
                
    def launch_home_frame(self):
        self.home_frame.pack(fill="both", expand=1)
        Label(self.home_frame, width=38, height=3).grid(row=1, column=0, columnspan=5)
        self.home_label.grid(row=2, column=0, rowspan=2, columnspan=5)
        Label(self.home_frame, width=38, height=5).grid(row=6, column=0, columnspan=5)
        self.aritmatic_label.grid(row=7, column=0, rowspan=2, columnspan=2)
        self.add_checkbox.grid(row=7, column=2)
        self.subtract_checkbox.grid(row=7, column=3)
        self.multiply_checkbox.grid(row=7, column=4)
        self.divide_checkbox.grid(row=8, column=2)
        self.fraction_checkbox.grid(row=8, column=3)
        self.select_all_checkbox.grid(row=8, column=4)
        Label(self.home_frame, width=38, height=5).grid(row=9, column=0, columnspan=5)
        self.label_num_question.grid(row=10, column=0, columnspan=2)
        self.input_num_question.grid(row=10, column=2)
        Label(self.home_frame, width=38, height=5).grid(row=11, column=0, columnspan=5)
        
    def checkbox_status(self):
        if self.select_all_variable.get() == "select_all" and not self.input_num_question.get() == "" and str(self.input_num_question.get()).isdecimal() and int(self.input_num_question.get()) > 0:
            self.add_variable.set("+"), self.subtract_variable.set("-"), self.multiply_variable.set("*"), self.divide_variable.set("/"), self.fraction_variable.set("fraction")
        status_list = [self.add_variable.get(), self.subtract_variable.get(), self.multiply_variable.get(), self.divide_variable.get(), self.fraction_variable.get()]
        if all(item == "0" or item is None for item in status_list):
            return "Please Select atleast One option!"
        else:
            return [self.add_variable.get(), self.subtract_variable.get(), self.multiply_variable.get(), self.divide_variable.get(), self.fraction_variable.get()]
    
    def start(self):
        """Start the exam based on user selections."""
        self.test_checkbox.grid_forget()
        if self.checkbox_status() == "Please Select atleast One option!" or self.input_num_question.get() == "" or not str(self.input_num_question.get()).isdecimal() or int(self.input_num_question.get()) <= 0:
            self.test_checkbox.grid(row=13, column=0, columnspan=5)
        else:
            self.launch_exam_frame()
            
    def launch_exam_frame(self):
        self.status_checkbox = self.checkbox_status()                 # To fetch the user selection
        self.question_to_ask = int(self.input_num_question.get())     # To fetch how many question to ask
        self.home_frame.pack_forget()
        self.exam_frame.pack(fill="both", expand=1)
        self.sound_checkbox.grid(row=0, column=7)
        self.sound_checkbox.deselect()
        Label(self.exam_frame, width=38, height=5).grid(row=1, column=0, columnspan=5)
        self.question_label.grid(row=2, column=1, rowspan=2, columnspan=5, sticky=W)
        Label(self.exam_frame, width=38, height=5).grid(row=5, column=0, columnspan=5)
        self.label_user_answer.grid(row=6, column=1, rowspan=2, columnspan=2)
        Label(self.exam_frame, width=38, height=5).grid(row=5, column=0, columnspan=5)
        self.input_user_answer.grid(row=6, column=2, rowspan=2, columnspan=1, sticky="E")
        self.start_time = datetime.now()
        self.test_start = self.start_time.strftime("%I:%M%p")
        Label(self.exam_frame, width=38, height=5).grid(row=9, column=0, columnspan=5)
        self.check_button.grid(row=10, column=1)
        Label(self.exam_frame, width=15, height=5).grid(row=11, column=0, columnspan=5)
        self.generate_question()
        
    def generate_question(self):
        """
        Generate and display a new math question.
        """
        self.question_paper = Exam.quiz(self.status_checkbox)
        self.display_question.set(f"Q.{self.question_asked+1} What will be the result of {self.question_paper.question}?")
        self.question_label.config(text=self.display_question.get())
        self.question_asked += 1
        if self.question_paper._S == "/":
            self.label_user_answer.config(text="Type Quotient Here:")
            self.label_user_answer_remainder.grid(row=6, column=3, rowspan=2, columnspan=2, sticky="E")
            self.input_user_answer_remainder.grid(row=6, column=5, rowspan=2, columnspan=1, sticky="W")
        else:
            self.label_user_answer.config(text="Type Answer Here:")
            self.label_user_answer_remainder.grid_forget()
            self.input_user_answer_remainder.grid_forget()
    
    def check_user_answer(self):
        """
        Check the user's answer and provide feedback.
        """
        if self.question_paper._S in ["f+", "f-", "f*", "f/"]:
            try:
                self.question_paper.answer_user = Fraction(self.input_user_answer.get())
            except Exception:
                messagebox.showerror("Input Error", "Please type a valid fraction like 1/2")
                return
        elif str(self.input_user_answer.get()).isdecimal() or str(self.input_user_answer_remainder.get()).isdecimal():
            self.question_paper.answer_user = int(self.input_user_answer.get())
            if self.question_paper._S == "/":
                self.question_paper.answer_user_remainder = int(self.input_user_answer_remainder.get())
            self.evaluation_result = evaluate(self.question_paper.answer_user,
                                            self.question_paper.answer_actual,
                                            self.question_paper.answer_user_remainder,
                                            self.question_paper.answer_actual_remainder if self.question_paper._S =="/" else None,
                                            self.question_paper._S)
            if self.evaluation_result == True:
                if self.question_paper._S == "/":
                    self.evaluation_feedback.config(text=f"Correct!, For {self.question_paper.question}, the Quotient is {self.question_paper.answer_actual} & Remainder is {self.question_paper.answer_actual_remainder}", bg="green")
                else:
                    self.evaluation_feedback.config(text=f"Correct!, {self.question_paper.question} is {self.question_paper.answer_actual}", bg="green")
                self.evaluation_feedback.grid(row=12, column=1, columnspan=8)
                self.exam_score += 1
                if self.sound_variable.get() != "":
                    GUI_Exam.engine.say(self.for_correct_answer())
                    GUI_Exam.engine.runAndWait()
            else:
                if self.attempts_counter == 0:
                    self.evaluation_feedback.config(text="Your Answer is Incorrect, you've got 2 more attempts!", bg="teal")
                    self.evaluation_feedback.grid(row=12, column=1, columnspan=8)
                    self.attempts_counter += 1
                    if self.sound_variable.get() != "":
                        GUI_Exam.engine.say(self.for_incorrect_answer())
                        GUI_Exam.engine.runAndWait()
                elif self.attempts_counter == 1:
                    self.evaluation_feedback.grid_forget()
                    self.evaluation_feedback.config(text="Your Answer is Incorrect, it's the last attempt!", bg="yellow")
                    self.evaluation_feedback.grid(row=12, column=1, columnspan=8)
                    self.attempts_counter += 1
                    if self.sound_variable.get() != "":
                        GUI_Exam.engine.say(self.for_incorrect_answer())
                        GUI_Exam.engine.runAndWait()
                elif self.attempts_counter == 2:
                    self.evaluation_feedback.grid_forget()
                    if self.question_paper._S == "/":
                        self.evaluation_feedback.config(text=f"Incorrect!, For {self.question_paper.question} the Quotient is {self.question_paper.answer_actual} & Remainder is {self.question_paper.answer_actual_remainder} not {self.question_paper.answer_user} & {self.question_paper.answer_user_remainder}", bg="red")
                        if self.sound_variable.get() != "":
                            GUI_Exam.engine.say(f"Incorrect!, For {self.question_paper.question} the Quotient is {self.question_paper.answer_actual} & Remainder is {self.question_paper.answer_actual_remainder}")
                            GUI_Exam.engine.runAndWait()
                    else:
                        self.evaluation_feedback.config(text=f"Incorrect!, {self.question_paper.question} is {self.question_paper.answer_actual} not {self.question_paper.answer_user}", bg="red")
                        if self.sound_variable.get() != "":
                            GUI_Exam.engine.say(f"Incorrect!, {self.question_paper.question} is {self.question_paper.answer_actual} not {self.question_paper.answer_user}")
                            GUI_Exam.engine.runAndWait()
                    self.evaluation_feedback.grid(row=12, column=1, columnspan=8)
                    self.attempts_counter += 1
                    if self.sound_variable.get() != "":
                        GUI_Exam.engine.say(self.for_failed_attempt())
                        GUI_Exam.engine.runAndWait()
        else:
            messagebox.showerror("Input Error", "Please type Numbers only!")
            return

        # Check if all questions have been asked
        if self.question_asked < self.question_to_ask and (self.evaluation_result == True or self.attempts_counter > 2):
            self.store_data()
            self.attempts_counter = 0
            self.generate_question()
        elif self.question_asked <= self.question_to_ask and self.evaluation_result != True and self.attempts_counter <= 2:
            pass
        elif self.question_asked == self.question_to_ask and (self.evaluation_result == True or self.attempts_counter > 2):
            self.store_data()
            self.end_time = datetime.now()
            self.test_end = self.end_time.strftime("%I:%M%p")
            self.launch_result_frame()
        
        # Clear the content of Input Entry Box
        self.input_user_answer.delete(0, END)
        self.input_user_answer_remainder.delete(0, END)

    def launch_result_frame(self):
        """Launch the result screen after completing the exam."""
        self.exam_frame.pack_forget()
        self.result_frame.pack(fill="both", expand=1)
        
        # 3.1 Creating a display for grades
        self.grade.set(get_grade(self.exam_score, self.question_asked))
        self.grade_label.config(text=self.grade.get())
        Label(self.result_frame, width=25, height=3).grid(row=0, column=0, columnspan=5)
        self.grade_label.grid(row=1, column=0, rowspan=3, columnspan=8)

        # 3.2 Creating the exam stat chart
        Label(self.result_frame, width=25, height=10).grid(row=3, column=0, columnspan=5)
        self.stat_frame.grid(row=4, column=0, columnspan=10)
        
        # 3.2.1 Creating test start info
        Label(
        self.stat_frame,
        text=f"Test Date: {self.start_time.strftime('%d-%B-%Y')}\nTest started on: {self.test_start}\nTest ended on: {self.test_end}\nExam Duration: {round((self.end_time - self.start_time).total_seconds()/60, 2)} minutes",
        font=("Bell MT", 16), justify="left"
        ).pack(pady=5)
        Label(
        self.stat_frame,
        text=f"Score: {self.exam_score}\nTotal Questions: {self.question_asked}\nPercent Marks: {round(self.exam_score/self.question_asked*100, 2)}%",
        font=("Bell MT", 16), justify="left"
        ).pack(pady=5)
        
        # 3.2.2 Adding quit button
        Label(self.result_frame, width=25, height=3).grid(row=12, column=0, columnspan=5)
        self.quit_button.grid(row=13, column=0, rowspan=10, columnspan=10)
        
        # 3.2.3 Grades announcment
        if self.sound_variable.get() != "":
            GUI_Exam.engine.say(tell_grade(self.grade.get()))
            GUI_Exam.engine.runAndWait()
        
        self.store_data()
        self.make_pdf()
    
    def for_correct_answer(self):
        """Provide a random message for correct answers."""
        return random.choice([
        "Bingo! You're practically a math magician!",
        "Nailed it! You're as sharp as a ninja star!",
        "Absolutely correct! You're a math superhero in the making!",
        "Epic win! You're the ruler of numbers!",
        "Bravo! You're a math wizard in the making!",
        "Fantastic! You're a superstar!",
        "Hooray! You did it!",
        "Congratulations! You're amazing!",
        "Great job! Keep up the good work!",
        "Wow! You're a champion!",
        "Superb effort! Well done!",
        "Bravo! You're a shining star!",
        "Congratulations on your success!",
        "Awesome work! You're a rockstar!",
        "Hip, hip, hooray! You're a winner!",
        "Well done! You make us proud!",
        "Congratulations! You're on fire!",
        "Incredible! Keep reaching for the stars!",
        "You did it! You're a real trooper!",
        "Cheers to your success! You're awesome!",
        "Woo-hoo! You're a success story!",
        "Way to go! You're a true hero!",
        "Congratulations, superstar! You're unstoppable!",
        "High fives! You're a fantastic friend!",
        "You did it with style! Congratulations!"
    ])
    
    def for_incorrect_answer(self):
        """Provide a random message for incorrect answers."""
        return random.choice([
        "Oopsie-doodle! No worries, superheroes stumble too!",
        "Close, but no cookie this time! You'll get it next round, I believe in you!",
        "Uh-oh! The numbers did a little dance, but don't worry, you'll catch the rhythm next time!",
        "Not quite, but you're on the right track! Keep up the awesome effort!",
        "Almost there! Your brain is flexing its muscles. Let's give it another shot!",
        "No worries! Mistakes help us learn. You've got this!",
        "Oops, that's okay! Keep trying, you'll get it right!",
        "Don't give up! You're getting closer with each attempt.",
        "Learning is an adventure. Keep exploring!",
        "It's okay to make mistakes. You're on the path to success!",
        "Every great scientist started with a few mistakes. You're a little scientist!",
        "Mistakes are proof that you are trying. Keep it up!",
        "You're doing fantastic! Keep going, you'll crack it!",
        "Great effort! You're making progress!",
        "Mistakes are just opportunities to learn something new. Well done!",
        "Keep that positive attitude! You're doing amazing things!",
        "You're a problem-solving champion in the making!",
        "Every mistake is a step closer to success. You're doing great!",
        "Learning is a journey, and you're on the right path!",
        "Believe in yourself! You're capable of incredible things.",
        "It's okay to struggle. That's how we become stronger!",
        "Perseverance is the key to success. You're persevering!",
        "Your efforts are commendable! Keep pushing forward.",
        "You're on a learning adventure! Keep up the good work.",
        "Remember, even the best had to practice. You're doing awesome!"
    ])

    def for_failed_attempt(self):
        """Provide a random message for failed attempts."""
        return random.choice([
        "Phew, tricky one! No worries, every mistake is a chance to learn something new!",
        "Whoa, that one did a little twist! Mistakes happen, but so does progress. Ready for the next adventure?",
        "That was a toughie! Don't worry, you're building a super-strong brain by giving it a workout!",
        "Not this time, but your determination is shining bright! Take a breath, and let's tackle the next challenge together!",
        "Whoopsie-daisy! Even the best explorers take a wrong turn. Shake it off, and let's set sail for the next discovery!",
        "That's okay! Don't worry, you gave it your best shot.",
        "No problem! Mistakes happen. You'll do better next time!",
        "Great effort! Remember, mistakes are stepping stones to success.",
        "You're resilient! Keep a positive attitude for the next challenge.",
        "Well done for trying! Learning is a journey, and you're on it!",
        "Fantastic attempt! Even the experts were once beginners.",
        "You're a superstar! Keep practicing, and you'll master it.",
        "It's okay to feel frustrated. Take a deep breath and try again later!",
        "You're a champion for giving it your all. Keep up the good work!",
        "Every mistake is a lesson learned. You're becoming wiser!",
        "You're on the right track! Keep going, and success will follow.",
        "Mistakes are proof that you're trying. Keep that positive spirit!",
        "You're making progress every day. Celebrate the small victories!",
        "The journey of learning is full of twists and turns. You're doing great!",
        "Perseverance is your superpower! Keep pushing forward.",
        "You've got the courage to face challenges. Keep that bravery!",
        "Your effort is what matters most. Keep up the hard work!",
        "Don't be discouraged! You're growing with every attempt.",
        "Remember, even the strongest heroes faced setbacks. You're a hero!",
        "Believe in yourself! Your potential is limitless."
    ])

    def store_data(self):
        if self.question_asked == 1 and self.test_end == None:
            self.file_open_mode = "w"
        else:
            self.file_open_mode = "a"
        if self.test_end == None:
            a = self.display_question.get()
            b = f"Your Answer: {self.input_user_answer.get()}"
            c = f"Remainder: {self.input_user_answer_remainder.get()}" if self.question_paper._S == "/" else None
            d = f"You answered Correctly in Attempt No.: {self.attempts_counter+1}" if self.attempts_counter < 3 else f"You answered this question incorrectly!"
        else:
            a = f"Score: {self.exam_score}\nTotal Questions: {self.question_asked}\nPercent Marks: {round(self.exam_score/self.question_asked*100, 2)}%.\n{self.grade.get()}"
            b = f"Test Dated: {self.start_time.strftime('%d-%B-%Y')}\nTest Started: {self.test_start}"
            c = f"Test Ended: {self.test_end}"
            d = f"Exam Duration: {round((self.end_time - self.start_time).total_seconds()/60, 2)} minutes"
        with open(f"{self.file_name}.txt", (self.file_open_mode)) as file:
            if a!= None and b==None and c==None and d==None:
                file.write(str(f"{a}\n\n"))
                return
            elif a!= None and b!=None and c==None and d==None:
                file.write(str(f"{a}\n"))
                file.write(str(f"{b}\n\n"))
                return
            elif a!= None and b!=None and c!=None and d==None:
                file.write(str(f"{a}\n"))
                file.write(str(f"{b}\n"))
                file.write(str(f"{c}\n\n"))
                return
            elif a!= None and b!=None and c==None and d!=None:
                file.write(str(f"{a}\n"))
                file.write(str(f"{b}\n"))
                file.write(str(f"{d}\n\n"))
                return
            elif a!= None and b!=None and c!=None and d!=None:
                file.write(str(f"{a}\n"))
                file.write(str(f"{b}\n"))
                file.write(str(f"{c}\n"))
                file.write(str(f"{d}\n\n"))
                return

    def make_pdf(self):
        self.pdf = PDF()
        self.pdf.set_title("Mathematics Practice")
        self.pdf.set_author("Vijendra Singh")
        self.pdf.print_chapter(f"{self.file_name}.txt")
        self.pdf.output(f"Worksheet_{datetime.now().strftime('%d-%b-%y-%I%M')}.pdf")


class PDF(FPDF, GUI_Exam):
    def header(self):
        # Rendering logo:
        self.image("logo_image.jpg", 10, 8, 15)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)
        # Calculating width of title and setting cursor position:
        width = self.get_string_width(self.title) + 6
        self.set_x((210 - width) / 2)
        # Setting colors for frame, background and text:
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Setting thickness of the frame (1 mm)
        self.set_line_width(1)
        # Printing title:
        self.cell(
            width,
            9,
            self.title,
            border=1,
            align="C",
            fill=True,
        )
        # Performing a line break:
        self.ln(15)
    
    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        # Printing page number
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_body(self, filepath):
        # Reading text file:
        with open(f"{root_instance.file_name}.txt", "rb") as fh:
            txt = fh.read().decode("latin-1")
        # Setting font: Times 12
        self.set_font("Times", size=12)
        # Printing justified text:
        self.multi_cell(0, 5, txt)
        # Performing a line break:
        self.ln()
        # Final mention in italics:
        self.set_font("helvetica", "I", 8)
        self.cell(0, 5, "(End of test!)", align="C")

    def print_chapter(self, filepath):
        self.add_page()
        self.chapter_body(filepath)


def main():
    global root_instance
    root_instance = GUI_Exam.launch_main()
    GUI_Exam.root.mainloop()

def get_grade(m, t):
    """
    Calculate the user's grade based on the exam score.

    Parameters:
        - m: User's exam score
        - t: Total number of questions

    Returns:
        - A string representing the user's grade
    """
    score = (m/t)*100
    if score >= 90:
        return("Grade: A")
    elif score >= 80:
        return("Grade: B")
    elif score >= 70:
        return("Grade: C")
    elif score >=60:
        return("Grade: D")
    else:
        return("Grade: F")

def evaluate(answer_user, answer_actual, answer_user_remainder=None, answer_actual_remainder=None, sign=None):
    if sign != "/":
        if answer_user == answer_actual:
            return True
        else:
            return False
    else:
        if answer_user == answer_actual and answer_user_remainder == answer_actual_remainder:
            return True
        else:
            return False

def tell_grade(grade):
    """Provide a random congratulatory message based on the grade."""
    if grade == "Grade: A":
        return random.choice([
    "Fantastic! You've reached Grade A! You're a math wizard in the making!",
    "Incredible job! Grade A is the highest honor, and you've earned it with your exceptional skills.",
    "Wow! You're a mathematical genius! Grade A is a testament to your brilliance.",
    "Amazing! Your Grade A achievement proves that you're a math superhero!",
    "Brilliant work! Grade A means you've mastered the math quest. Keep up the fantastic effort!"
])
    elif grade == "Grade: B":
        return random.choice([
    "Bravo! Grade B is outstanding! Keep up the great work, you're mastering these math challenges!",
    "Impressive! Grade B showcases your dedication to excellence in math.",
    "Well done! Grade B is a mark of your commitment and hard work in the math adventure.",
    "Great job! You've achieved Grade B, and you're on the path to becoming a math star!",
    "Excellent effort! Grade B reflects your strong performance in the math quest. Keep shining!"
])
    elif grade == "Grade: C":
        return random.choice([
    "Congratulations on achieving Grade C! You're doing well, and with a bit more practice, you'll shine even brighter!",
    "Good work! Grade C signifies your steady progress in mastering math skills.",
    "Well deserved! Grade C shows your commitment to learning and improvement.",
    "Thumbs up! Grade C is a positive step, and you're on your way to conquering more math challenges.",
    "Keep it up! Grade C is a commendable achievement, and you're on the right track!"
])
    elif grade == "Grade: D":
        return random.choice([
    "Great effort! Grade D shows progress, and you're on the right track. Keep practicing, and you'll see amazing results!",
    "Well done on achieving Grade D! Your dedication is paying off, and you're improving in math.",
    "Persistence pays off! Grade D acknowledges your hard work and commitment to overcoming math obstacles.",
    "You're getting there! Grade D is a step forward, and you're making strides in the math adventure.",
    "Good job! Grade D recognizes your efforts, and you're making progress in the world of math."
])
    elif grade == "Grade: F":
        return random.choice([
    "No worries! Even superheroes face challenges. Grade F is just a stepping stone. With persistence, you'll conquer every math quest!",
    "Keep going! Grade F is a chance to learn and grow. You'll overcome math challenges with determination.",
    "Every setback is a setup for a comeback! Grade F is a starting point, and you'll rise to new math heights.",
    "Stay positive! Grade F is an opportunity to improve and become an even better math explorer.",
    "You're on a math journey, and Grade F is a part of the adventure. Keep going, and you'll achieve great things!"
])


if __name__ == "__main__":
    main()
