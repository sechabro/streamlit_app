# Streamlit Cryptocurrency Live Data Feed #

## Deploying to Heroku via CLI ##
_Heroku cli installation, and heroku app, need to be created first_
```
heroku login
heroku container:login
heroku container:push web -a <app_name>
heroku container:release web -a <app_name>
heroku open -a <app_name>
```