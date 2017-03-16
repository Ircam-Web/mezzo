#!/bin/bash

rsync -a -e "ssh -p 2232" build/ cri@localhost:/srv/vertigo/doc/build/html/wp3-m3/
