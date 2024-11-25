from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Control, Cycle, Validation, DesignAnswer, DesignQuestion
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

class CustomLoginView(auth_views.LoginView):
    template_name = 'audit/login.html'  # Use the custom template
    form_class = CustomLoginForm  # Use the custom form

    def form_valid(self, form):
        # Get the selected cycle from the form
        cycle = form.cleaned_data.get('cycle')
        # Store the cycle ID in the session
        self.request.session['selected_cycle_id'] = cycle.id  # Store the cycle ID in the session
        
        # Print for debugging
        print(f"Cycle selected: {cycle.id}")
        
        # Call the parent class's form_valid to complete the login
        return super().form_valid(form)

@login_required
def get_assigned_controls(request):
    controls = Control.objects.filter(assigned_auditor=request.user)
    data = [{'id': c.id, 'name': c.name, 'description': c.description} for c in controls]
    return JsonResponse({'controls': data})

@login_required
def assigned_controls(request):
    controls = Control.objects.filter(assigned_auditor=request.user)
    return JsonResponse({'controls': list(controls.values())})


@login_required
def dashboard(request):
    # Get the selected cycle from session (assuming it is stored after login)
    cycle_id = request.session.get('selected_cycle_id')

    if not cycle_id:
        # If no cycle is selected, set a default message or show an error
        return render(request, 'audit/dashboard.html', {
            'error_message': "No cycle selected. Please select a cycle first."
        })

    # Get the cycle object using the cycle_id
    cycle = get_object_or_404(Cycle, id=cycle_id)

    # Get controls assigned to the user for the selected cycle
    controls = Control.objects.filter(assigned_auditor=request.user, cycle=cycle)
    
    # Get all available cycles for the user to select
    cycles = Cycle.objects.all()

    return render(request, 'audit/dashboard.html', {
        'controls': controls,
        'cycles': cycles,
        'selected_cycle': cycle,  # Pass the cycle object to the template
        'user_name': request.user.username,  # Display logged-in user's name
    })


def validation_evaluation(request, pk):
    validation = get_object_or_404(Validation, pk=pk)
    # Your logic for evaluating the design
    return render(request, 'validation_evaluation.html', {'validation': validation})

def validation_review(request, pk):
    validation = get_object_or_404(Validation, pk=pk)
    # Your logic for reviewing EFI
    return render(request, 'validation_review.html', {'validation': validation})

def validation_operational(request, pk):
    validation = get_object_or_404(Validation, pk=pk)
    # Your logic for operational evaluation
    return render(request, 'validation_operational.html', {'validation': validation})


def control_header(request, control_id):
    control = get_object_or_404(Control, pk=control_id)

    if request.method == 'POST':
        # Update control fields with the user input
        control.date_elaborated = request.POST.get('fecha_elaboracion')
        control.status = request.POST.get('estado')
        control.total_hours = request.POST.get('total_horas')
        control.consulted_resources = request.POST.get('recursos')

        # Save the changes
        control.save()

        return redirect('control_header', control_id=control.id)  

    context = {
        'control': control
    }
    return render(request, 'audit/control_header.html', context)

@login_required
def control_design(request, control_id):
    control = get_object_or_404(Control, pk=control_id)
    questions = control.questions.all()

    # Retrieve existing answers for the current control
    existing_answers = DesignAnswer.objects.filter(question__control=control)

    # Retrieve existing Validation object for the current control
    validation = Validation.objects.filter(control=control).first()

    # Handle POST request (saving new answers)
    if request.method == 'POST':
        # Collect values for date_elaborated, person_name, and person_role
        date_elaborated = request.POST.get('date_elaborated')
        person_name = request.POST.get('person_name')
        person_role = request.POST.get('person_role')

        # Initialize variables to track answers
        all_answered = True
        all_positive = True
        total_questions = len(questions)

        for question in questions:
            response = request.POST.get(f'response_{question.id}')
            explanation = request.POST.get(f'explanation_{question.id}')

            # Check if all questions are answered
            if not response:
                all_answered = False
            if response != 'Sí':  # If any answer is not "Sí", set all_positive to False
                all_positive = False

            # Create or update the DesignAnswer object
            design_answer, created = DesignAnswer.objects.update_or_create(
                question=question,
                defaults={'answer': response, 'explanation': explanation},
            )

        # If all questions are answered, update control status to "Terminado"
        if all_answered:
            control.status = 'Terminado'
        else:
            control.status = 'En proceso'

        # Save control status
        control.save()

        # Update or create the Validation object for the Control
        validation, validation_created = Validation.objects.update_or_create(
            control=control,  # link Validation to the Control object
            defaults={
                'date_elaborated': date_elaborated,
                'person_name': person_name,
                'person_role': person_role,
            },
        )

        # If all answers are positive ("Sí"), set design score to 100
        if all_positive:
            validation.design_score = 100
            validation.status = 'Satisfactorio'
        else:
            # If some answers are negative, set design score based on logic (could be less than 100)
            validation.design_score = (total_questions - 1) * 100 // total_questions  # Example formula
            validation.status = 'Insatisfactorio'

        validation.save()

        return redirect('dashboard')  # Redirect after saving

    # Pass the existing validation data to the template
    return render(request, 'audit/control_design.html', {
        'control': control,
        'questions': questions,
        'existing_answers': existing_answers,
        'validation': validation,  # Pass existing validation to the template
    })
