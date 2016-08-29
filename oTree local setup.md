#Local setup of Leeps oTree fork

###Prerequisites
Due to bower dependencies, npm and bower are needed

[Install node.js](https://nodejs.org/en/download/ ), which will install npm (node package manager)    
To check if npm is installed, open terminal and use `npm -v`   
To install bower globally use `npm install -g bower`  

###To install
1. git clone to local directory of choice
2. cd into _static directory, to find bower.json
3. run `bower install`
4. cd.. into main oTree directory and run `pip install -r requirements_base.txt`

###To run locally
1. run `otree resetdb`
2. run `otree runserver` to start local oTree. Leave cli open, open a new terminal if needed.
3. go to url [localhost:8000](localhost:8000) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

###To create new app
`otree startapp my_new_app` to create my_new_app  
add app info to settings.py  
`otree resetdb` needs to be run when a new app is created

###To upgrade otree core
`pip3 install --upgrade otree-core`  
`otree resetdb`