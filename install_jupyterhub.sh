#!/bin/bash

readonly COLOR_RED="\033[0;31m"
readonly COLOR_YELLOW="\033[1;33m"
readonly COLOR_GREEN="\033[0;32m"
readonly COLOR_CYAN="\033[0;36m"
readonly COLOR_NONE="\e[0m"
readonly COLOR_WHITE="\033[1;37m"

function print_error_message() {
  local message=$1
  echo -e "${COLOR_RED}${message}${COLOR_NONE}"
  exit 1
}

function print_status_message() {
  local message=$1
  echo -e "\t => ${COLOR_LIGHT_GRAY}${message}...${COLOR_NONE}"
}

function print_message() {
  local message=$1
  echo -e "\t => ${COLOR_NONE}${message}${COLOR_NONE}"
}

function validate_root_user() {
    if [[ "${EUID}" -ne 0 ]]; then
        print_error_message "Root permission are required. Please run $0 using sudo"
    fi
}

function install_nodejs_and_dependencies() {
    print_status_message "Installing nodejs"
    apt-get update
    apt-get install curl virtualenv -y
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
    apt-get update
    apt-get install nodejs -y
    npm install -g configurable-http-proxy
}

function install_jupyterhub() {
    print_status_message "Installing jupyterhub"
    mkdir -p /opt/jupyterhub
    virtualenv /opt/jupyterhub/venv --python /usr/bin/python3
    source /opt/jupyterhub/venv/bin/activate
    pip install jupyterhub 
    pip install --upgrade notebook
    pip install "dask[distributed,dataframe]" dask_labextension
}

function install_service() {
    cp jupyterhub.service /etc/systemd/system/jupyterhub.service
    cp jupyterhub_config.py /opt/jupyterhub/
    systemctl daemon-reload
    systemctl start jupyterhub
}

function main() {
    validate_root_user
    install_nodejs_and_dependencies
    install_virtual_env
    install_jupyterhub
    install_service
}

main "$@"