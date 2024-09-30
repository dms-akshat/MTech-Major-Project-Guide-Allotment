# views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Student, Guide, PreferenceOrder, AllocatedGuide
from django.forms.models import model_to_dict

def check_eligibility(request,student_id):
    try:
        # Continue processing with the student object
        student = Student.objects.get(student_id=student_id)
        #To check if guide has been alloted
        exist_guide = AllocatedGuide.objects.filter(student=student)
        if not exist_guide.exists():
            #To fill preference order
            return redirect('fill_preference_order', student_id=student_id)
            #To connect with frontend, the following JsonResponse will be sent
            # return JsonResponse({'allocated':'false'})
        else:
            # return render(request, 'allocate/not_eligible.html')
            allocated_guide = AllocatedGuide.objects.get(student=student)
            #To connect with frontend, the following JsonResponse will be sent

            allocated_guide_data = model_to_dict(allocated_guide)
            return JsonResponse({
                'allocated':'true',
                'allocated_guide': allocated_guide_data
            })
            # return render(request, 'allocate/show_allocated_guide.html', {'guide': allocated_guide.guide})
        
    except Student.DoesNotExist:
        return HttpResponse(f"No student found with ID {student_id}", status=404)
    
def fill_preference_order(request, student_id):
    """
    Handles the submission of a student's guide preference order.
    This view retrieves the student and all available guides. If the request method is POST,
    it processes the submitted preference order, sorts it, and saves it to the database.
    If a preference order already exists for the student, it is deleted before saving the new one.
    Args:
        request (HttpRequest): The HTTP request object.
        student_id (int): The ID of the student submitting their preference order.
    Returns:
        JsonResponse: A JSON response indicating the status of the operation and the saved preference order if successful.
        HttpResponse: Renders the preference order form template if the request method is GET.
    Template:
        allocate/fill_preference_order.html: The template for submitting the preference order.
    Context:
        guides (QuerySet): A queryset of all Guide objects.
        range (range): A range object from 1 to the number of guides + 1.
    """
    student = Student.objects.get(student_id=student_id)
    guides = Guide.objects.all()

    if request.method == "POST":
        preference_order = []
        preference_set = set()
        for guide in guides:
            preference = request.POST.get(f'preference_{guide.guide_id}')
            if preference:
                try:
                    preference_value = int(preference)
                    # Check if the preference is already used (no duplicates)
                    if preference_value in preference_set:
                        return JsonResponse({'status': 'error', 'message': f'Duplicate preference value {preference_value} for guide {guide.guide_id}'})
                    # Add the preference to the list and the set
                    preference_order.append((preference_value, guide.guide_id))
                    preference_set.add(preference_value)
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': f'Invalid preference value for guide {guide.guide_id}'})
            else:
                return JsonResponse({'status': 'error', 'message': f'Preference missing for guide {guide.guide_id}'})

    
        if len(preference_order) != len(guides):
            return JsonResponse({'status': 'error', 'message': 'Preference order cannot be empty'})

        # Sort by preference number
        preference_order.sort(key=lambda x: x[0])
        
        # Extract only the ordered guide IDs
        ordered_guides = [guide_id for _, guide_id in preference_order]

        # Check if a preference order already exists for the student
        existing_preference_order = PreferenceOrder.objects.filter(student=student)
        if existing_preference_order.exists():
            # Delete the existing preference order
            existing_preference_order.delete()

        # Save the new preference order
        PreferenceOrder.objects.create(
            student=student,
            preference_order=ordered_guides  # Save as a list in JSONField
        )
        
        return JsonResponse({'status': 'success','preference_order':preference_order})
        # else:
        # return JsonResponse({'status': 'failure'}, status=400)
        # return redirect('show_allocated_guide',student_id=student_id)  # Redirect to a success page after saving
    
    return render(request, 'allocate/fill_preference_order.html', {
        'guides': guides,
        'range': range(1, guides.count() + 1)
    })


def show_allocated_guide(request, student_id):
    """
    View function to display the allocated guide for a given student.

    Args:
        request (HttpRequest): The HTTP request object.
        student_id (int): The ID of the student whose allocated guide is to be displayed.

    Returns:
        HttpResponse: The rendered HTML page displaying the allocated guide for the student.
    """
    req_student = Student.objects.get(student_id=student_id)
    allocated_guide = AllocatedGuide.objects.get(student=req_student)
    return render(request, 'allocate/show_allocated_guide.html', {'guide': allocated_guide.guide})
