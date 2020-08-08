# Web App

All codes are in python, using plotly, dash and dash_bio components. 

To deploy the dash app I used Heroku.


# Created a new folder for the project:
```$ mkdir dash_app_example
$ cd dash_app_example```


# Initialize the folder with git and a virtualenv
```$ git init        # initializes an empty git repo
$ virtualenv venv # creates a virtualenv called "venv"
$ source venv/bin/activate # uses the virtualenv```



# Initialize the folder with a sample app (app.py), a .gitignore file, requirements.txt, and a Procfile for deployment
```$ pip install dash
$ pip install plotly
$ pip install gunicorn```




# 4. Initialize Heroku, add files to Git, and deploy
```$ heroku create my-dash-app # change my-dash-app to a unique name
$ git add . # add all files to git
$ git commit -m 'Initial app boilerplate'
$ git push heroku master # deploy code to heroku
$ heroku ps:scale web=1  # run the app with a 1 heroku "dyno"```
