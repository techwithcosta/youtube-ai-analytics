#!/bin/bash

# Check if the files exist
if [ -f "mage/example_env" ] && [ -f "terraform/keys/example_my-creds" ] && [ -f "mage/keys/example_my-creds" ]; then
    # Rename the files
    mv mage/example_env mage/.env
    mv terraform/keys/example_my-creds terraform/keys/my-creds.json
    mv mage/keys/example_my-creds mage/keys/my-creds.json
    echo "Files renamed successfully!"
else
    echo "One or more files do not exist."
fi