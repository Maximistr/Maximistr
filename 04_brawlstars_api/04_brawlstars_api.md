# Brawl Stars API Project

## Overview
This project is a data-driven analytics dashboard for the mobile game **Brawl Stars**. It fetches player information from the official Brawl Stars API, tracks player progression over time, and visualizes key metrics through an interactive dashboard built with Streamlit.

## Project Structure

### Files

- **api_pull.py** - Backend script for fetching and storing player data
  - Retrieves player information from Brawl Stars API
  - Saves player data to JSON format
  - Tracks trophy progression over time in CSV format

- **show_data.py** - Frontend dashboard for data visualization
  - Interactive Streamlit web application
  - Displays three main visualizations:
    - Power level distribution of brawlers
    - Trophy progression over time
    - Brawler ranks distribution

- **requirements.txt** - Python package dependencies
- **.env** - Environment variables (API key for authentication)
- **player_data.json** - Cached player data in JSON format
- **trophies.csv** - Historical trophy tracking data

## Features

### Data Collection
- Fetches real-time player statistics from Brawl Stars API
- Caches player data locally for offline access
- Maintains historical trophy records for trend analysis

### Automated Data Scanning
- Uses **GitHub Actions** to periodically scan for new player data
- Automatically runs data collection on a scheduled interval
- Ensures historical records are continuously updated without manual intervention
- Workflow configuration: `.github/workflows/run_python.yaml`

### Visualization Dashboard
- **Power Levels Chart** - Shows distribution of brawler power levels
- **Trophy Trend Line** - Visualizes player trophy progression over time
- **Rank Distribution Pie Chart** - Displays brawlers categorized by achievement rank

## Setup & Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the `.env` file with your Brawl Stars API key:
   ```
   BS_API_KEY=your_api_key_here
   ```

3. Run the data collection script:
   ```bash
   python api_pull.py
   ```

4. Launch the dashboard:
   ```bash
   streamlit run show_data.py
   ```

## API Integration
- Uses Brawl Stars API (via bsproxy.royaleapi.dev)
- Requires Bearer token authentication
- Player tag format: `#PLAYERTAG` (e.g., `#JRLLR9QU`)

## Technologies Used
- **Requests** - HTTP library for API calls
- **Pandas & NumPy** - Data processing and analysis
- **Plotly** - Interactive chart visualization
- **Streamlit** - Web dashboard framework
- **Python-dotenv** - Environment variable management
- **GitHub Actions** - Automated scheduled data collection and workflow automation
