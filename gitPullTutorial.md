#How to use git pull to update local version of repository

###Prerequisites   
run git clone on the repository you want to update
	git clone https://github.com/rlopezlu/ExpressionPTToTree.git

###To git pull
1. In your terminal, navigate using `cd` to the Otree folder containing settings.py, manage.py, and the ExpressionPTT folder
2. run 'git pull'
3. run 'otree resetdb' and press y when prompted
4. run 'otree runserver'
5. go to to url [localhost:8000](localhost:8000) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

###To git commit push
1.	git add .
2.	git commit -m "comment"
3.	git push orign master
	

	
