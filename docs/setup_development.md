## Pre Requisites
The project is built using following versions of software:
1. Python 3.12.3
2. pip 24.3.1
3. Node 22.13.0
4. Npm 10.9.2
5. Docker

## Clone the Forked Repository
```bash
git clone https://github.com/priyanshu-batham/Algolyzer.git
cd Algolyzer
```

## Setting up Google OAuth service (Optional)
Goto [Google Developer Console](https://console.developers.google.com). Make a new OAuth Client using the following URL as the Authorized Redirect URI:
```http://localhost:8000/accounts/google/login/callback/```

## Run the following commands (Windows users just use git bash):
 ```bash
        # Create a virtual environment named 'env'
        python3 -m venv env
    
        # Activate the virtual environment
        source env/bin/activate
        # (For Windows)
        source env/Scripts/activate

        # Create .env file from .env.sample
        cp .env.sample .env

        # Edit the values in .env accordingly and check it
        cat .env

        # Install python dependencies
        pip install -r requirements.txt
    
        # Install node dependencies
        npm install

        # Install pre-commit hooks
        pre-commit install
    
        # Navigate into Algolyzer project
        cd Algolyzer
    
        # Apply migrations
        python manage.py migrate
    
        # Create a local administrator (make sure you specified values in .env)
        python manage.py create_superuser

        # Load default values in database
        python manage.py loaddata data/*

        # download aiml models
        python manage.py download_models

        # start redis as a docker container
        docker run --name redis -p 6379:6379 -d redis

        # start celery
        celery -A Algolyzer worker --loglevel=info
        # (For Windows)
        celery -A Algolyzer worker --loglevel=info --pool=threads
    
        # Now open a NEW TERMINAL and start tailwind in Algolyzer dir
        npm run tw_watch

        # Finally Open a Third terminal and Run Django server.
        source myenv/bin/activate
        # (For Windows)
        source env/Scripts/activate

        cd Algolyzer
        python manage.py runserver 8000
```
## Open a web browser and goto
```bash
http://localhost:8080
```
**Note - Always use `localhost:8000` instead of `127.0.0.1:8000` if you don't want access blocked from Google during development**