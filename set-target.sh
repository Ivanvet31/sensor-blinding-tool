#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <new_address>"
    exit 1
fi

NEW_ADDRESS=$1

curl -X POST -H "Content-Type: application/json" -d "\"$NEW_ADDRESS\"" http://botnet.ai-poly.online/address
