# 📄 ISO Document Control System (Maintenance 2nd site)
ระบบบริหารจัดการและติดตามเอกสารมาตรฐานสากล สำหรับแผนกซ่อมบำรุง (Maintenance 2nd site)

---

## 🌟 คุณสมบัติ (Features)
- **Multi-Standard Support**: รองรับ ISO 9001, 14001, 45001, 50001 และ PSM
- **Scalable Architecture**: ออกแบบโครงสร้างแบบแยก App และ Settings พร้อมรองรับการขยายระบบ
- **Version Control**: ระบบเก็บประวัติการแก้ไข (Revision History) และการจัดการไฟล์แนบแยกตามรุ่น
- **Review Tracking**: ระบบแจ้งเตือนและติดตามวันทบทวนเอกสาร (Next Review Date)
- **Role-based Workflow**: กำหนดผู้จัดทำ (Preparer), ผู้ทบทวน (Reviewer) และผู้อนุมัติ (Approver)
- **Production Ready**: รองรับ PostgreSQL และการตั้งค่าความปลอดภัยสำหรับ Production

---

## 🛠 ความต้องการของระบบ (Prerequisites)
- **Python**: 3.9 หรือสูงกว่า
- **PostgreSQL**: 13 หรือสูงกว่า
- **Virtual Environment**: แนะนำให้ใช้งาน venv หรือ virtualenv

---

## 🚀 ขั้นตอนการติดตั้ง (Installation Guide)

### 1. เตรียมโปรเจกต์
```bash
# Clone หรือดาวน์โหลดโปรเจกต์
cd Web_app_support_ISO

# สร้าง Virtual Environment
python -m venv venv

# เปิดใช้งาน Virtual Environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. ติดตั้ง Library
```bash
pip install -r requirements.txt
```

### 3. ตั้งค่าสภาพแวดล้อม (Environment)
คัดลอกไฟล์ตัวอย่างและแก้ไขค่าคอนฟิก:
```bash
cp .env.example .env
```
เปิดไฟล์ `.env` และแก้ไขข้อมูลให้ถูกต้อง:
- `DATABASE_URL`: รูปแบบ `postgres://user:password@host:port/dbname`
- `SECRET_KEY`: กำหนดรหัสความปลอดภัยสำหรับ Django
- `DEFAULT_SITE`: `Maintenance 2nd site` (หรือชื่อไซต์ที่ต้องการ)

### 4. เตรียมฐานข้อมูล (Database Migration)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. สร้างบัญชีผู้ดูแลระบบ (Initial Data)
```bash
# สร้าง Superuser
python manage.py createsuperuser

# (แนะนำ) เข้าไปเพิ่ม Standard Types และ Categories ในหน้า Admin
```

### 6. เริ่มใช้งาน
```bash
python manage.py runserver
```
เข้าใช้งานได้ที่: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## 🏗 โครงสร้างโฟลเดอร์ (Architecture)
- `/apps/document_control`: โมเดลและตรรกะหลักของระบบ
- `/config/settings`:
    - `base.py`: ค่าพื้นฐานที่ใช้ร่วมกัน
    - `local.py`: สำหรับการพัฒนา (DEBUG=True)
    - `production.py`: สำหรับใช้งานจริง (Security Hardened)
- `/media/documents`: โฟลเดอร์เก็บไฟล์เอกสารที่อัปโหลด (จัดโครงสร้างแยกตามเลขที่เอกสาร)

---

## 📝 บันทึกการพัฒนา (Developer Notes)
- **Database Indexing**: มีการสร้าง Index ในฟิลด์ `document_number`, `status`, และ `next_review_date` เพื่อเพิ่มประสิทธิภาพการค้นหา
- **File Storage**: ระบบจะสร้างโฟลเดอร์ให้อัตโนมัติในรูปแบบ `documents/<doc_number>/v<version>/<filename>`
- **Security**: กรุณาอย่าส่งไฟล์ `.env` เข้าไปในระบบ Source Control (Git)

---

## 📞 ติดต่อและสนับสนุน
หากพบปัญหาหรือต้องการฟีเจอร์เพิ่มเติม กรุณาติดต่อทีมพัฒนาซอฟต์แวร์ของแผนก
