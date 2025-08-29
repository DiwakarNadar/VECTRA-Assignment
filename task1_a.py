import pandas as pd
import numpy as np

# Step 0: Create student data and save
students = {
    "ID": [101, 102, 103, 104, 105, 106, 107],
    "Name": ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace"],
    "Math": [95, 72, 88, 55, 80, 99, 68],
    "Physics": [89, 65, 91, 62, 77, 95, 72],
    "Chemistry": [92, 70, 85, 58, 79, 97, 74],
    "Biology": [88, 60, 90, 61, 83, 96, 70]
}

df = pd.DataFrame(students)
df.to_excel("student.xlsx", index=False)

# Step 1: Read data
df = pd.read_excel("student.xlsx")

# Step 2: Compute total, average, grade
subs = ["Math", "Physics", "Chemistry", "Biology"]

df["Total"] = df[subs].sum(axis=1)
df["Avg"] = df[subs].mean(axis=1)

conds = [
    df["Avg"] >= 90,
    df["Avg"] >= 75,
    df["Avg"] >= 60
]
grades = ["A", "B", "C"]
df["Grade"] = np.select(conds, grades, default="F")

# Step 3: Top 3 in each subject
top_rows = []
for sub in subs:
    top3 = df.nlargest(3, sub)[["ID", "Name", sub]].copy()
    top3["Subject"] = sub
    top3.rename(columns={sub: "Marks"}, inplace=True)
    top_rows.append(top3)

top_df = pd.concat(top_rows, ignore_index=True)
top_df = top_df[["Subject", "ID", "Name", "Marks"]]

# Step 4: Subject averages
avg_marks = df[subs].mean()

# Step 5: Save everything to Excel
with pd.ExcelWriter("results.xlsx", engine="xlsxwriter") as writer:
    df[["ID", "Name", "Total", "Avg", "Grade"]].to_excel(writer, sheet_name="Summary", index=False)
    top_df.to_excel(writer, sheet_name="Top Performers", index=False)

    book = writer.book
    sheet = book.add_worksheet("Chart")
    writer.sheets["Chart"] = sheet

    sheet.write_column("A2", avg_marks.index)
    sheet.write_column("B2", avg_marks.values)

    chart = book.add_chart({"type": "column"})
    chart.add_series({
        "name": "Average Marks",
        "categories": ["Chart", 1, 0, len(avg_marks), 0],
        "values": ["Chart", 1, 1, len(avg_marks), 1]
    })
    chart.set_title({"name": "Average Marks per Subject"})
    chart.set_x_axis({"name": "Subjects"})
    chart.set_y_axis({"name": "Average Marks"})
    sheet.insert_chart("D2", chart)

print("✅ results.xlsx created!")
