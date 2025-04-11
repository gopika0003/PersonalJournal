from django.shortcuts import render, redirect, get_object_or_404
from .forms import JournalEntryForm
from .models import JournalEntry
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Dashboard View
@login_required
def dashboard(request):
    return render(request, 'authentication/dashboard.html')


# New Entry Page
@login_required
def new_entry(request):
    success = False  # Flag to show success message

    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            success = True
            form = JournalEntryForm(initial={'content': 'DEAR DIARY, '})
    else:
        form = JournalEntryForm(initial={'content': 'DEAR DIARY, '})

    return render(request, 'entry.html', {'form': form, 'success': success})


# View All Entries (with optional date filtering)
@login_required
def view_page(request):
    selected_date = request.GET.get('date')
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    if selected_date:
        entries = entries.filter(created_at__date=selected_date)

    edit_entry_id = request.GET.get('edit')
    edit_form = None

    if edit_entry_id:
        entry_to_edit = get_object_or_404(JournalEntry, id=edit_entry_id, user=request.user)
        edit_form = JournalEntryForm(instance=entry_to_edit)

    if request.method == 'POST' and 'save_edit' in request.POST:
        entry_id = request.POST.get('entry_id')
        entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('view_entries')

    return render(request, 'view.html', {
        'entries': entries,
        'edit_entry_id': int(edit_entry_id) if edit_entry_id else None,
        'edit_form': edit_form
    })


# Read a Single Entry (view or edit)
@login_required
def read_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        entry.title = request.POST.get('title')
        entry.content = request.POST.get('content')
        entry.save()
        return redirect('view_entries')

    editable = request.GET.get('edit') == 'true'
    return render(request, 'read.html', {
        'entry': entry,
        'editable': editable
    })


# Delete Entry
@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
    return redirect('view_entries')


# Toggle Favorite
@login_required
def toggle_favorite(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.is_favorite = not entry.is_favorite
        entry.save()
    return redirect('view_entries')


# View Favorite Entries Only
@login_required
def favorite_entries(request):
    entries = JournalEntry.objects.filter(user=request.user, is_favorite=True).order_by('-created_at')
    return render(request, 'favorites.html', {'entries': entries})
