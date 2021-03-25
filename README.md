![workflow status](https://github.com/JulieNikitina/foodgram-projectl/workflows/cook_workflow/badge.svg)

# Foodgram-project

Social network for publishing recipes by app users.

## Getting Started
These instructions will allow you to run a copy of the project on your server 
using CICD with Github actions.

### Prerequisites

1. Prepare your server
2. Fork repository https://github.com/JulieNikitina/foodgram-project.git
3. Clone your repository
4. Rename .env-example to .env and fill with your secret data.
5. Change 12 line in settings.py (ALLOWED_HOSTS) to public IP of your server 
6. Create public repository for this project on https://hub.docker.com/
7. Open foodgram-project folder and run  ```docker build -t <DockerHub_username>/<project_name> .``` 
   for build image of project
8. Push your image to DockerHub 
  ``` 
    docker login -u <DockerHub_username>
    docker push <DockerHub_username>/<project_name>
  ```
9. Change the name of the image on line 18 of the file docker-compose.yaml 
   to name of image <DockerHub_username>/<project_name>
10. Change the name of the image on line 24 of the file .github/workflows/cook_workflow.yml
   to name of image <DockerHub_username>/<project_name>
11. Go to the Settings repository in GitHub, select the Secrets tab, 
   and create secrets:
    * with all the variables from the file .env with names: DB_HOST, DB_NAME, DB_PORT, POSTGRES_PASSWORD, POSTGRES_USER, SECRET_KEY
    * with login and password for DockerHub with names: DOCKER_PASSWORD, DOCKER_USERNAME
    * with settings for connecting to the server with names: HOST, SSH_KEY (private ssh key), USER
    * with settings for send deployment progress message to Telegram with names: TELEGRAM_TO (Your telegram-ID), TELEGRAM_TOKEN (Token of your telegram-bot(get from @BotFather))
12. Run commands for deploy your project
   ```
    git add .
    git commit
    git push
   ```
    
### Installing

1. Сonnect to your server
2. Run the command ```sudo docker-container ls``` for get CONTAINER ID of IMAGE of your project
3. Run ``` sudo docker exec -it <CONTAINER ID> bash```. Use CONTEINER ID from the previous paragraph 
4. Run ```python manage.py makemigrations```
5. Run ```python manage.py migrate```
6. Run ```python manage.py collectstatic -y```
6. To load data, run ```python manage.py load_ingredients```
7. Run ```python manage.py createsuperuser```. Create and enter Username and Password for admin user
8. Go to <your_IP>/admin for use an admin panel and create tags objects
   For tags use names and colors: breakfast - orange, lunch - green, dinner - purple
9. Go to <your_IP> for use project

### Functionallity
   * Full user authentication.
   * Create/edit/delete new recipe.
    * Filter by breakfast/lunch/dinner.
    * Choose from a bunch of ingredients.
    * Add to favourites.
    * Favourites page.
    * Follow another authors.
    * Add to shopping list.
    * Download shopping list.

### What I used
* [Python: 3.8.5](https://www.python.org/)
* [Django: 3.0.8](https://www.djangoproject.com/)
* [PostgreSQL: 12.4](https://www.postgresql.org/)
* [Docker: 3.1.0](https://www.docker.com/)
* [DjangoRestFramework: 3.12.2](https://www.django-rest-framework.org/)
* [gunicorn: 20.0.4](https://gunicorn.org/)

### Author of project
Julie Nikitina - [GitHub](https://github.com/JulieNikitina)

Programming from May 2020

[Yandex.Praktikum](https://praktikum.yandex.ru/) backend-developer faculty graduate March 2021 
  
### License
[MIT](https://choosealicense.com/licenses/mit/)

