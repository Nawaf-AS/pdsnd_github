# This program allows users to explore US bikeshare data interactively
# Import necessary libraries
import time
import pandas as pd
import numpy as np
import json

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    # Get user input for city
    while True:
        city = input("Enter city (chicago, new york city, washington): ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter a valid city name.")
    
    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Enter month (all, january, february, ... , june): ").strip().lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month name or 'all'.")
    
    # Get user input for day of the week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Enter day (all, monday, tuesday, ... sunday): ").strip().lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day or 'all'.")
    
    print('-' * 40)
    return city, month, day

# Loads data for the specified city and filters by month and day if applicable
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # Filter by month if needed
    if month != 'all':
        df = df[df['month'] == months.index(month) + 1]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\n{}".format(" Most Frequent Travel Times ".center(78, '=')))
    print("Most common month: {}".format(df['month'].mode()[0]))
    print("Most common day of the week: {}".format(df['day_of_week'].mode()[0]))
    print("Most common start hour: {}".format(df['Start Time'].dt.hour.mode()[0]))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("\n{}".format(" Most Popular Stations and Trip ".center(78, '=')))
    print("Most common start station: {}".format(df['Start Station'].mode()[0]))
    print("Most common end station: {}".format(df['End Station'].mode()[0]))
    df['route'] = df['Start Station'] + " -> " + df['End Station']
    print("Most common trip: {}".format(df['route'].mode()[0]))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("\n{}".format(" Trip Duration ".center(78, '=')))
    print("Total travel time: {}".format(df['Trip Duration'].sum()))
    print("Average travel time: {}".format(df['Trip Duration'].mean()))


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("\n{}".format(" User Stats ".center(78, '=')))
    print("User Types:\n{}".format(df['User Type'].value_counts().to_string()))
    
    if 'Gender' in df.columns:
        print("\nGender Count:\n{}".format(df['Gender'].fillna('Not disclosed').value_counts().to_string()))
    
    if 'Birth Year' in df.columns:
        print("\nEarliest birth year: {}".format(int(df['Birth Year'].min())))
        print("Most recent birth year: {}".format(int(df['Birth Year'].max())))
        print("Most common birth year: {}".format(int(df['Birth Year'].mode()[0])))


def display_raw_data(df):
    """Displays raw data upon user request."""
    row = 0
    while True:
        raw_data = input("\nWould you like to see raw data? Enter yes or no: ").lower()
        if raw_data != 'yes':
            break
        print(df.iloc[row:row+5].to_json(indent=2))
        row += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input("\nWould you like to restart? Enter yes or no: ").lower()
        if restart != 'yes':
            print("\n{}".format(" Analysis ended ".center(78, '*')))
            break

if __name__ == "__main__":
    main()