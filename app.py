from flask import Flask, request, redirect, url_for, render_template, flash
import csv
import os

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        usn = request.form.get("usn").strip().upper()

        if not os.path.exists("marks.csv"):
            flash("Marks file not found. Please wait until it's uploaded.")
            return render_template("home.html")

        with open("marks.csv", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["USN"].strip().upper() == usn:
                    return render_template("result.html", student=row)

        flash("USN not found.")
        return render_template("home.html")

    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'marks_file' not in request.files:
            flash("No file part in the request.")
            return redirect(request.url)

        file = request.files['marks_file']
        if file.filename == '':
            flash("No file selected.")
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            file.save("marks.csv")
            flash("File uploaded successfully.")
            return redirect(url_for("home"))
        
        flash("Please upload a valid CSV file.")
        return redirect(request.url)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
