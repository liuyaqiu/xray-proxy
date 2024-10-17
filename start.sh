#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
DOWNLOAD_DIR="xray-bin"
CONFIG_SCRIPT="gen_conf.py"  # Replace with the actual name of your Python script

# Determine platform
case "$(uname -s)" in
    Linux*)     platform="linux";;
    Darwin*)    platform="macos";;
    CYGWIN*|MINGW*|MSYS*) platform="windows";;
    *)          echo "Unsupported platform"; exit 1;;
esac

# Check if the xray-bin directory exists
if [ ! -d "$DOWNLOAD_DIR" ]; then
    echo "Directory $DOWNLOAD_DIR does not exist. Downloading the latest Xray package..."
    
    # Fetch the latest release version
    latest_version="$(wget -qO- --no-check-certificate https://api.github.com/repos/XTLS/Xray-core/releases | jq -r '.[0].tag_name' | cut -d v -f 2)"
    DOWNLOAD_URL="https://github.com/XTLS/Xray-core/releases/download/v${latest_version}/Xray-${platform}-64.zip"
    
    # Download and unzip the package
    echo "Download ${DOWNLOAD_URL}"
    wget -q --show-progress "$DOWNLOAD_URL" -O xray.zip
    unzip -q xray.zip -d "$DOWNLOAD_DIR"
    rm xray.zip
else
    echo "Directory $DOWNLOAD_DIR already exists. Skipping download."
fi

# Run the Python script to generate the config_client.json file
echo "Generating config_client.json..."
./"$CONFIG_SCRIPT"

# Execute the Xray package with exec
echo "Running Xray..."
exec "$DOWNLOAD_DIR/xray" -c config_client.json
