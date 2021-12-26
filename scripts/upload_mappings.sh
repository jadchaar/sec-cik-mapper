#!/usr/bin/env bash

MAPPINGS_DIR="mappings"
NUM_CHANGES=$(git status $MAPPINGS_DIR --porcelain | wc -l)
CURRENT_DATE=$(date +'%m/%d/%y')

if [[ $NUM_CHANGES -gt 0 ]]; then
    # Mappings have changed, so commit and push them to the remote repo
    git config --global user.name 'Jad Chaar'
    git config --global user.email 'jadchaar@users.noreply.github.com'
    git add $MAPPINGS_DIR
    git commit -m "$CURRENT_DATE automated CRON job - update mappings"
    git push
else
    echo "No mapping changes detected. Skipping upload..."
fi
