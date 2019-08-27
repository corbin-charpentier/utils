#!/bin/bash

# Note this will only succeed on host xapps-dev2

echo "--Stopping previous instance.."
fw web stop $1 $2

printf "\n--Copying new applicat...\n"
fw web copy $1 $2

printf "\n--Starting up new application...\n"
fw web start $1 $2
fw web running

printf "\n\nDONE\n"

