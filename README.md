# MathQuest Adventures

MathQuest Adventures is a Python GUI application for practicing basic arithmetic skills. It lets users select the types of questions (addition, subtraction, multiplication, division and fractions), specify how many to attempt and provides instant feedback. The app can speak results using `pyttsx3` with a more natural sounding voice and will create a text log and optional PDF report of your session.

## Requirements
- Python 3
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [fpdf](https://pypi.org/project/fpdf/)
- tkinter (bundled with most Python installations)

Install the required packages with pip:

```bash
pip install pyttsx3 fpdf
```

## Running the application
Launch the exam interface with:

```bash
python project.py
```

Select your desired operations, choose a difficulty level (Easy, Medium or Hard) and specify the number of questions, then start the exam. Available modes include basic arithmetic, fractions, prime factorization, HCF and the new **LCM** practice. After completion you can save a PDF report summarizing your results. A checkbox labeled **Factors & Prime Count** enables quiz questions that ask how many factors a given number has, reporting whether it is prime or composite.

## Repository contents
- `project.py` – main program containing the GUI and quiz logic.
- `logo_image.jpg` – logo used when generating PDF reports.
- Text files named `Practice_dated_<timestamp>.txt` and PDF files `Worksheet_<timestamp>.pdf` may be generated when you run the program; these are not stored in version control.

## License
This project is provided as-is for educational purposes.
