# Django Project with PostgreSQL

This project is built with Django and PostgreSQL as the database backend. It also uses JWT authentication (`rest_framework_simplejwt`), with roles for students, teachers, and admins, as well as project submission and form approval workflows.

## Requirements


## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/porcupine02/mini_clone_carbon.git
cd mini_clone_carbon
```


### 2. Set backend 
-   Go to backend folder : `cd carbon_lamunpun`
-   Set docker : `docker compose up -d`
-   Set reuirements : `pip install -r requirements.txt`
-   `python manage.py makemigrations`
-   `python manage.py migrate`
-   `python3 manage.py runserver`


### 3. Set frontend 
-   Go to frontend folder : `cd front`
-   `yarn install`
-   `yarn dev`
