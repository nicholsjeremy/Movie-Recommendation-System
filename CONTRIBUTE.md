Steps to contribute:
1. Checkout to main  branch:
The main branch is created. 
If you need to checkout to main:

`git checkout main`

2. Creating other branches:
To create and switch to a new branch:

`git checkout -b new-branch-name`

To create a branch without switching to it:

`git branch new-branch-name`

3. Raising pull requests:
Push your branch to the remote repository:

`git push origin new-branch-name`

Go to the repository on GitHub
Click on "Pull requests" tab
Click "New pull request"
Select the branch you want to merge into (usually master/main) as the base branch
Select your new branch as the compare branch
Add a title and description for your pull request
Click "Create pull request"
Some best practices:
Use descriptive names for branches (e.g. feature/add-login, bugfix/fix-header)
Keep pull requests focused on a single feature or fix
Write clear descriptions of your changes in the pull request
Request reviews from relevant team members

4. Once approved by a team member, merge it from the Github terminal
