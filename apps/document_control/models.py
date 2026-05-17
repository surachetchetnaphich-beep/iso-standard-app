import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def document_upload_path(instance, filename):
    # Upload path format: media/documents/<document_number>/v<version>/filename
    return os.path.join(
        'documents', 
        str(instance.document.document_number), 
        f"v{instance.version_number}", 
        filename
    )

def schedule_upload_path(instance, filename):
    # Upload path format: media/schedules/activity_<id>/filename
    return os.path.join(
        'schedules', 
        f"activity_{instance.schedule.id}", 
        filename
    )

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StandardType(TimeStampedModel):
    name = models.CharField(_("ชื่อมาตรฐาน"), max_length=100, unique=True)
    description = models.TextField(_("รายละเอียด"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("ระบบมาตรฐาน")
        verbose_name_plural = _("ระบบมาตรฐาน")

class DocumentCategory(TimeStampedModel):
    name = models.CharField(_("ชื่อหมวดหมู่"), max_length=100, unique=True)
    code = models.CharField(_("รหัสหมวดหมู่"), max_length=10, unique=True) # e.g., WI, PROC, FORM

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = _("หมวดหมู่เอกสาร")
        verbose_name_plural = _("หมวดหมู่เอกสาร")

class Document(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('ฉบับร่าง')
        PUBLISHED = 'PUBLISHED', _('ประกาศใช้')
        REVIEW = 'REVIEW', _('รอการทบทวน')
        CANCELLED = 'CANCELLED', _('ยกเลิก')

    standard_type = models.ForeignKey(
        StandardType, on_delete=models.PROTECT, related_name='documents',
        verbose_name=_("ระบบมาตรฐาน")
    )
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.PROTECT, related_name='documents',
        verbose_name=_("หมวดหมู่เอกสาร")
    )
    
    document_number = models.CharField(
        _("เลขที่เอกสาร"), max_length=50, unique=True, db_index=True
    )
    title = models.CharField(_("ชื่อเอกสาร"), max_length=255)
    
    status = models.CharField(
        _("สถานะ"), 
        max_length=20, 
        choices=Status.choices, 
        default=Status.DRAFT,
        db_index=True
    )
    
    site = models.CharField(
        _("ไซต์/สถานที่"), 
        max_length=100, 
        default=getattr(settings, 'DEFAULT_SITE_NAME', 'Maintenance 2nd site')
    )
    
    # Responsible Persons
    preparer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='prepared_documents',
        verbose_name=_("ผู้จัดทำ")
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='reviewed_documents',
        verbose_name=_("ผู้ทบทวน")
    )
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='approved_documents',
        verbose_name=_("ผู้อนุมัติ")
    )
    
    next_review_date = models.DateField(
        _("วันทบทวนครั้งถัดไป"), db_index=True, null=True, blank=True
    )

    @property
    def latest_file(self):
        latest_v = self.versions.order_by('-created_at').first()
        if latest_v and latest_v.file:
            return latest_v.file.url
        return None

    def __str__(self):
        return f"[{self.document_number}] {self.title}"

    class Meta:
        verbose_name = _("เอกสาร")
        verbose_name_plural = _("เอกสารทั้งหมด")
        ordering = ['-updated_at']

class DocumentVersion(TimeStampedModel):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='versions',
        verbose_name=_("เอกสาร")
    )
    version_number = models.CharField(_("เวอร์ชัน/การแก้ไข"), max_length=20)
    file = models.FileField(_("ไฟล์แนบ"), upload_to=document_upload_path)
    revision_history = models.TextField(_("ประวัติการแก้ไข"), blank=True)
    effective_date = models.DateField(_("วันที่มีผลบังคับใช้"))

    def __str__(self):
        return f"{self.document.document_number} - v{self.version_number}"

    class Meta:
        verbose_name = _("เวอร์ชันเอกสาร")
        verbose_name_plural = _("เวอร์ชันเอกสารทั้งหมด")
        unique_together = ('document', 'version_number')

class Department(TimeStampedModel):
    name = models.CharField(_("ชื่อแผนก"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("แผนก")
        verbose_name_plural = _("แผนกทั้งหมด")

class Employee(TimeStampedModel):
    employee_id = models.CharField(_("รหัสพนักงาน"), max_length=20, unique=True)
    first_name = models.CharField(_("ชื่อ"), max_length=100)
    last_name = models.CharField(_("นามสกุล"), max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='employees',
        verbose_name=_("แผนก")
    )
    position = models.CharField(_("ตำแหน่ง"), max_length=100, blank=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("พนักงาน")
        verbose_name_plural = _("พนักงานทั้งหมด")

class Schedule(TimeStampedModel):
    class ActivityType(models.TextChoices):
        TRAINING = 'TRAINING', _('การฝึกอบรม')
        INTERNAL_AUDIT = 'INTERNAL_AUDIT', _('การตรวจติดตามภายใน')
        EXTERNAL_AUDIT = 'EXTERNAL_AUDIT', _('การตรวจติดตามภายนอก')
        MANAGEMENT_REVIEW = 'MANAGEMENT_REVIEW', _('การทบทวนฝ่ายบริหาร')

    class Status(models.TextChoices):
        PLANNED = 'PLANNED', _('ตามแผน')
        COMPLETED = 'COMPLETED', _('ดำเนินการเสร็จสิ้น')
        CANCELLED = 'CANCELLED', _('ยกเลิก')

    activity_type = models.CharField(
        _("ประเภทกิจกรรม"), max_length=50, choices=ActivityType.choices, db_index=True
    )
    standard_type = models.ForeignKey(
        StandardType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='schedules',
        verbose_name=_("มาตรฐานที่เกี่ยวข้อง")
    )
    title = models.CharField(_("ชื่อกิจกรรม"), max_length=255)
    scheduled_date = models.DateField(_("วันที่กำหนด"), db_index=True)
    description = models.TextField(_("รายละเอียด"), blank=True)
    responsible_person = models.CharField(_("ผู้รับผิดชอบ"), max_length=100)
    status = models.CharField(
        _("สถานะ"), max_length=20, choices=Status.choices, default=Status.PLANNED
    )
    documents = models.ManyToManyField(
        Document, 
        blank=True, 
        related_name='training_schedules',
        verbose_name=_("เอกสารที่เกี่ยวข้องกับการอบรม")
    )

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title}"

    class Meta:
        verbose_name = _("กำหนดการ")
        verbose_name_plural = _("กำหนดการทั้งหมด")
        ordering = ['scheduled_date']

class TrainingRecord(TimeStampedModel):
    class Result(models.TextChoices):
        PASS = 'PASS', _('ผ่าน')
        FAIL = 'FAIL', _('ไม่ผ่าน')
        PENDING = 'PENDING', _('รอผล')

    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='training_records',
        verbose_name=_("รายการอบรม")
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='training_history',
        verbose_name=_("พนักงาน")
    )
    is_attended = models.BooleanField(_("เข้าอบรม"), default=True)
    score = models.DecimalField(_("คะแนน"), max_digits=5, decimal_places=2, null=True, blank=True)
    result = models.CharField(
        _("ผลการทดสอบ"), max_length=10, choices=Result.choices, default=Result.PENDING
    )
    remark = models.TextField(_("หมายเหตุ"), blank=True)

    def __str__(self):
        return f"{self.employee} - {self.schedule.title}"

    class Meta:
        verbose_name = _("บันทึกการอบรมรายบุคคล")
        verbose_name_plural = _("บันทึกการอบรมรายบุคคล")
        unique_together = ('schedule', 'employee')

class ScheduleAttachment(TimeStampedModel):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='attachments',
        verbose_name=_("กำหนดการ")
    )
    file = models.FileField(_("ไฟล์แนบ"), upload_to=schedule_upload_path)
    description = models.CharField(_("รายละเอียดไฟล์"), max_length=255, blank=True)

    def __str__(self):
        return f"ไฟล์แนบสำหรับ {self.schedule.title}"

    class Meta:
        verbose_name = _("ไฟล์แนบกำหนดการ")
        verbose_name_plural = _("ไฟล์แนบกำหนดการทั้งหมด")
