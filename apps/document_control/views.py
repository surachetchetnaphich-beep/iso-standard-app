from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from .models import Document, StandardType, DocumentCategory, Schedule, Employee, TrainingRecord

def dashboard(request):
    """
    Landing Page / Dashboard with Search and Scheduling
    """
    query = request.GET.get('q')
    search_results = Document.objects.none()
    schedule_results = Schedule.objects.none()
    employee_results = Employee.objects.none()

    try:
        if query:
            # Search Documents
            search_results = Document.objects.filter(
                Q(title__icontains=query) | Q(document_number__icontains=query)
            ).order_by('-updated_at').distinct()

            # Search Schedules
            schedule_results = Schedule.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(documents__title__icontains=query) |
                Q(documents__document_number__icontains=query)
            ).order_by('-scheduled_date').distinct()

            # Search Employees
            employee_results = Employee.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(employee_id__icontains=query) |
                Q(department__name__icontains=query)
            ).order_by('first_name').distinct()

        context = {
            'total_docs': Document.objects.count(),
            'standards': StandardType.objects.all(),
            'categories': DocumentCategory.objects.all(),
            'recent_docs': Document.objects.order_by('-updated_at')[:5],
            'pending_review': Document.objects.filter(status='REVIEW').count(),
            'total_employees': Employee.objects.count(),
            'upcoming_schedules': Schedule.objects.filter(
                scheduled_date__gte=timezone.now().date(),
                status='PLANNED'
            ).order_by('scheduled_date')[:5],
            'query': query,
            'search_results': search_results,
            'schedule_results': schedule_results,
            'employee_results': employee_results,
        }
    except Exception as e:
        # Fallback for empty database or migration issues during initial setup
        context = {
            'total_docs': 0,
            'standards': [],
            'categories': [],
            'recent_docs': [],
            'pending_review': 0,
            'total_employees': 0,
            'upcoming_schedules': [],
            'query': query,
            'search_results': [],
            'schedule_results': [],
            'employee_results': [],
            'error': str(e)
        }
    return render(request, 'document_control/dashboard.html', context)

