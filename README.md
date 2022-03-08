# Run The MariaDB Server
`docker-compose up -d`

# Run The API
`cd server`
`python -m pip install -r requirements.txt`
`uvicorn main:app --port 8000`

# Run The Web App
`cd client`
`yarn install`
`ionic serve`