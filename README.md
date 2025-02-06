<h1 align="center" id="title">Newspaper Editorial Tracking System</h1>

<p id="description">You are the chief editor of a newspaper. You have an excellent team of editors but you lack a proper system to track which editors were responsible for each newspaper issue published by your agency. To solve this problem you have decided to create a system that will allow tracking of editors assigned to each newspaper issue. This will help maintain a clear record of responsibilities.</p>

<h2>🚀 Demo</h2>

[https://newspaper-old-paper-agency.onrender.com](https://newspaper-old-paper-agency.onrender.com)

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Manage newspaper issues and their assigned editors
*   Track editorial responsibility for each published issue
*   Optional: Assign multiple themes to each newspaper issue for better categorization

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository:</p>

```
git clone https://github.com/valerii-kashpur/Newspaper-agency
```

```
cd newspaper-tracking
```

<p>3. Switch branch to dev</p>

```
git checkout dev
```

<p>4. Create and activate a virtual environment:</p>

```
python -m venv venv
```

```
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

<p>6. Install dependencies:</p>

```
pip install -r requirements.txt
```

<p>7. Run migrations:</p>

```
python manage.py migrate
```

<p>8. Load fixtures:</p>

```
manage.py loaddata dump.json
```

<p>9. Create .env with vars from example:</p>

```
SECRET_KEY =
```

```
DJANGO_SETTINGS_MODULE=agency_service.settings.dev
```

<p>11. Also use dev for all settings to be able use alowed host:</p>

```
agency_service.settings.dev
```

<p>12. Run the development server:</p>

```
python manage.py runserver
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Backend: Django (Python)
*   Database: PostgreSQL (or SQLite for development)
*   Frontend: Django templates
*   Authentication: Django Authentication System
*   Styles: Bootstrap 5

<h2>🛡️ License:</h2>

This project is licensed under the

<h2>💖Like my work?</h2>

Author: Valerii Kashpur Contact: kashpur.v.f@gmail.com
