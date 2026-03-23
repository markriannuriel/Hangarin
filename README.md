# Hangarin

A lightweight Django task and to-do manager.

## Features
- Create, edit, and delete tasks
- Deadlines with due soon and overdue views
- Task status and priority tracking
- Subtasks and notes support
- Basic search and filtering

## Tech stack
- Python 3.11+
- Django 6.0
- Bootstrap 5 for UI

## Setup
1. Clone repository:
   ```bash
   git clone https://github.com/markriannuriel/Hangarin.git
   cd Hangarin
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start development server:
   ```bash
   python manage.py runserver
   ```

## Maintenance
- To seed example data: `python manage.py seed`
- To run tests: `python manage.py test`

## License
MIT
