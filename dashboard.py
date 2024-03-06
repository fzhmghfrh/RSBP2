import subprocess

# List of required libraries
required_libraries = ['pandas', 'matplotlib', 'seaborn', 'streamlit', 'babel']

# Install required libraries
for library in required_libraries:
    subprocess.check_call(['pip', 'install', library])

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from statistics import mean
sns.set(style='dark')

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

st.header('Bike Rentals Dashboard :sparkles:')

st.subheader('Bike Rentals Count')
 
col1, col2 = st.columns(2)
 
with col1:
    daily_rents = round(main_df['cnt_x'].mean(), 0)
    st.metric("Average Daily Rentals", value=daily_rents)
 
with col2:
    total_rents = main_df['cnt_y'].sum()
    st.metric("Total Rentals", value=total_rents)
 

# Create a custom color palette
colors = ["#90CAF9", "#FFCC80", "#A5D6A7", "#FFAB91"]  # Add more colors if needed
custom_palette = sns.color_palette(colors)

# Create plots
fig1, (ax1) = plt.subplots(figsize=(10, 6))

# Bar plot for weather_situation distribution of counts with different colors for each category
sns.barplot(x='weathersit_x', y='cnt_x', hue='weathersit_x', data=main_df[main_df['yr_x'] == 0][['mnth_x', 'cnt_x', 'weathersit_x']], ax=ax1, palette=custom_palette, ci=None)
st.subheader('Distribution of Bike Rentals Based on Weather Situation')

# Add legend
legend_labels = ['Summer', 'Spring', 'Fall']  # Customize labels based on your data
ax1.legend(title='Weather Situation', loc='upper right', labels=legend_labels)

# Show plot
st.pyplot(fig1)  

# Combine holiday and workingday into one column
main_df['day_type'] = main_df.apply(lambda row: 'Working Day' if row['workingday_x'] == 1 else 'Holiday or Weekend', axis=1)

# Create the plot
fig2 = plt.figure(figsize=(10, 6))

# Bar plot for distribution of counts based on day type and season
sns.barplot(data=main_df, x='season_x', y='cnt_x', hue='day_type', ci=None)
st.subheader('Distribution of Bike Rentals Based on Day Type per Season')


# Show plot
st.pyplot(fig2)  
