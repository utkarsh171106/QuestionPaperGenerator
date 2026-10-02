from flask import Flask, render_template, request
import os
from docx import Document
from pypdf import PdfReader
import ollama

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html")

@app.route("/upload", methods=["POST"])
def upload():

    subject = request.form["subject"]
    file = request.files["syllabus"]

    if file.filename == "":
        return "No file selected"

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    text = ""

    if file.filename.lower().endswith(".docx"):
        doc = Document(path)

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"

    elif file.filename.lower().endswith(".pdf"):
        reader = PdfReader(path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    else:
        return "Only PDF and DOCX files are allowed"

    return render_template(
        "generate.html",
        subject=subject,
        text=text
    )

@app.route("/generate", methods=["POST"])
def generate():

    subject = request.form["subject"]
    syllabus = request.form["syllabus"]
    questions = request.form["questions"]
    marks = request.form["marks"]
    duration = request.form["duration"]
    difficulty = request.form["difficulty"]
    question_type = request.form["question_type"]

    prompt = f"""
You are a university question paper generator.

Subject: {subject}

Syllabus:
{syllabus}

Generate exactly {questions} questions.

Question Paper Details:
Total Marks: {marks}
Exam Duration: {duration}
Difficulty: {difficulty}
Question Type: {question_type}

Rules:
1. Generate questions ONLY from the provided syllabus.
2. Do not use topics outside the syllabus.
3. Cover different topics from the syllabus.
4. Do not repeat questions.
5. Make questions suitable for a university examination.
6. Number every question.
7. Return ONLY the questions.
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response["message"]["content"]

    return render_template(
        "result.html",
        subject=subject,
        questions=questions,
        marks=marks,
        duration=duration,
        difficulty=difficulty,
        question_type=question_type,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)