from flask import Flask, request, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

def process_file(input_file_path):
    # Reading the input file
    input_data = pd.read_excel(input_file_path, sheet_name='Sheet1')

    max_marks = input_data.iloc[0, 2:].astype(float).to_dict()
    weightage = input_data.iloc[1, 2:].astype(float).to_dict()

    student_data = input_data.iloc[2:].reset_index(drop=True)
    for column in student_data.columns[2:]:
        student_data[column] = pd.to_numeric(student_data[column], errors='coerce')

    def calculate_weighted_score(row):
        total = 0
        for exam, weight in weightage.items():
            if exam in max_marks and max_marks[exam] != 0:
                scaled_score = (row[exam] / max_marks[exam]) * weight
                total += scaled_score
        return round(total, 2)

    student_data['Grand Total/100'] = student_data.apply(calculate_weighted_score, axis=1)

    grade_sorted_df = student_data.sort_values(by='Grand Total/100', ascending=False).reset_index(drop=True)
    roll_sorted_df = student_data.sort_values(by='Roll').reset_index(drop=True)

    iapc_reco_percentages = {
        'AA': 5,
        'AB': 15,
        'BB': 25,
        'BC': 25,
        'CC': 15,
        'CD': 10,
        'DD': 5
    }

    num_students = len(student_data)
    iapc_reco_counts = {grade: round(num_students * pct / 100) for grade, pct in iapc_reco_percentages.items()}
    total_allocated = sum(iapc_reco_counts.values())
    if total_allocated != num_students:
        largest_grade = max(iapc_reco_counts, key=iapc_reco_counts.get)
        iapc_reco_counts[largest_grade] += num_students - total_allocated

    def assign_grades(sorted_df, grade_counts):
        grades = []
        for grade, count in grade_counts.items():
            grades.extend([grade] * count)
        sorted_df['Grade'] = grades[:len(sorted_df)]
        return sorted_df

    grade_sorted_df = assign_grades(grade_sorted_df, iapc_reco_counts)

    roll_sorted_df = roll_sorted_df.merge(grade_sorted_df[['Roll', 'Grade']], on='Roll', how='left')

    summary_data = pd.DataFrame({
        'Grade': list(iapc_reco_counts.keys()),
        'Old IAPC Reco': list(iapc_reco_percentages.values()),
        'Counts': list(iapc_reco_counts.values()),
        'Round': [round(iapc_reco_counts[grade]) for grade in iapc_reco_counts.keys()],
        'Count verified': list(iapc_reco_counts.values())
    })
    while len(summary_data) < 12:
        summary_data = pd.concat([summary_data, pd.DataFrame([[None] * 5], columns=summary_data.columns)], ignore_index=True)

    output_path = "Output-1.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        grade_sorted_df.to_excel(writer, sheet_name='Sheet1_Grade_Sorted', index=False, startrow=2)
        summary_data.to_excel(writer, sheet_name='Sheet1_Grade_Sorted', index=False, startcol=9, startrow=2)

        roll_sorted_df.to_excel(writer, sheet_name='Sheet2_Roll_Sorted', index=False, startrow=2)
        summary_data.to_excel(writer, sheet_name='Sheet2_Roll_Sorted', index=False, startcol=9, startrow=2)

    return output_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file:
            input_file_path = "uploaded_file.xlsx"
            file.save(input_file_path)
            output_file_path = process_file(input_file_path)
            return send_file(output_file_path, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
