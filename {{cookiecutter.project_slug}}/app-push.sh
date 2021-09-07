#!/bin/bash
cd ../
SERVER_PASS='<SERVER PASSWORD HERE>'
sshpass -p "$SERVER_PASS" rsync -avz --exclude-from={{ cookiecutter.project_slug }}/exclude.txt {{ cookiecutter.project_slug }}/ root@{{cookiecutter.server_ip}}:/root/{{ cookiecutter.project_slug }}/
sshpass -p "$SERVER_PASS" ssh -o StrictHostKeyChecking=no root@{{cookiecutter.server_ip}} "cd {{ cookiecutter.project_slug }}; docker-compose -f production.yml down; docker-compose -f production.yml up --build"
