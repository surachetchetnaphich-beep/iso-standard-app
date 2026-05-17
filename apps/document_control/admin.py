from django.contrib import admin
from django.utils.html import format_html
from .models import (
    StandardType, DocumentCategory, Document, DocumentVersion, 
    Schedule, ScheduleAttachment, Department, Employee, TrainingRecord
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'department', 'position')
    list_filter = ('department',)
    search_fields = ('employee_id', 'first_name', 'last_name')

class TrainingRecordInline(admin.TabularInline):
    model = TrainingRecord
    extra = 3
    autocomplete_fields = ('employee',)

@admin.register(StandardType)
class StandardTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion
    extra = 1

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'title', 'standard_type', 'category', 'status', 'next_review_date')
    list_filter = ('status', 'standard_type', 'category', 'site')
    search_fields = ('document_number', 'title')
    autocomplete_fields = ('preparer', 'reviewer', 'approver')
    inlines = [DocumentVersionInline]
    date_hierarchy = 'next_review_date'

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'effective_date', 'file_link')
    list_filter = ('effective_date',)
    search_fields = ('document__document_number', 'version_number')

    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_link.short_description = "Attachment"

class ScheduleAttachmentInline(admin.TabularInline):
    model = ScheduleAttachment
    extra = 1

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity_type', 'standard_type', 'scheduled_date', 'status', 'responsible_person')
    list_filter = ('activity_type', 'standard_type', 'status', 'scheduled_date')
    search_fields = ('title', 'responsible_person')
    filter_horizontal = ('documents',)
    inlines = [ScheduleAttachmentInline, TrainingRecordInline]
    date_hierarchy = 'scheduled_date'

@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'schedule', 'is_attended', 'result', 'score')
    list_filter = ('is_attended', 'result', 'schedule__scheduled_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'schedule__title')

@admin.register(ScheduleAttachment)
class ScheduleAttachmentAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'file', 'description', 'created_at')
