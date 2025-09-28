# PetTech - เทสๆ

นี่คือ backend ของโปรเจกต์ PetTech ที่พัฒนาด้วย Django และ Django REST Framework คู่มือนี้จะอธิบายวิธีการตั้งค่าและรันโปรเจกต์ในเครื่องของคุณให้ทำงานได้เหมือนกับของผู้พัฒนา รวมถึงปัญหาที่อาจเกิดขึ้นและวิธีแก้ไขเบื้องต้น

## สารบัญ
- [สิ่งที่ต้องเตรียม](#สิ่งที่ต้องเตรียม)
- [ขั้นตอนการตั้งค่า](#ขั้นตอนการตั้งค่า)
- [โครงสร้างโปรเจกต์](#โครงสร้างโปรเจกต์)
- [การรันโปรเจกต์](#การรันโปรเจกต์)
- [ปัญหาที่อาจเกิดขึ้นและวิธีแก้ไข](#ปัญหาที่อาจเกิดขึ้นและวิธีแก้ไข)
- [การมีส่วนร่วม](#การมีส่วนร่วม)

## สิ่งที่ต้องเตรียม

ก่อนเริ่มตั้งค่าโปรเจกต์ ตรวจสอบว่าคุณมีสิ่งต่อไปนี้ติดตั้งแล้ว:
- **Python 3.8+**: ดาวน์โหลดได้ที่ [python.org](https://www.python.org/downloads/)
- **Git**: ดาวน์โหลดได้ที่ [git-scm.com](https://git-scm.com/downloads)
- **PostgreSQL**: ใช้สำหรับฐานข้อมูล (ต้องใช้กับ `psycopg2-binary`) ดาวน์โหลดได้ที่ [postgresql.org](https://www.postgresql.org/download/) หรือใช้บริการคลาวด์ เช่น Render หรือ ElephantSQL
- โปรแกรมแก้ไขโค้ด (เช่น VS Code)
- เทอร์มินัลหรือ Command Prompt

## ขั้นตอนการตั้งค่า

ทำตามขั้นตอนต่อไปนี้เพื่อตั้งค่าโปรเจกต์ในเครื่องของคุณ:

1. **โคลน Repository**
   ```bash
   git clone https://github.com/KKP240/Devtools-Proj-Repo.git
   cd Devtools-Proj
   ```

2. **สร้างและเปิดใช้งาน Virtual Environment**
   - บน Windows:
     ```bash
     python -m venv myvenv
     myvenv\Scripts\activate
     ```
   - บน macOS/Linux:
     ```bash
     python3 -m venv myvenv
     source myvenv/bin/activate
     ```

   หลังจากเปิดใช้งาน คุณจะเห็น `(myvenv)` ในเทอร์มินัล

3. **ติดตั้ง Dependencies**
   ติดตั้งแพ็กเกจ Python ที่ระบุในไฟล์ `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   แพ็กเกจที่ติดตั้งประกอบด้วย:
   - `django`: เฟรมเวิร์ก Django
   - `djangorestframework`: สำหรับสร้าง REST API
   - `psycopg2-binary`: อแดปเตอร์สำหรับ PostgreSQL
   - `python-dotenv`: สำหรับจัดการตัวแปรสภาพแวดล้อม
   - `gunicorn`: เซิร์ฟเวอร์ WSGI สำหรับ production
   - `djangorestframework-simplejwt`: สำหรับการยืนยันตัวตนด้วย JWT

4. **ตั้งค่าฐานข้อมูล**
   - ตรวจสอบว่า PostgreSQL ทำงานอยู่ในเครื่องหรือคุณมีสิทธิ์เข้าถึงฐานข้อมูล PostgreSQL
   - สร้างฐานข้อมูลใน PostgreSQL:
     ```sql
     เปิด pgadmin 4
     สร้าง db ชื่อ pettech
     ```
   - สร้างไฟล์ `.env` ในโฟลเดอร์ `pettech` เพื่อเก็บข้อมูลการเชื่อมต่อฐานข้อมูล:
     ```plaintext
    DATABASE_NAME=pettech
    DATABASE_USER=postgres
    DATABASE_PASSWORD=1234 <=== เปลี่ยนตัวนี้
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
     ```
     แทนที่ `DATABASE_PASSWORD` และ `DATABASE_USER` ด้วยข้อมูลของ PostgreSQL ของคุณ

5. **รัน Migrations**
   เข้าไปในโฟลเดอร์โปรเจกต์:
   ```bash
   cd pettech
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **รันเซิร์ฟเวอร์พัฒนา**
   เริ่มเซิร์ฟเวอร์ Django:
   ```bash
   python manage.py runserver
   ```
   เซิร์ฟเวอร์จะทำงานที่ `http://127.0.0.1:8000/` เปิด URL นี้ในเบราว์เซอร์เพื่อตรวจสอบ

## โครงสร้างโปรเจกต์

```
Devtools-Proj/
├── myvenv/              # Virtual environment
├── pettech/             # โฟลเดอร์โปรเจกต์ Django
│   ├── pettech/         # การตั้งค่าและคอนฟิกโปรเจกต์
│   ├── pettechApp/      # แอปพลิเคชันหลัก
│   ├── manage.py        # สคริปต์จัดการ Django
│   └── .env             # ตัวแปรสภาพแวดล้อม (ไม่ถูก track ใน Git)
├── .gitignore           # ไฟล์กำหนดสิ่งที่ Git จะละเว้น
├── README.md            # ไฟล์นี้
└── requirements.txt     # รายการ dependencies
```

- `.gitignore`: ละเว้น `myvenv/`, `__pycache__/`, และ `*.pyc` เพื่อให้ repository สะอาด
- `pettechApp`: แอป Django หลักที่เก็บโมเดล, วิว, และ serializers

## การรันโปรเจกต์

1. เปิดใช้งาน virtual environment:
   ```bash
   myvenv\Scripts\activate  # Windows
   source myvenv/bin/activate  # macOS/Linux
   ```

2. เข้าไปในโฟลเดอร์โปรเจกต์:
   ```bash
   cd pettech
   ```

3. รันเซิร์ฟเวอร์:
   ```bash
   python manage.py runserver
   ```

4. เข้าถึง API หรือหน้า admin (ถ้าตั้งค่าไว้) ที่ `http://127.0.0.1:8000/`

## ปัญหาที่อาจเกิดขึ้นและวิธีแก้ไข

1. **ModuleNotFoundError: No module named 'django' (หรือแพ็กเกจอื่น)**
   - **สาเหตุ**: ไม่ได้ติดตั้ง dependencies อย่างถูกต้อง
   - **วิธีแก้**:
     - ตรวจสอบว่า virtual environment ถูกเปิดใช้งาน (เห็น `(myvenv)` ในเทอร์มินัล)
     - รันคำสั่ง:
       ```bash
       pip install -r requirements.txt
       ```

2. **ข้อผิดพลาดการเชื่อมต่อฐานข้อมูล**
   - **สาเหตุ**: ข้อมูล PostgreSQL ไม่ถูกต้องหรือ PostgreSQL ไม่ทำงาน
   - **วิธีแก้**:
     - ตรวจสอบว่า PostgreSQL ทำงานอยู่ (ใช้ `pg_isready` หรือตรวจสอบ service)
     - ตรวจสอบว่าไฟล์ `.env` มีข้อมูลการเชื่อมต่อที่ถูกต้อง
     - ตรวจสอบการตั้งค่า `DATABASES` ใน `pettech/settings.py`:
       ```python
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.postgresql',
               'NAME': 'pettech',
               'USER': '<your_username>',
               'PASSWORD': '<your_password>',
               'HOST': 'localhost',
               'PORT': '5432',
           }
       }
       ```
       หรือตรวจสอบว่า `DATABASE_URL` ใน `.env` ถูกต้อง

3. **Migration ไม่ถูกนำไปใช้**
   - **สาเหตุ**: ไม่ได้สร้างหรือรัน migration
   - **วิธีแก้**:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

4. **พอร์ตถูกใช้งานอยู่**
   - **สาเหตุ**: มีโปรแกรมอื่นใช้พอร์ต 8000
   - **วิธีแก้**: หยุดโปรแกรมที่ใช้พอร์ตหรือรันเซิร์ฟเวอร์บนพอร์ตอื่น:
     ```bash
     python manage.py runserver 8080
     ```

5. **Git Push ล้มเหลว**
   - **สาเหตุ**: URL remote ไม่ถูกต้องหรือมีปัญหาการยืนยันตัวตน
   - **วิธีแก้**:
     - ตรวจสอบ URL remote:
       ```bash
       git remote -v
       ```
     - ตรวจสอบว่าคุณมีสิทธิ์เขียนใน repository (`https://github.com/KKP240/Devtools-Proj-Repo.git`)
     - ใช้ personal access token หรือ SSH key ถ้าถูกถามเรื่องการยืนยันตัวตน

6. **ไม่พบไฟล์ .env**
   - **สาเหตุ**: ไฟล์ `.env` ไม่ถูกรวมใน repository (ตาม `.gitignore`)
   - **วิธีแก้**: สร้างไฟล์ `.env` ในโฟลเดอร์ `pettech` ด้วยตัวแปรสภาพแวดล้อมที่จำเป็น (เช่น `DATABASE_URL`)

## การมีส่วนร่วม

1. Fork repository นี้
2. สร้าง branch ใหม่:
   ```bash
   git checkout main
   ```
3. ทำการเปลี่ยนแปลงและ commit:
   ```bash
   git add .
   git commit -m "เพิ่มฟีเจอร์ของคุณ"
   ```
4. Push ไปยัง branch ของคุณ:
   ```bash
   git push -u origin main
   ```
5. สร้าง pull request บน GitHub

หากมีปัญหาหรือคำถามเกี่ยวกับการตั้งค่า ติดต่อได้เลย!