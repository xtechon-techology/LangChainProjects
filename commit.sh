#!/bin/bash

# Store the current global Git username and email
OLD_GLOBAL_USER_NAME=$(git config --global user.name)
OLD_GLOBAL_USER_EMAIL=$(git config --global user.email)

# Store the current local Git username and email (if they exist)
OLD_LOCAL_USER_NAME=$(git config user.name)
OLD_LOCAL_USER_EMAIL=$(git config user.email)

# Set new Git username and email globally
echo "Changing global Git username and email..."
git config --global user.name "xtechon-techology"
git config --global user.email "helpdesk@xtechon.com"

# Set new Git username and email locally
echo "Changing local Git username and email..."
git config user.name "xtechon-techology"
git config user.email "helpdesk@xtechon.com"

# Add all changes to the staging area and commit
echo "Staging changes..."
git add .

echo "Committing changes..."
git commit -m "Ollama with LLama 3"

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
