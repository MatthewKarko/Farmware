# Developer Documentation
## Running The Application
### Backend
The backend is made using the Django framework. 

1. There might be a possibility that you need to migrate any database changes. To
do so, simply run `python manage.py migrate`
2. Run the server using `python manage.py runserver`

### Frontend
The frontend is made using the React JavaScript framework.
1. Navigate to the frontend directory, i.e., `cd frontend/`
2. Run the install script via the package manager, i.e., `npm install --save`
3. Run the frontend server using `npm run`

## Testing
To test the application, run `python manage.py test`

## Getting Ready for Production
To ensure everything is ready for production
1. Go into the frontend directory and run `npm run build`
1. Run `python manage.py collectstatic`

## Running The Application in Deployment
1. Create an EC2 instance with appropriate settings
1. Add instance URL to `ALLOWED_HOSTS` inside `settings.py`
1. Add URL to the axios base URL in the `frontend`
1. Connect to EC2 instance
1. Update apt via `sudo apt-get update`
1. Install pip3 via `sudo apt-get install python3-pip`
1. Clone the production branch of the repository in the current directory
1. Use `cd Farmware` to go into the Farmware directory
1. Install requirements via `pip install -r requirements.txt`
1. Use `sudo apt-get install nginx` to install nginx
1. Use `sudo service nginx status` to check the status of the server.
    - If it is not running, use `sudo service nginx start`
1. Install uwsgi using `pip3 install uwsgi`
1. Install the python plugin for uwsgi via `sudo apt-get install uwsgi-plugin-python3`
1. Replace the `/etc/nginx/nginx.conf` file with the one in the Farmware deployment directory
1. Setup a `.env` file in `Farmware/farmware/farmware/` with the following
    - DJANGO_DEBUG = False
    - SENDGRID_DISTRIBUTED_API_KEY = <YOUR_API_KEY>
1. Copy the `uwsgi.ini` file in the Farmware deployment directory to `Farmware/farmware/`
2. Restart the server using `sudo service nginx restart`
1. Run uwsgi using `uwsgi uwsgi.ini --plugin python3`
1. Ensure everything is working by visiting the EC2 url

### Troubleshooting
1. If there is an issue with the static files
    - Run `python manage.py collectstatic` within the EC2 console
    - Ensure the permissions are not too restrictive, e.g., `sudo chmod a+rwx ubuntu/`