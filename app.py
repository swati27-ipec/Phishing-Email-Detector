import matplotlib.pyplot as plt
import tkinter as tk
import csv
import os
from datetime import datetime 
from tkinter import filedialog
from detector import detect_phishing

def upload_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "r") as file:
            content = file.read()

        email_box.delete("1.0", tk.END)
        email_box.insert(tk.END, content)

def generate_graph(score):
    plt.figure(figsize=(5, 3))

    plt.bar(["Risk Score"], [score])

    plt.ylim(0, 100)
    plt.ylabel("Score")
    plt.title("Phishing Risk Analysis")

    plt.savefig("graphs/risk_score.png")
    plt.show()

def save_analysis(risk, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("analysis_history.txt", "a") as file:
        file.write(
            f"{timestamp} | Risk: {risk} | Score: {score}\n"
        )

def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("Analysis History")
    history_window.geometry("600x400")

    history_text = tk.Text(history_window)
    history_text.pack(fill="both", expand=True)

    try:
        with open("analysis_history.txt", "r") as file:
            history_text.insert(tk.END, file.read())
    except FileNotFoundError:
        history_text.insert(
            tk.END,
            "No analysis history found."
        )

def export_to_csv(risk, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile("analysis_report.csv")

    with open("analysis_report.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                ["Timestamp", "Risk Level", "Score"]
            )

        writer.writerow(
            [timestamp, risk, score]
        )

def generate_pie_chart():
    import matplotlib.pyplot as plt

    high = 0
    medium = 0
    low = 0

    try:
        with open("analysis_report.csv", "r") as file:
            next(file)

            for line in file:
                if "High Risk" in line:
                    high += 1
                elif "Medium Risk" in line:
                    medium += 1
                elif "Low Risk" in line:
                    low += 1

    except FileNotFoundError:
        return

    labels = ["High", "Medium", "Low"]
    values = [high, medium, low]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Email Risk Distribution")

    plt.savefig("graphs/risk_distribution.png")
    plt.show()

def generate_trend_graph():
    import matplotlib.pyplot as plt
    import csv

    scores = []
    count = []

    try:
        with open("analysis_report.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            index = 1

            for row in reader:
                scores.append(int(row[2]))
                count.append(index)
                index += 1

    except FileNotFoundError:
        return

    plt.figure(figsize=(8, 4))
    plt.plot(count, scores, marker="o")

    plt.xlabel("Analysis Number")
    plt.ylabel("Risk Score")
    plt.title("Risk Score Trend")

    plt.savefig("graphs/risk_trend.png")
    plt.show()

def generate_dashboard(score):
    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.bar(["Risk Score"], [score])
    plt.title("Current Score")

    plt.subplot(1,2,2)
    plt.pie([score, 100-score],
            labels=["Risk","Safe"],
            autopct="%1.1f%%")
    plt.title("Risk Percentage")

    plt.show()
    
def analyze_email():
    email_text = email_box.get("1.0", tk.END)

    risk, score = detect_phishing(email_text)
    save_analysis(risk, score)
    export_to_csv(risk,score)
    generate_dashboard(score)

    if risk == "High Risk":
       result_label.config(
        text=f"Risk Level: {risk}\nScore: {score}",
        fg="red"
      )

    elif risk == "Medium Risk":
         result_label.config(
        text=f"Risk Level: {risk}\nScore: {score}",
        fg="orange"
    )

    else:
        result_label.config(
        text=f"Risk Level: {risk}\nScore: {score}",
        fg="green"
    )

root = tk.Tk()
root.title("Phishing Email Detector")
root.geometry("500x400")

title_label = tk.Label(
    root,
    text="Phishing Email Detector",
    font=("Arial", 16)
)
title_label.pack(pady=10)

email_box = tk.Text(root, height=10, width=50)
email_box.pack(pady=10)

upload_button = tk.Button(
    root,
    text="Upload Email File",
    command=upload_file
)
upload_button.pack(pady=5)

history_button = tk.Button(
    root,
    text="View History",
    command=view_history
)
history_button.pack(pady=5)

dashboard_button = tk.Button(
    root,
    text="Risk Dashboard",
    command=generate_pie_chart
)
dashboard_button.pack(pady=5)

analyze_button = tk.Button(
    root,
    text="Analyze Email",
    command=analyze_email
)
analyze_button.pack(pady=10)

result_label = tk.Label(
    root,
    text="Enter an email and click Analyze",
    font=("Arial", 12)
)
result_label.pack(pady=10)

root.mainloop()