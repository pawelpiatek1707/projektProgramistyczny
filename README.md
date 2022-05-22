# Projekt Promistyczny

## Project description

The subject of the project is a web application. It consists of two parts: a backend part created using Flask and a frontend part created using React.js

Flask application through access to the camera observes the environment and saves photos when it detects a person.

Additionally, the application provides 3 endpoints.
- For logging in ```/login```
- To download all photos ```/images```
- To delete selected photo ```/images/<name>```

## Usefull resources

- [Frontend repo](https://github.com/pawelpiatek1707/projekt-programistyczny-react)
- [Heroku](https://cctv-flask.herokuapp.com/)

## Technologies

### Backend

- Flask
- OpenCV



## Project structure
```
|---app
    |-- helpers (functions for capturing images)
    |-- static (captured images)
    |-- templates (html page for capturing images)
    |-- main.py (main python file)
```

## Getting started

python main.py
