# import pandas as pd
# import os
# from collections import defaultdict
# from random import choice
# from algo.scripts.send_mail import send_clashmail


# from django.db import models
# from algo.models import AllocatedGuide, Student, Guide
# from allocate.models import PreferenceOrder

# def dummy_function(students):
#     """Dummy function to simulate professor allocation."""
#     return choice(students).name if students else None


# def resolve_clash(students, proffesor):
#     student_data = []
#     for student in students:
#         student_data.append([student.name, student.roll_no, str(student.cgpa), str(student.cluster)])

#     return send_clashmail(student_data, proffesor)


# def alloc_algorithm():

#      # Fetch all students from the database
#     all_students = Student.objects.all()
#     allotment_results = []

#     # Process each cluster independently
#     for cluster in Student.objects.values_list('cluster', flat=True).distinct():
#         cluster_students = all_students.filter(cluster=cluster)

#         # Step 1: Allocate based on first preferences
#         visited_professors = set()  # Track visited professors
#         conflicts = defaultdict(list)  # Track conflicts

#         unresolved_students = [s for s in cluster_students if s.allotment_status == 'Pending']

#         for pref_index in range(0, Guide.objects.count()):  # Starting from the second preference
#             new_unresolved_students = []
#             conflicts.clear()  # Clear conflicts for the new preference index

#             for student in unresolved_students:

#                 if pref_index < len(PreferenceOrder.objects.get(student=student).preference_order):
#                     next_pref = PreferenceOrder.objects.get(student=student).preference_order[pref_index]
#                     if next_pref and next_pref not in visited_professors:
#                         conflicts[next_pref].append(student)
#                     else:
#                         new_unresolved_students.append(student)  # Keep unresolved students

#             # Resolve conflicts again
#             for professor, students in conflicts.items():
#                 if len(students) > 1:
#                     #selected_student_name = dummy_function(students)
#                     selected_student_name = resolve_clash(students, professor)
#                     for student in students:
#                         if student.roll_no == selected_student_name:
#                             student.allotment = professor
#                             student.allotment_status = 'Successful'
#                             allotment_results.append(student)
#                             visited_professors.add(professor)
#                         else:
#                             student.allotment_status = 'Pending'
#                             new_unresolved_students.append(student)
#                         student.save()  # Save each student only once

#                 elif len(students) == 1:  # Only one student wants this professor
#                     student = students[0]
#                     student.allotment = professor
#                     student.allotment_status = 'Successful'
#                     visited_professors.add(professor)
#                     student.save()
#                     allotment_results.append(student)

#             unresolved_students = new_unresolved_students  # Update unresolved students

#     # Step 4: Print or log the final allotment results
#     for student in all_students:

        
#         allotted_pair = AllocatedGuide(
#             student=student,
#             guide=Guide.objects.get(guide_id = student.allotment)
#         )
#         allotted_pair.save()
#         print(f"Student {student.name} (Roll No: {student.roll_no}) allocated to {student.allotment} with status {student.allotment_status}")

import pandas as pd
import os
from collections import defaultdict
from random import choice
from algo.scripts.send_mail import send_clashmail
from django.db import models
from algo.models import AllocatedGuide, Student, Guide
from allocate.models import PreferenceOrder

def dummy_function(students):
    """Dummy function to simulate professor allocation."""
    return choice(students).name if students else None

def resolve_clash(students, professor):
    student_data = [[student.name, student.roll_no, str(student.cgpa), str(student.cluster)] for student in students]
    return send_clashmail(student_data, professor)

def alloc_algorithm():
    # Fetch all students from the database
    all_students = Student.objects.all()
    allotment_results = []

    # Process each cluster independently
    for cluster in Student.objects.values_list('cluster', flat=True).distinct():
        cluster_students = all_students.filter(cluster=cluster)

        # Step 1: Allocate based on preferences
        visited_professors = set()  # Track visited professors
        conflicts = defaultdict(list)  # Track conflicts

        unresolved_students = [s for s in cluster_students if s.allotment_status == 'Pending']

        # Fetch all preference orders at once to avoid repeated queries
        preference_orders = {po.student_id: po.preference_order for po in PreferenceOrder.objects.filter(student__in=unresolved_students)}

        for pref_index in range(0, Guide.objects.count()):  # Starting from the first preference
            new_unresolved_students = []
            conflicts.clear()  # Clear conflicts for the new preference index

            for student in unresolved_students:
                preferences = preference_orders.get(student.id, [])
                if pref_index < len(preferences):
                    next_pref = preferences[pref_index]
                    if next_pref and next_pref not in visited_professors:
                        conflicts[next_pref].append(student)
                    else:
                        new_unresolved_students.append(student)  # Keep unresolved students
                else:
                    new_unresolved_students.append(student)  # No more preferences available

            # Resolve conflicts again
            for professor, students in conflicts.items():
                if len(students) > 1:
                    selected_student_name = resolve_clash(students, Guide.objects.get(guide_id=professor).email)
                    for student in students:
                        if student.roll_no == selected_student_name:
                            student.allotment = professor
                            student.allotment_status = 'Successful'
                            allotment_results.append(student)
                            visited_professors.add(professor)
                        else:
                            student.allotment_status = 'Pending'
                            new_unresolved_students.append(student)
                        student.save()

                elif len(students) == 1:  # Only one student wants this professor
                    student = students[0]
                    student.allotment = professor
                    student.allotment_status = 'Successful'
                    visited_professors.add(professor)
                    student.save()
                    allotment_results.append(student)

            unresolved_students = new_unresolved_students  # Update unresolved students

    # Step 4: Save final allotment results
    AllocatedGuide.objects.all().delete()
    for student in all_students:
        if student.allotment:  # Ensure student is allocated
            allocated_pair = AllocatedGuide(
                student=student,
                guide=Guide.objects.get(guide_id=student.allotment)
            )
            allocated_pair.save()
            print(f"Student {student.name} (Roll No: {student.roll_no}) allocated to {student.allotment} with status {student.allotment_status}")

