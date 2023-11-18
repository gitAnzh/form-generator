
Logo
form generator gateway
A service to create form and get its information.
Explore the docs »

View Demo · Report Bug · Request Feature

Table of Contents
About The Project
For a business, we needed a gateway for generating. So we created this service.

This service will do:

Create a user
create a form
Get a user
Get all users
Get all forms
create super admin

(back to top)

Built With
In this project, we used the following technologies:

Python
Mongo DB
Minio
Later, Vue.js may included.
(back to top)

Getting Started
In this part, there is an instructions on setting up the project locally. To get a local copy up and running follow these simple steps.

Prerequisites
For this project, you need python v3.9 and mongodb v5Install MongoDB Community Edition

Installation
After installing prerequisites, now you can install dependencies of this project:

Clone the repo

git clone [github.com/gitAnzh/form-generator](https://github.com/gitAnzh/form-generator.git)
Setup an environment

sudo apt install python3-virtualenv
virtualenv venv
source venv/bin/activate
Install pip packages

pip install -r requirements.txt
In main directory(where setup.py file is) use this command to install the project

pip install -e .
Create .env file in main directory

APP_NAME="form-generator"

MONGO_HOST="localhost"
MONGO_PORT="27017"
MONGO_USER=""
MONGO_PASS=""

MINIO_HOST="localhost"
MINIO_PORT="9001"
MINIO_ACCESS_KEY=""
MINIO_SECRET_KEY=""
MINIO_BUCKET_NAME=""

UVICORN_HOST="0.0.0.0"
UVICORN_PORT="8000"

TELEGRAM_BOT_TOKEN=""
CHAT_IDS=[123456789]
(back to top)

Usage
To run the project, make sure that the mongodb service is up locally and run this in the app directory

python main.py
You can visit localhost:8000 for root directory.
(back to top)

Database Visualization
Download mongodb compass: MongoDB Compass

Testing
For testing the project, run this command in main directory

pytest
Coverage
Testing coverage can also be achieved by:

pytest --cov
Roadmap
Get and manipulate Kowsar data
CRUD for form-generator
validate form-generator
Refactor according to needs
Multi-language Support
Persian
English
Arabic
(back to top)

Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
(back to top)

License
All rights reserved

(back to top)

Contact
Mohsen yousefi - mohsen.u3fi@hotmail.com

(back to top)
