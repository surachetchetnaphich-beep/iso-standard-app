import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.document_control.models import (
    StandardType, DocumentCategory, Document, DocumentVersion,
    Department, Employee, Schedule, TrainingRecord
)
from django.contrib.auth import get_user_model

User = get_user_model()

def create_mock_data():
    print("--- Starting Mock Data Generation ---")
    
    # 1. Ensure a Superuser exists
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'is_staff': True, 'is_superuser': True}
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.username}")

    # 2. Departments
    depts_names = ['Production', 'Maintenance', 'Safety & Environment', 'Quality Assurance', 'Human Resources']
    depts = []
    for name in depts_names:
        dept, _ = Department.objects.get_or_create(name=name)
        depts.append(dept)
    print(f"Created {len(depts)} Departments")

    # 3. Employees
    employees = []
    first_names = ['Somsak', 'Wichai', 'Anan', 'Malee', 'Suda', 'Kanya', 'Chai', 'Piti']
    last_names = ['Rakthai', 'Deejai', 'Mungmee', 'Srisuk', 'Rattanapan', 'Wongsuwan', 'Jaidee', 'Thongdee']
    
    for i in range(15):
        emp, _ = Employee.objects.get_or_create(
            employee_id=f"EMP{1000 + i}",
            defaults={
                'first_name': random.choice(first_names),
                'last_name': random.choice(last_names),
                'department': random.choice(depts),
                'position': 'Staff' if i > 5 else 'Senior Staff'
            }
        )
        employees.append(emp)
    print(f"Created {len(employees)} Employees")

    # 4. Standards
    std_names = ['ISO 9001:2015', 'ISO 14001:2015', 'ISO 45001:2018', 'PSM (Process Safety Management)']
    stds = []
    for name in std_names:
        std, _ = StandardType.objects.get_or_create(name=name)
        stds.append(std)
    print(f"Created {len(stds)} Standards")

    # 5. Categories
    cat_data = [
        ('Manual', 'MN'),
        ('Procedure', 'PROC'),
        ('Work Instruction', 'WI'),
        ('Form', 'FORM')
    ]
    cats = []
    for name, code in cat_data:
        cat, _ = DocumentCategory.objects.get_or_create(name=name, code=code)
        cats.append(cat)
    print(f"Created {len(cats)} Categories")

    # 6. Documents & Versions
    docs = []
    doc_titles = [
        'Safety Management Procedure', 'Maintenance Work Instruction', 
        'Quality Control Process', 'Waste Management Policy',
        'Emergency Response Plan', 'Corrective Action Form'
    ]
    
    for i, title in enumerate(doc_titles):
        doc, _ = Document.objects.get_or_create(
            document_number=f"DOC-ISO-{100 + i}",
            defaults={
                'title': title,
                'standard_type': random.choice(stds),
                'category': random.choice(cats),
                'status': 'PUBLISHED',
                'preparer': admin_user,
                'reviewer': admin_user,
                'approver': admin_user,
                'next_review_date': datetime.now().date() + timedelta(days=365)
            }
        )
        docs.append(doc)
        
        # Add a version
        DocumentVersion.objects.get_or_create(
            document=doc,
            version_number='01',
            defaults={
                'file': 'documents/sample.pdf',
                'effective_date': datetime.now().date() - timedelta(days=30),
                'revision_history': 'Initial Release'
            }
        )
    print(f"Created {len(docs)} Documents with Versions")

    # 7. Training Schedules & Records
    activities = [
        ('Internal Audit Training', Schedule.ActivityType.TRAINING),
        ('Annual Safety Review', Schedule.ActivityType.TRAINING),
        ('New WI Implementation', Schedule.ActivityType.TRAINING)
    ]
    
    for i, (title, act_type) in enumerate(activities):
        schedule, _ = Schedule.objects.get_or_create(
            title=title,
            activity_type=act_type,
            defaults={
                'scheduled_date': datetime.now().date() + timedelta(days=(i+1)*5),
                'status': 'PLANNED',
                'responsible_person': 'Safety Manager',
                'standard_type': random.choice(stds)
            }
        )
        
        # Link some documents to this training
        linked_docs = random.sample(docs, 2)
        schedule.documents.set(linked_docs)
        
        # Create Training Records for some employees
        sampled_emps = random.sample(employees, 5)
        for emp in sampled_emps:
            TrainingRecord.objects.get_or_create(
                schedule=schedule,
                employee=emp,
                defaults={
                    'is_attended': True,
                    'result': 'PASS' if random.random() > 0.2 else 'FAIL',
                    'score': random.randint(70, 100)
                }
            )
    
    print(f"Created {len(activities)} Schedules with Training Records")
    print("--- Mock Data Generation Completed Successfully ---")

if __name__ == '__main__':
    create_mock_data()
