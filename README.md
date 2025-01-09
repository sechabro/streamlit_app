# Streamlit Cryptocurrency Live Data Feed #

## Deployment Plans ##
_This is a multi-container application using SSH to login directly from one container to the other. It also uses Docker volumes. Unfortunately, Heroku does not support Docker volumes, nor do their dynos support SSH. Therefore, the plan is to deploy using VPS like Ionos or Hostinger._
```
Prior to deployment, however, I'll need to install either Nginx or Apache webserver to map a url to the web container portion of the app.
```
```
VPS deployment instructions to go here.

heroku login
heroku container:login
heroku container:push web -a <app_name>
heroku container:release web -a <app_name>
heroku open -a <app_name>
```