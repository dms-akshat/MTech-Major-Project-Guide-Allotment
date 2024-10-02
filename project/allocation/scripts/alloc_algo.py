import pandas as pd
import os
from collections import defaultdict
from random import choice
from allocation.scripts.send_mail import send_clashmail


from django.db import models
from allocation.models import Student

def dummy_function(students):
    """Dummy function to simulate professor allocation."""
    return choice(students).name if students else None


def resolve_clash(students, proffesor):
    student_data = []
    for student in students:
        student_data.append([student.name, student.roll_no, str(student.cgpa), str(student.cluster)])

    return send_clashmail(student_data, proffesor)


def alloc_algorithm():
    # Load the Excel file
    file_path = os.path.join(os.path.dirname(__file__), 'preference.xlsx')

    # Define the column names
    column_names = [
        'Sl No.', 'Roll_No', 'Name', 'Major_CGPA', 'Pref_1', 'Pref_2', 'Pref_3', 'Pref_4', 'Pref_5', 
        'Pref_6', 'Pref_7', 'Pref_8', 'Pref_9', 'Pref_10', 'Pref_11', 'Pref_12', 'Pref_13', 'Pref_14'
    ]

    # Read the Excel file to identify sheet names
    excel_data = pd.ExcelFile(file_path)

    # Load the "Student Preference List" sheet if it exists
    if "Student Preference List" in excel_data.sheet_names:
        student_preference_data = excel_data.parse("Student Preference List", header=None, names=column_names)

        # Add a Cluster column with initial value 1
        student_preference_data['Cluster'] = 1
        cluster_counter = 0

        # Process the DataFrame to increment the Cluster value
        for index, row in student_preference_data.iterrows():
            if isinstance(row['Sl No.'], str) and len(row['Sl No.'].split()) > 1 and row['Sl No.'].split()[1] == "Cluster":
                cluster_counter += 1
                student_preference_data.drop(index, inplace=True)  
            elif pd.isna(row['Sl No.']) or not isinstance(row['Sl No.'], (int, float)) or row['Sl No.'] != int(row['Sl No.']):
                student_preference_data.drop(index, inplace=True)  # Drop invalid rows
            else:
                student_preference_data.at[index, 'Cluster'] = cluster_counter

        student_preference_data.reset_index(drop=True, inplace=True)

        # Create Student instances
        for index, row in student_preference_data.iterrows():
            preferences = [
                row[f'Pref_{i}'].strip() for i in range(1, 15)
            ]

            student = Student(
                name=row['Name'].strip(),
                roll_no=row['Roll_No'].strip(),
                cgpa=row['Major_CGPA'],
                pref_queue=preferences,
                cluster=row['Cluster'],
                allotment_status='Pending',
                allotment=''
            )
            student.save()

     # Fetch all students from the database
    all_students = Student.objects.all()
    allotment_results = []

    # Process each cluster independently
    for cluster in Student.objects.values_list('cluster', flat=True).distinct():
        cluster_students = all_students.filter(cluster=cluster)

        # Step 1: Allocate based on first preferences
        visited_professors = set()  # Track visited professors
        conflicts = defaultdict(list)  # Track conflicts

        unresolved_students = [s for s in cluster_students if s.allotment_status == 'Pending']

        for pref_index in range(0, 14):  # Starting from the second preference
            new_unresolved_students = []
            conflicts.clear()  # Clear conflicts for the new preference index

            for student in unresolved_students:
                if pref_index < len(student.pref_queue):
                    next_pref = student.pref_queue[pref_index]
                    if next_pref and next_pref not in visited_professors:
                        conflicts[next_pref].append(student)
                    else:
                        new_unresolved_students.append(student)  # Keep unresolved students

            # Resolve conflicts again
            for professor, students in conflicts.items():
                if len(students) > 1:
                    #selected_student_name = dummy_function(students)
                    selected_student_name = resolve_clash(students, professor)
                    for student in students:
                        if student.roll_no == selected_student_name:
                            student.allotment = professor
                            student.allotment_status = 'Successful'
                            allotment_results.append(student)
                            visited_professors.add(professor)
                        else:
                            student.allotment_status = 'Pending'
                            new_unresolved_students.append(student)
                        student.save()  # Save each student only once

                elif len(students) == 1:  # Only one student wants this professor
                    student = students[0]
                    student.allotment = professor
                    student.allotment_status = 'Successful'
                    visited_professors.add(professor)
                    student.save()
                    allotment_results.append(student)

            unresolved_students = new_unresolved_students  # Update unresolved students

    # Step 4: Print or log the final allotment results
    for student in all_students:
        print(f"Student {student.name} (Roll No: {student.roll_no}) allocated to {student.allotment} with status {student.allotment_status}")