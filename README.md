# mini_clone_carbon
clone carbon.it mini for test django, nuxt for apply job


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

Note : postman file version 2.0

### 3. Set frontend 
-   Go to frontend folder : `cd front`
-   `yarn install`
-   `yarn dev`
