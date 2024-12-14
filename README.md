# Resume Builder

## Install

* Python: https://www.python.org/downloads/
* Pycharm: https://www.jetbrains.com/pycharm/download/?section=windows
* Git: https://git-scm.com/downloads (set default editor to "nano" `git config --global core.editor "nano"`)

## App Setup
**Note: if terminal commands are giving errors, try replacing 'python' with: `C:\users\public\ANACONDA\python.exe` .**
**With pip commands, include the same directory just before 'pip', then include the rest of the command as normal.**
1) Clone the repository in a terminal directed to your desired folder with: `git clone https://github.com/Carleton-BIT/project-AliciaMcG.git`
2) In PyCharm: file -> open -> [cloned project folder]
3) Open the terminal in PyCharm and install dependencies: `pip install -r requirements.txt`
![install dependencies]
5) Create an `.env` in the top level directory
6) Generate a secret key with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and copy the output.
7) Edit the `.env` file and add: `SECRET_KEY="[output from step 6]"`
8) On the terminal run: `python manage.py makemigrations` and `python manage.py migrate`
9) Download and install pillow: `python -m pip install Pillow`

## Running the App
Clicking the play button, or in the terminal: `python manage.py runserver`.
Navigate to 127.0.0.1:8000, or the local host url which is printed in the terminal when you run the server.
Creating a superuser is not necessary to interact and run the site, but if you would like to: `python manage.py createsuperuser` and follow the prompts.
On the home page, create an account or log in with super user credentials. Now you can access the app.