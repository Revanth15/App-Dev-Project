# App-Dev-Project
git commands

----FIRST TIME COMMANDS----------------------------------------------------------------

git config --global user.name "<Your name>"

git config --global user.email <email>

git remote add origin https://github.com/Revanth15/App-Dev-Project.git

git remote -v
  
--------------


--To clone--

git clone https://github.com/Revanth15/App-Dev-Project.git
  
-----------------

--To create venv--

py -3 -m venv .venv

pip install -r requirements.txt 

pip install <your needed packages>

---------------------------------------------------------------------------------------



----To update repo---------------------------------------------------------------------

git add . # adds everything to staging

git commit -m "<insert your message>" # to commit changes into locak repo

git push -u origin <branch_name>
  
---------------------------------------------------------------------------------------

----To pull repo-----------------------------------------------------------------------

git pull https://github.com/Revanth15/App-Dev-Project.git

---------------------------------------------------------------------------------------

----Change branch----------------------------------------------------------------------

git checkout -b <branch_name>

---------------------------------------------------------------------------------------
  
----Undo changes----------------------------------------------------------------------

git log # show previous commits
  
git reset --hard HEAD~1 #!!USE WITH CAUTION!! undo commit + any changes made after last commit
  
git reset --soft HEAD~1 #undo commit + keep changes
  
git push -f origin <commit_hash>:<branch_name> #undo remote repo commit to commit hash
  
git revert #fallback to a previous commit. Counts as a commit

---------------------------------------------------------------------------------------









