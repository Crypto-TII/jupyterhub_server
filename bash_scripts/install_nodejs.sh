#!/bin/bash

readonly COLOR_RED="\033[0;31m"
readonly COLOR_YELLOW="\033[1;33m"
readonly COLOR_NONE="\e[0m"

function print_error_message() {
  local message=$1
  echo -e "${COLOR_RED}${message}${COLOR_NONE}"
  exit 1
}

function print_status_message() {
  local message=$1
  echo -e "\t => ${COLOR_YELLOW}${message}...${COLOR_NONE}"
}


function validate_root_user() {
    if [[ "${EUID}" -ne 0 ]]; then
        print_error_message "Root permission are required. Please run $0 using sudo"
    fi
}

function install_nodejs_and_dependencies() {
    print_status_message "Installing nodejs"
    if [[ ! -d "/opt/node-v16.16.0-linux-x64" ]]; then
      wget https://nodejs.org/dist/v16.16.0/node-v16.16.0-linux-x64.tar.xz
      tar xfv node-v16.16.0-linux-x64.tar.xz -C /opt/
      export PATH=/opt/node-v16.16.0-linux-x64/bin:$PATH
      npm install -g configurable-http-proxy
      rm node-v16.16.0-linux-x64.tar.xz
    else
      print_status_message "Nodejs is already installed"
    fi
}

function main() {
    validate_root_user
    install_nodejs_and_dependencies
}

main "$@"