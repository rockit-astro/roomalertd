#!/bin/bash
# Script to clean up after fetch-package-repository.sh
shred -u "${HOME}/.ssh/id_rsa"
rm -rf deploy/repository