# Add changes

## AWS instance
1. Activate virtual environment:
```
$ ls mysite
$ source websiteenv/bin/activate
```
2. Migrate changes:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
3. Collect static content:
```
$ python manage.py collectstatic
```
4. Deactivate virtual environment:
```
$ deactivate
```
5. Reload Gunicorn
```
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
```
6. Restart Nginx:
```
$ sudo systemctl restart nginx
```

# Deployment

## AWS instance
Instantiate remote server
1. Start an EC2 (elastic compute) instance based in Singapore (or any SEA servers).
2. Select Ubuntu 16 free-tier AMI
3. Launch remote server
4. Add inbound rules for security group used:
```
HTTP TCP 80 0.0.0.0/0
HTTP TCP 80 ::/0
SSH TCP 22 0.0.0.0/0
SMTP TCP 25 ::/0
SMTP TCP 25 0.0.0.0/0
```

Connect to remote server
1. If on Linux (preferably Ubuntu), launch a terminal. On the other hand for Windows, launch Putty or Cygwin. (I use Cygwin which simulates a Linux terminal environment since I don't want to install Ubuntu)
2. On your AWS EC2 instance dashboard, follow the steps on 'Connect To Your Instance' modular page to open an SSH to the remote server.

## Prerequisites
* steps were followed [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
1. Update packages:
```
$ sudo apt-get update
```
2. Install python3-pip, python3-dev, libpq-dev, nginx and git:
```
$ sudo apt-get install python3-pip python3-dev libpq-dev nginx git
```
3. Install virtualenv through pip
```
$ sudo -H pip3 install --upgrade pip
$ sudo -H pip3 install virtualenv
```
4. Clone remote website directory:
```
$ git clone https://github.com/adjourn02/mysite.git
```
5. Create a virtual environment and activate it:
```
$ ls mysite
$ virtualenv websiteenv
$ source websiteenv/bin/activate
```
6. Install django and gunicorn:
```
$ pip install django gunicorn
```
7. Install other dependencies:
```
$ pip install django-js-asset Pillow
```
8. Change allowed hosts to '*':
```
$ sudo vim mysite/settings.py
```
9. Migrate changes:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
10. Collect static content:
```
$ python manage.py collectstatic
```
11. Deactivate virtual environment:
```
$ deactivate
```
12. Create and open a systemd service file for Gunicorn with sudo privileges in your text editor:
```
$ sudo vim /etc/systemd/system/gunicorn.service

...

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/mysite
ExecStart=/home/ubuntu/mysite/websiteenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/mysite/mysite.sock mysite.wsgi:application

[Install]
WantedBy=multi-user.target
```
12. Start the Gunicorn service we created and enable it so that it starts at boot:  
```
$ sudo systemctl start gunicorn
$ sudo systemctl enable gunicorn
```
&nbsp;&nbsp;&nbsp;&nbsp;If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:
```
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
```
&nbsp;&nbsp;&nbsp;&nbsp;Check status:
```
$ sudo systemctl status gunicorn
```
13. Start by creating and opening a new server block in Nginx's sites-available directory:
```
$ sudo vim /etc/nginx/sites-available/mysite

...

server_names_hash_bucket_size  128;

server {
    listen 80;
    server_name ec2-18-136-120-131.ap-southeast-1.compute.amazonaws.com lostjuanderer.com www.lostjuanderer.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/mysite;
    }

    location /media {
        autoindex on;
        alias /home/ubuntu/mysite/blogs/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/mysite/mysite.sock;
    }
}
```
14. Save and close the file when you are finished. Now, we can enable the file by linking it to the sites-enabled directory:
```
$ sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled
```
15. Test your Nginx configuration for syntax errors by typing:
```
$ sudo nginx -t
```
16. If no errors are reported, go ahead and restart Nginx by typing:
```
$ sudo systemctl restart nginx
```

## Connect AWS instance to Godaddy
1. Copy the IP address of the AWS instance to DNS Management
```
Type | Name |     Value      | TTL
 A   |  @   | 18.136.120.131 | 600 
```
    
## Enable Django to send emails
* Followed this [thread](https://stackoverflow.com/questions/35659172/django-send-mail-from-ec2-via-gmail-gives-smtpauthenticationerror-but-works)
1. Unlock captcha: https://accounts.google.com/displayunlockcaptcha
2. On AWS instance, restart Gunicorn and Nginx:
```
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
$ sudo systemctl restart nginx
```

# File transfer
* Refer [here](https://angus.readthedocs.io/en/2014/amazon/transfer-files-between-instance.html)

From local to remote
```
$ scp -i <path/to/PEM file> <path/to/local file> ubuntu@<remote/server/public DNS>:~/<filename>
```
From remote to local
```
$ scp -i <path/to/PEM file> ubuntu@<remote/server/public DNS>:~/<filename> .
```
* if file to be transferred is a directory, include ```-r``` to above command

# Django admin password reset
1. On AWS instance, activate virtual environment:
```
$ ls mysite
$ source websiteenv/bin/activate
```
2. Reset password:
```
$ python manage.py changepassword <username>
```
