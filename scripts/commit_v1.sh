#!/bin/bash

# Check if a commit message is passed as an argument
if [ -z "$1" ]; then
    echo "Error: No commit message provided."
    echo "Usage: ./change_git_user.sh \"Your commit message\""
    exit 1
fi

# Store the commit message from the command line
COMMIT_MESSAGE=$1

# Store the current global Git username and email
OLD_GLOBAL_USER_NAME=$(git config --global user.name)
OLD_GLOBAL_USER_EMAIL=$(git config --global user.email)

# Store the current local Git username and email (if they exist)
OLD_LOCAL_USER_NAME=$(git config user.name)
OLD_LOCAL_USER_EMAIL=$(git config user.email)

# Set new Git username and email globally
echo "Changing global Git username and email..."
git config --global user.name "xtechon-technology"
git config --global user.email "helpdesk@xtechon.com"

# Set new Git username and email locally
echo "Changing local Git username and email..."
git config user.name "xtechon-technology"
git config user.email "helpdesk@xtechon.com"

# Remove previously tracked files that are now ignored by .gitignore
echo "Removing ignored files from Git tracking..."
git rm -r --cached .venv .env build LangChainProjects.egg-info

# Add only tracked files to the staging area (excluding files in .gitignore)
echo "Staging changes (excluding files in .gitignore)..."
git add -u  # Stages modified and deleted files only

# Check for staged changes
if git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi

# Commit the staged changes with the provided message
echo "Committing changes with the message: '$COMMIT_MESSAGE'"
git commit -m "$COMMIT_MESSAGE"

# Push the commit to the remote repository
echo "Pushing the commit to the remote repository..."
git push --force

# Pull the changes
echo "Pulling the latest changes..."
git pull

# Revert to the previous global Git username and email
echo "Reverting global Git username and email..."
git config --global user.name "$OLD_GLOBAL_USER_NAME"
git config --global user.email "$OLD_GLOBAL_USER_EMAIL"

# Revert to the previous local Git username and email (if they existed)
if [ -n "$OLD_LOCAL_USER_NAME" ] && [ -n "$OLD_LOCAL_USER_EMAIL" ]; then
    echo "Reverting local Git username and email..."
    git config user.name "$OLD_LOCAL_USER_NAME"
    git config user.email "$OLD_LOCAL_USER_EMAIL"
else
    echo "Clearing local Git username and email as they were not previously set."
    git config --unset user.name
    git config --unset user.email
fi

echo "Git user information restored to previous values."
