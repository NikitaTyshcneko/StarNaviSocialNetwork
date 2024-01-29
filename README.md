**SOCIAL NETWORK**


**Copy code**
```
git clone https://github.com/NikitaTyshcneko/StarNaviSocialNetwork.git
cd SocialNetwork
```

**Install dependencies:**
```
pip install -r requirements.txt
```
**Apply migrations:**
```
python manage.py makemigrations
python manage.py migrate
```

**Run the Django development server:**
```
python manage.py runserver
```

**API Endpoints**

GET /api/v1/post/: Retrieve posts.

POST /api/v1/post/: Add a new post.

PUT /api/v1/post/: Update post.

DELETE /api/v1/post/: Delete post.

GET /api/v1/like-analytic/: Retrieve analytic about likes.

GET /api/v1/user-activity/: Retrieve info about user.

GET /register/: Register new user.

GET /api/v1/docs/: Swagger documentation.

**Testing**
```
pytest
```

**Dockerization**
The application is containerized using Docker for easy deployment and scalability. Use the provided Dockerfile to build the Docker image.
```
docker-compose up --build 
```
