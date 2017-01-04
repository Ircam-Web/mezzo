#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'

python $manage migrate --noinput
python $manage create-admin-user

# @todo searching every fixtures file in each folder
python $manage loaddata $app/organization/job/fixtures/organization-job.json
python $manage loaddata $app/organization/projects/fixtures/organization-projects-repositorysystems.json
