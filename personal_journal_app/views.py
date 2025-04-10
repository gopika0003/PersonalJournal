from django.shortcuts import render, redirect
from .forms import JournalEntryForm
from .models import JournalEntry
from django.contrib.auth.decorators import login_required

# New Entry Page
@login_required
def dashboard(request):
    return render(request, 'authentication/dashboard.html')

def new_entry(request):
    success = False  # Flag to show the success message

    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            success = True  # Mark save success to show message

            # Reinitialize form with default content
            form = JournalEntryForm(initial={'content': 'DEAR DIARY, '})

    else:
        form = JournalEntryForm(initial={'content': 'DEAR DIARY, '})

    return render(request, 'entry.html', {'form': form, 'success': success})

def view_page(request):
    return render(request, 'view.html')


