# Pre Requisites
The project is built using following versions of software:
1. Docker & Docker-Compose

## Clone the Forked Repository
```bash
git clone https://github.com/priyanshu-batham/Algolyzer.git
cd Algolyzer
```

## (Optional) Setting up Google OAuth service
Goto [Google Developer Console](https://console.developers.google.com). Make a new OAuth Client using the following URL as the Authorized Redirect URI:
```http://localhost:8000/accounts/google/login/callback/```

## Copy .env.sample into .env

```bash
cp .env.sample .env
```
## IMPORTANT: Read the `.env` carefully and make sure to uncomment and comment necessary `CELERY_BROKER_URL` lines in `.env` as specified there.

3. Run the docker containers
```bash
docker-compose up --build
```
## Open a web browser and goto
```bash
http://localhost:8000
```
**Note - Always use `localhost:8000` instead of `127.0.0.1:8000` if you don't want access blocked from Google during development**