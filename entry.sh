#!/bin/bash

if [ ! -f "state.json" ]; then
    echo "Doing a dry run to populate state.json"
    python3 -m scraper.main --dry-run
fi

echo "Registering cron job"
crond -f
