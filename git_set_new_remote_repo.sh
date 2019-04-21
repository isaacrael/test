#!/bin/bash
# Written By: Gil Rael




echo "Enter URL for new remote repo"
read remote_url


git remote set-url origin $remote_url
