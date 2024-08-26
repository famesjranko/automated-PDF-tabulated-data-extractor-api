# PDF TABLE PARSER API - BACK-END
  
## How to run:  
  
1. install python 3.7 to local machine incl. PATH (https://www.python.org/downloads/)  
2. install git  
windows: [git for windows](https://gitforwindows.org/)  
macos: ```brew install git```  
debian: ```sudo apt install git```   
3. clone the repo to your project dir:
```bash
git clone --single-branch --branch master https://github.com/4BDAW/Lensell-Project.git
```
4. change into cloned project directory and create python virtual env
```
cd Lensell-Project
python3 -m venv env
```
5. activate venv   
unix based systems: ```source env/bin/activate```   
windows: ```env\Scripts\activate```   
  
5. upgrade pip, setuptools and wheel  
```bash
python -m pip install --upgrade pip setuptools wheel
```  
6. change into django-backend directory and install project dependencies:
```bash
pip install -r requirements.txt
```  
7. install poppler - see below for guide  
8. and finally, run project with: 
```bash
python manage.py runserver 0.0.0.0:8000
```  

### Admin web portal:
```bash
http://127.0.0.1:8000/admin/
```
#### admin login:  
name: admin  
password: lensell  
  
### Additional:  
If any issues with the database, complete any lingering migrations:  
first run:
```bash
python manage.py makemigrations
```  
then run:
```bash
python manage.py migrate
```  
This shouldn't be required tho
  
## Troubleshooting Issues

### Camelot depends on:  
1. [Poppler](https://pdf2image.readthedocs.io/en/latest/installation.html)  
  
### Installing poppler:  

#### Ubuntu  
```bash
sudo apt-get install poppler-utils  
```

#### MacOS  
```bash
brew install poppler  
```
  
#### Windows  
1. Download the latest package from http://blog.alivate.com.au/poppler-windows/  
2. Extract the package  
3. Move the extracted directory to the desired place on your system  
4. Add the bin/ directory to your PATH  
5. Test that all went well by opening cmd and making sure that you can call pdftoppm -h  
  
SCREENSHOTS:  
UPLOAD  
![upload](https://github.com/4BDAW/Lensell-Project/blob/master/django-backend/screenshots//file-only.png)  
UPLOAD DB-DATA-CONTROL  
![upload-data-control](https://github.com/4BDAW/Lensell-Project/blob/master/django-backend/screenshots/data_control.png)  
ADMIN VIEW REPORTS  
![admin view reports](https://github.com/4BDAW/Lensell-Project/blob/master/django-backend/screenshots/reports.png)  
ADMIN EDIT/ADD/DELETE REPORT  
![admin edit reports](https://github.com/4BDAW/Lensell-Project/blob/master/django-backend/screenshots/change_report.png)  
