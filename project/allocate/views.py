from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import datetime
from .models import Student, Guide, PreferenceOrder, AllocatedGuide
from my_admin_app.models import Date

def check_eligibility(request, email):
    # Get the student object or return a 404 error if not found
    student = get_object_or_404(Student, email=email)
    # Check if a guide has been allocated
    exist_guide = AllocatedGuide.objects.filter(student=student)
    date = Date.objects.first()
    start_date = date.start_date
    end_date = date.end_date
    current_date = datetime.date.today()

    if current_date>=start_date and current_date<=end_date and PreferenceOrder.objects.filter(student=student).exists():
        
        # Redirect to fill the preference order if no guide is allocated
        return redirect('preference_filled', email=email)
    
    if current_date<start_date:
        messages.error(request, "Allotment yet to start.")
        return redirect('student_page',email=email)
    
    if current_date>end_date:
        return redirect('show_allocated_guide',email=email)
    
    if not exist_guide.exists():
        # Set a message indicating that the preference order needs to be filled
        messages.info(request, "You have not filled your preference order yet. Please fill it now.")
        
        # Redirect to fill the preference order if no guide is allocated
        return redirect('fill_preference_order', email=email)
    
    # If a guide is allocated, render the template for showing the allocated guide
    allocated_guide = exist_guide.first()  # Use first() to avoid multiple queries
    return render(request, 'allocate/show_allocated_guide.html', {
        'guide': allocated_guide.guide,
        'email': email  # Corrected the key name to match
    })

def fill_preference_order(request, email):
    student = get_object_or_404(Student, email=email)
    guides = Guide.objects.all()

    if request.method == "POST":
        preference_order = []
        preference_set = set()

        for guide in guides:
            preference = request.POST.get(f'preference_{guide.guide_id}')
            if preference:
                try:
                    preference_value = int(preference)
                    if preference_value in preference_set:
                        return render(request, 'allocate/fill_preference_order.html', {
                            'guides': guides,
                            'range': range(1, guides.count() + 1),
                            'error_message': f'Duplicate preference value {preference_value} for guide {guide.guide_id}'
                        })
                    preference_order.append((preference_value, guide.guide_id))
                    preference_set.add(preference_value)
                except ValueError:
                    return render(request, 'allocate/fill_preference_order.html', {
                        'guides': guides,
                        'range': range(1, guides.count() + 1),
                        'error_message': f'Invalid preference value for guide {guide.guide_id}'
                    })
            else:
                return render(request, 'allocate/fill_preference_order.html', {
                    'guides': guides,
                    'range': range(1, guides.count() + 1),
                    'error_message': f'Preference missing for guide {guide.guide_id}'
                })

        if len(preference_order) != len(guides):
            return render(request, 'allocate/fill_preference_order.html', {
                'guides': guides,
                'range': range(1, guides.count() + 1),
                'error_message': 'Preference order cannot be empty'
            })

        # Sort by preference number
        preference_order.sort(key=lambda x: x[0])
        ordered_guides = [guide_id for _, guide_id in preference_order]

        # Check if a preference order already exists for the student
        existing_preference_order = PreferenceOrder.objects.filter(student=student)
        if existing_preference_order.exists():
            existing_preference_order.delete()

        # Save the new preference order
        PreferenceOrder.objects.create(
            student=student,
            preference_order=ordered_guides  # Save as a list in JSONField
        )

        return redirect('show_allocated_guide', email=email)  # Redirect to show allocated guide

    return render(request, 'allocate/fill_preference_order.html', {
        'guides': guides,
        'range': range(1, guides.count() + 1)
    })

def show_allocated_guide(request, email):
    req_student = get_object_or_404(Student, email=email)
    allocated_guide = AllocatedGuide.objects.filter(student=req_student).first()
    if allocated_guide is None:
        # Redirect to fill preference order page if no guide has been allocated
        return render(request, 'allocate/show_allocated_guide.html', {
            'guide':None,
            'email': email
        })
    return render(request, 'allocate/show_allocated_guide.html', {'guide': allocated_guide.guide,'email':email})

def preference_filled(request, email):
    return render(request, 'allocate/preference_filled_no_guide_yet.html', {
        'email': email,
    })
