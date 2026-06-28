from django.shortcuts import render
from django.http import HttpResponse
from CalucaltorApp.forms import CaluclatorForm


# Create your views here.
def calculator_view(request):
    # 1. Initialize the form
    form = CaluclatorForm()
    total = None # Initialize total variable for the context

    # 2. Check if the form was submitted (POST request)
    if request.method == 'POST':
        # Bind the form to the submitted data
        form = CaluclatorForm(request.POST)
        
        # 3. Validate the form data
        if form.is_valid():
            # Get the clean data from the form
            num1 = form.cleaned_data['num1']
            num2 = form.cleaned_data['num2']
            
            # Calculate the result
            total = num1 + num2
            
    # 4. Pass the form and the result to the template
    context = {
        'form': form,
        'total': total,
    }
    return render(request, 'CaluclatorApp/calcy.html', context)
