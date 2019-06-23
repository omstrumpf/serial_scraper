#!/bin/bash

echo "Doing a dry run to populate state.json"
python3 -m scraper.main --dry-run

echo "Registering cron job"
crond -f
