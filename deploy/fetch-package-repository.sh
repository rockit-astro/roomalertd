#!/bin/bash
# Script to clone the centos-packages repository to deploy/repository/

# Decrypt and install SSH private key so that we can fetch and push to the package repository
mkdir -p "${HOME}/.ssh"

gpg --passphrase "${GPG_PASSPHRASE}" -d deploy/id_rsa.gpg > "${HOME}/.ssh/id_rsa"
chmod 0600 "${HOME}/.ssh/id_rsa"

git clone --branch=master git@github.com:warwick-one-metre/centos-packages.git deploy/repository
