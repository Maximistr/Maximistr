"""
Brawl Stars Analytics Dashboard
This Streamlit application visualizes player statistics including brawler power levels,
trophy progression, and rank distribution through interactive charts.
"""

import plotly.express as px
import json
import pandas as pd
import numpy as np
import csv
import streamlit as st

# Load player data from cached JSON file
with open('player_data.json', 'r') as file:
    data = json.load(file)

# Create three-column layout for side-by-side charts
col1, col2, col3 = st.columns(3)

# Configure Streamlit page layout
st.set_page_config(layout="wide")

# ============================================================================
# DATA PREPARATION
# ============================================================================

# Extract brawler information from player data and convert to DataFrame
brawlers = pd.DataFrame(data["brawlers"])

# Load historical trophy data from CSV file
tropy_data = pd.read_csv('trophies.csv', names=['Date', 'Trophies'])

# Count the frequency of each power level among brawlers
power_levels = brawlers['power'].value_counts()

# Count brawlers by rank and sort them in ascending order
rank_counts = sorted(brawlers['rank'].value_counts().items(), key=lambda x: x[0])
print(rank_counts)

# Convert rank counts to pandas Series for easier manipulation
rank_counts = pd.Series({rank: count for rank, count in rank_counts})

# ============================================================================
# CHART 1: POWER LEVEL DISTRIBUTION
# ============================================================================

# Create bar chart showing distribution of brawlers by power level
power_bars = px.bar(power_levels, x=power_levels.index, y=power_levels.values,
             labels={'x': 'Power Level', 'y': 'Number of Brawlers'},
             title='Distribution of Brawlers by Power Level',
             text=power_levels.values, template='plotly_dark',
             text_auto=False)

# Position value labels above the bars
power_bars.update_traces(textposition='outside')

# Set x-axis ticks to increment by 1 (for each power level)
power_bars.update_layout(xaxis=dict(tickmode='linear', dtick=1))

# ============================================================================
# CHART 2: RANK DISTRIBUTION WITH CUSTOM LABELS
# ============================================================================

def get_rank_label(rank):
    """
    Convert numeric rank to trophy range label.
    
    Args:
        rank (int): Numeric rank from Brawl Stars (1-indexed)
        
    Returns:
        str: Trophy range label (e.g., '0-250', '250-500')
        
    Note:
        - Rank 1: 0-250 trophies
        - Rank 2: 250-500 trophies
        - Rank 3: 500-750 trophies
        - Rank 4: 750-1000 trophies
        - Rank 5+: 1000+ trophies (increments of 1000 per rank)
    """
    if rank == 1:
        return '0-250'
    elif rank == 2:
        return '250-500'
    elif rank == 3:
        return '500-750'
    elif rank == 4:
        return '750-1000'
    elif rank >= 5:
        # Calculate trophy range for higher ranks
        return f'{1000 * (rank - 4)}-{1000 * (rank - 3)}'

# Convert numeric ranks to human-readable trophy range labels
rank_labels = [get_rank_label(rank) for rank in rank_counts.index]

# Define color palette for each rank tier (matches Brawl Stars theme colors)
tier_colors = ["#9a3f2e", "#f67114", "#9895cd", "#faaf0d", "#b26dfd", "#f4639a", "#f4ed66"]

# If there are more than 7 ranks, use the last color for additional tiers
if len(rank_labels) > 7:
    for i in range(len(rank_labels) - 7):
        tier_colors.append("#f4ed66")


# Create pie chart showing distribution of brawlers across rank tiers
rank_pie = px.pie(rank_counts, names=rank_labels, values=rank_counts.values,
             title='Distribution of Brawlers by Rank')

# Apply tier colors to pie slices and display percentage + label inside
rank_pie.update_traces(marker_colors=tier_colors, textinfo='percent+label', textposition='inside')

# ============================================================================
# CHART 3: TROPHY PROGRESSION OVER TIME
# ============================================================================

# Create line chart showing trophy changes over time
tropy_line = px.line(tropy_data, x='Date', y='Trophies',
             labels={'Date': 'Date', 'Trophies': 'Trophies'},
             title='Trophies Over Time',
             template='plotly_dark')

# Set line color to bright yellow to match Brawl Stars branding
tropy_line.update_traces(line_color="#F6FF00")

# ============================================================================
# DISPLAY CHARTS IN DASHBOARD
# ============================================================================

# Display power levels chart in first column
with col1:
    st.write("### Power Levels of Brawlers") 
    st.plotly_chart(power_bars, width="stretch")

# Display trophy trend chart in second column
with col2:
    st.write("### Trophies Over Time")
    st.plotly_chart(tropy_line, width="stretch")

# Display rank distribution chart in third column
with col3:
    st.write("### Ranks of Brawlers")
    st.plotly_chart(rank_pie, width="stretch")
    
