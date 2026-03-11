# 🏢 NexusHR - Human Resources Management System

A comprehensive HR management system with a modern Graphical User Interface (GUI), developed in Python using `CustomTkinter` and `SQLite` following the MVC architecture.

*Read this in other languages: [Español](README.es.md)*

## ⚡ QUICK START

### 1-Click Installation

```bash
# 1. Install Python 3.8+ (https://www.python.org/downloads/)
# 2. Run the launcher:
python iniciar_sistema.py
```

**That's it!** The system will automatically:
- ✅ Check Python versions and install dependencies (`customtkinter`, `bcrypt`, `matplotlib`).
- ✅ Setup the `SQLite` local database (No XAMPP or MySQL required!).
- ✅ Launch the application in your preferred language.

---

## 🚀 Features (v3.0.0)

- **Modern GUI** with CustomTkinter (Dark/Light themes).
- **Zero-Config Database**: Powered by SQLite for true portability.
- **3 System Roles** with strict authorization flows (First user is Admin).
- **i18n Support**: Native English and Spanish toggles.
- **Data Analytics**: Visual charts (Matplotlib) for department headcount and salaries.
- **Synthetic Data**: One-click test data generation for easy evaluation.
- **Time Tracking**: Legal validation for max 12h/day.
- **Security**: Bcrypt password hashing.

## 🏗️ MVC Architecture

```text
models/            → Data layer (SQLite operations)
views/             → Graphical interfaces (CustomTkinter)
controllers/       → Business logic & Validation
utils/             → Helpers, Validators, and i18n
config.py          → Centralized settings (Themes, DB, App Title)
iniciar_sistema.py → ⭐ UNIQUE EXECUTABLE ENTRY POINT
```

## 👤 First Use (Registration Flow)

1. **Register the initial user**
   - Click "Register" on the login screen.
   - The **First Registered User** automatically becomes the **HR Admin (100)**.
2. **Subsequent Users**
   - Any other user registered from the public portal defaults to **Employee (102)**.
   - Admins must manually promote them to Managers if required.
3. **Log in** with your created credentials.

## 👥 System Roles

### 🔴 HR Administrator (100)
- Full CRUD for employees and projects.
- Analytics and charts dashboard.
- Generate synthetic test data.
- System-wide configuration.

### 🟠 Manager (101)
- CRUD for departments.
- Assign employees to departments.
- View department analytics.

### 🟡 Employee (102)
- Log worked hours on assigned projects.
- View personal history.

## 📖 Usage Tutorial

Follow these steps to experience the full NexuHR workflow:

1. **Initial Setup (Admin)**
   - Run the app and click **Register**.
   - Create your account. **Because you are the first user in the system**, you automatically become the **HR Administrator (100)**.
   - You can toggle the public Registration on or off using the yellow button in your dashboard.

2. **Generate Test Data (Optional but recommended)**
   - As an Admin, go to the **"Informes" (Reports)** tab.
   - Click "**Generar Datos de Prueba Sintéticos**" to instantly spawn 50+ fake employees, 6 departments, and random assignments.
   - *This step populate the entire system so you can test search and analytics!*

3. **Managing the Company**
   - Head back to the **"Gestionar Empleados" (Manage Employees) / "Gestionar Proyectos" (Manage Projects)** tabs to Create, Read, Update, or Delete (CRUD) records.
   - If other real users register via the Login screen, they will start as **Employees (102)**. You can select them and Edit their role to **Manager (101)** if needed.

4. **Manager Workflow**
   - Log out and log in as a Manager account (or create one).
   - Managers have access to their own unique interface holding the **"Gestionar Departamentos" (Manage Departments)** tab.
   - Here, they assign employees to departments and monitor their own areas.

5. **Employee Workflow**
   - Log out and log in as a standard **Employee**.
   - Employees see a narrowed-down dashboard.
   - Go to the **"Registrar Tiempo" (Time Logging)** tab. Select the date, write your hours, link them to a project if desired, and save.
   - View your historical logs in the **"Mis Registros"** tab.

6. **Analytics and Insights**
   - Log back in as Admin!
   - Head to **Reports > Ver Analíticas (View Analytics)**.
   - A new dashboard with Matplotlib pie and bar charts will materialize, reading live metrics from the SQLite DB.

## 🐛 Troubleshooting

### "ModuleNotFoundError"
If the auto-installer fails, you can run:
```bash
pip install -r requirements.txt
```

### General Errors
Check `Local-Human-Resources-System/.system_generated/logs/` or run `python test_sistema.py` to diagnose SQLite or UI issues.
