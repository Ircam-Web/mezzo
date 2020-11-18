include .env
.DEFAULT_GOAL := help
SHELL=/usr/bin/env bash
PWD = $(shell pwd)
NOW = $(shell date +%d-%m-%Y_%H-%M-%S)
PROD_BRANCH=master
STAGING_BRANCH=dev
DOCKER_COMPOSE=docker-compose -f docker-compose.yml -f env/${ENV}.yml

SUPPORTED_COMMANDS := switch-urls
SUPPORTS_MAKE_ARGS := $(findstring $(firstword $(MAKECMDGOALS)), $(SUPPORTED_COMMANDS))
ifneq "$(SUPPORTS_MAKE_ARGS)" ""
  COMMAND_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(COMMAND_ARGS):;@:)
endif

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

print_env:
ifndef ENV
	$(error ENV is undefined, cannot imply the environment. Please create or edit the .env file)
endif
	@echo "---------------------------"
	@echo "> ENVIRONMENT: ${ENV}"
	@echo "---------------------------"
	@echo

deploy: print_env ## Backs up the database, pulls new changes,] rebuilds and reloads the container.
ifeq ($(ENV), prod)
	@echo "> This will checkout \`${PROD_BRANCH}\` and pull changes, build the image and reload the container."
	@read -p "> Press <Enter> to continue or <Ctrl+C> to abort."

	@echo
	#
	# >>> PULL CHANGES
	#
	@echo

	git fetch origin
	git checkout ${PROD_BRANCH}
	git pull origin ${PROD_BRANCH}
	git submodule update --init --recursive
endif
ifeq ($(ENV), staging)
	@echo "> This will checkout \`${STAGING_BRANCH}\` and pull changes, build the image and reload the container."
	@read -p "> Press <Enter> to continue or <Ctrl+C> to abort."

	@echo
	#
	# >>> PULL CHANGES
	#
	@echo

	git fetch origin
	git checkout ${STAGING_BRANCH}
	git pull origin ${STAGING_BRANCH}
	git submodule update --init --recursive
endif
ifeq ($(ENV), dev)
	@echo "> This will build the image and reload the container."
	@read -p "> Press <Enter> to continue or <Ctrl+C> to abort."
endif

	@echo
	#
	# >>> BUILD
	#
	@echo
	$(DOCKER_COMPOSE) build

	@echo
	#
	# >>> RECREATING CONTAINER
	#
	@echo
	$(DOCKER_COMPOSE) up -d

ifeq ($(ENV), dev)
	@echo "> Run \`make watch-frontend\` to build & watch the front-end"
else
	@echo
	#
	# >>> BUILDING THEME
	#
	@echo
	$(DOCKER_COMPOSE) exec app bash -c "cd /srv/lib/ircam-forum-theme/ircam_forum_theme; npm ci; npx webpack --env ${ENV}"
	$(DOCKER_COMPOSE) exec app python manage.py collectstatic --no-input
endif

backup: print_env ## Backs up the database
ifeq ($(ENV), prod)
	sudo -u postgres bash -c "pg_dump -Fc -d ircamforum > ${PWD}/var/backup/postgres_${NOW}.dump"
	rm -f ${PWD}/var/backup/postgres_latest.dump
	ln -s ./postgres_${NOW}.dump ${PWD}/var/backup/postgres_latest.dump
else
	$(DOCKER_COMPOSE) run db /srv/bin/prod/local/backup_db.sh
endif

# TODO: make a backup before the restore (tricky because then it would restore it right away, instead of the n-1)
restore: print_env ## Restore a database backup (default: latest, else pass `name=postgres_XXX` — see ./var/backup)
	@echo "> The restore might exit with error (and thus \`make\` too), but still be successful. Read the warnings carefully tho."
	@echo "> Note that if you restore the database with the latest backup, ALL DATA WRITTEN AFTER THAT BACKUP WILL BE LOST!"
	@read -p "> Press <Enter> to continue or <Ctrl+C> to abort."
ifeq ($(ENV), prod)
ifeq ($(shell test -z $(name) && echo -n not), not)
	sudo -u postgres pg_restore -c -d ircamforum ${PWD}/var/backup/postgres_latest.dump
else
	sudo -u postgres pg_restore -c -d ircamforum ${PWD}/var/backup/$(name).dump
endif
else
ifeq ($(shell test -z $(name) && echo -n not), not)
	$(DOCKER_COMPOSE) run db /srv/bin/dev/local/restore_db.sh
else
	$(DOCKER_COMPOSE) run db /srv/bin/dev/local/restore_db.sh $(name).dump
endif
endif

build: print_env ## Shorthand for `docker-compose ... build` (optionnal `service` parameter)
	@echo "> This will build a new image from the Dockerfile."
	@read -p "> Press <Enter> to continue or <Ctrl+C> to abort."
	$(DOCKER_COMPOSE) build $(service)

up: print_env ## Shorthand for `docker-compose ... up -d` (optionnal `service` parameter)
ifeq ($(ENV), dev)
	$(DOCKER_COMPOSE) up $(service)
else
	$(DOCKER_COMPOSE) up -d $(service)
endif

down: print_env ## Shorthand for `docker-compose ... down`
	$(DOCKER_COMPOSE) down

logs: print_env ## Shorthand for `docker-compose ... logs -f --tail=256` (optionnal `service` parameter)
	$(DOCKER_COMPOSE) logs -f --tail=256

ps: print_env ## Shorthand for `docker-compose ... ps` (optionnal `service` parameter)
	$(DOCKER_COMPOSE) ps

reload: print_env ## Shorthand for `touch app/wsgi.py`
	touch ${PWD}/app/wsgi.py

restart: print_env ## Shorthand for `docker-compose ... restart` (optionnal `service` parameter)
	$(DOCKER_COMPOSE) restart $(service)

pull: print_env ## Pulls changes from the repository on the current branch
	git fetch origin
	git pull
	git submodule update --init --recursive

test: print_env ## Launches APIs connectivity tests
	$(DOCKER_COMPOSE) exec app python manage.py check-apps -d

pending-migrations: print_env ## Lists pending Django migrations
	$(DOCKER_COMPOSE) exec app python manage.py showmigrations --list | grep -v '\[X\]'

watch-frontend: print_env ## Watches front-end changes with Webpack (dev onyl)
ifeq ($(ENV), dev)
	$(DOCKER_COMPOSE) exec app bash -c "cd /srv/lib/ircam-forum-theme/ircam_forum_theme; npx webpack --env ${ENV}"
else
	$(error This target is to be executed in the local environment only)
endif

update: print_env ## Updates local repository and all submodules
	# Update main project
	git pull

	# Get the current branch
	curr_branch=$(git symbolic-ref --short HEAD)
	echo $curr_branch
	if [ $curr_branch != "master" ] && [ $curr_branch != "dev" ];
	then
	    curr_branch="dev"
	fi

	# checkout new submodule
	git submodule update --init

	# Synchronizes submodules' remote URL configuration setting to the value specified in .gitmodules
	git submodule sync

	# Checkout all submodules on right branches specified in .gitmodules, by default the branch is master
	git submodule foreach --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch-'$curr_branch' || echo master)'

	# Pull all submodules on right branches specified in .gitmodules, by default the branch is master
	git submodule foreach --recursive 'git pull origin $(git config -f $toplevel/.gitmodules submodule.$name.branch-'$curr_branch' || echo master)'

hard-reset: print env ## Hard resets the repository and all submodules to the local branches
	git reset --hard
	git submodule foreach --recursive 'git reset --hard')

fix-var-permissions: print_env ## Fixes permissions of the local data var directory
ifeq ($(ENV), dev)
	if ! uname -a | grep Darwin > /dev/null; then
	    declare -a arr=("var/media" "var/backup" "var/static")
	    for folder in "${arr[@]}"; do
	        INFO=( $(stat -L -c "%a %G %U" $folder) )
	        OWNER=${INFO[2]}
	        if [ "$OWNER" != "$USER" ]; then
	            sudo chown -R $USER $folder
	        fi
	    done
	fi
endif

migrations: print_env ## Produces django migrations
	$(DOCKER_COMPOSE) run app python /srv/app/manage.py makemigrations -v 3

merge: print_env ## Merges dev branches of all repositories into local branches
	git submodule foreach --recursive 'echo $name; git merge $(git config -f $toplevel/.gitmodules submodule.$name.branch-dev || echo dev)'

migrate: print_env ## Migrates DB tables against django models
	$(DOCKER_COMPOSE) run app python /srv/app/manage.py migrate -v 3

poetry-add: print_env ## Adds module given in argument to the poetry dependency list
	$(DOCKER_COMPOSE) exec app poetry add $1


pull-data: print_env ## Pulls project data
	git reset --hard origin/master
	git pull origin master
	sudo chown -R www-data: media static

push: print_env ## Pushes all repositories
	git push
	git submodule foreach --recursive 'git push'

status: print_env ## Displays status of the repository and all submodules
	git status  -s -b
	@echo '------ Sub Modules --------'
	git submodule foreach --recursive 'git status -s -b'

docker-clean: print_env ## Cleanup docker containers and images
	# Delete all stopped containers (including data-only containers)
	docker rm $(docker ps -a -q)
	# Delete all 'untagged/dangling' (<none>) images
	docker rmi $(docker images -q -f dangling=true)

update_git_urls: $(REGEX)
	find ./ -path ./var/lib -prune -o -type f \( -name ".gitmodules" -o -name "config" \)  -exec sed -i $(REGEX) {} +

switch-urls: print_env ## Switch all git URLs from SSH to HTTPS and vice versa
ifeq ($(COMMAND_ARGS), ssh)
	REGEX='s/https:\/\/github.com\//git@github.com:/g'
	$(update_git_urls $REGEX)
	REGEX='s/https:\/\/forge-2.ircam.fr\//git@forge-2.ircam.fr:/g'
	$(update_git_urls  REGEX)
endif

