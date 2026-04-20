"""
Brawl Stars API Data Collection Script
This module fetches player data from the Brawl Stars API and maintains historical trophy records.
"""

import os
import requests
import json
from datetime import date
from dotenv import load_dotenv
import subprocess
import sys
import csv

# Load environment variables from .env file
load_dotenv()

# Player tag to track (format: #TAG)
player_tag = "#JRLLR9QU"

# API credentials loaded from environment variables
API_TOKEN = os.getenv('BS_API_KEY')

# Base URL for Brawl Stars API proxy
URL = "https://bsproxy.royaleapi.dev/v1/"


def get_player(tag):
    """
    Fetch player information from Brawl Stars API.
    
    Args:
        tag (str): Player tag in format #XXXXXXXX
        
    Returns:
        dict: Player data containing stats, brawlers, trophies, etc.
        
    Note:
        - The '#' character is URL-encoded as %23
        - Response is saved to player_data.json for caching
        - Requires valid API token in environment variables
    """
    # Construct API URL - encode '#' as %23 for proper URL formatting
    url = f"{URL}players/{tag.replace('#', '%23')}"
    
    # Set authorization header with Bearer token
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    
    # Make GET request to API
    response = requests.get(url, headers=headers)
    
    # Save full response to JSON file for offline access and dashboard usage
    with open('player_data.json', 'w') as file:
        json.dump(response.json(), file, indent=2)
    
    return response.json()

    
def save_trophies_to_csv(player_data):
    """
    Save player's current trophy count with timestamp to CSV file.
    
    Args:
        player_data (dict): Player data dictionary from API response
        
    Note:
        - Appends to trophies.csv for historical tracking
        - Used to track trophy progression over time
        - CSV format: [Date, Trophies]
    """
    # Extract trophy count from player data (default to 0 if not found)
    trophies = player_data.get('trophies', 0)
    
    # Append new entry to CSV file
    with open('trophies.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write current date and trophy count
        writer.writerow([date.today(), trophies])

        
if __name__ == "__main__":
    # Fetch current player data from API
    player_data = get_player(player_tag)
    
    # Record today's trophy count for historical tracking
    save_trophies_to_csv(player_data)
