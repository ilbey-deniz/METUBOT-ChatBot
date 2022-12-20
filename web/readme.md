# metubot-web

## Project setup

First you need to install the dependencies:

```
cd backend; npm install; cd ../frontend; npm install;
```

Then you need to copy the backend/.env.example file to backend/.env and fill in the values. The real .env file is not
committed because it is dependent on the server and may contain classified information.


Run the backend/frontend bundle

```
cd backend; node node.js;
```


The compiled frontend is in git and can be found at frontend/dist. To compile it:

```
cd frontend; npm run build;
```
