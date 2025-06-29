import time
import pandas as pd
import numpy as np
from datetime import datetime

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

VALID_CITIES = ['chicago', 'new york city', 'washington']
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
VALID_FILTERS = ['month', 'day', 'both', 'none']

def get_user_input(prompt, valid_options):
    """
    Get user input and validate it against a list of valid options.
    
    Args:
        prompt (str): The message to display to the user when asking for input
        valid_options (list): List of valid input options that the user can choose from
    
    Returns:
        str: The validated user input in lowercase
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input! Please choose from: {', '.join(valid_options).title()}")

def get_filters():
    """
    Ask user to specify a city, month, and day to analyze.
    
    Returns:
        tuple: A tuple containing:
            - city (str): Name of the city to analyze
            - month (str): Name of the month to filter by, or "all" to apply no month filter
            - day (str): Name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    
    city = get_user_input("Would you like to see data for Chicago, New York City, or Washington? ", VALID_CITIES)
    
    filter_choice = get_user_input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter: ", VALID_FILTERS)
    
    month = 'all'
    day = 'all'
    
    if filter_choice == 'month' or filter_choice == 'both':
        month = get_user_input("Which month - January, February, March, April, May, or June? ", VALID_MONTHS[:-1])
    
    if filter_choice == 'day' or filter_choice == 'both':
        day = get_user_input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ", VALID_DAYS[:-1])
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Load data for the specified city and filter by month and day if applicable.
    
    Args:
        city (str): Name of the city to analyze
        month (str): Name of the month to filter by, or "all" to apply no month filter
        day (str): Name of the day of week to filter by, or "all" to apply no day filter
    
    Returns:
        pandas.DataFrame: DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """
    Display statistics on the most frequent times of travel.
    
    Args:
        df (pandas.DataFrame): DataFrame containing bikeshare data
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"Most common month: {months[popular_month - 1]}")
    
    popular_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {popular_day}")
    
    popular_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {popular_hour}")
    
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def station_stats(df):
    """
    Display statistics on the most popular stations and trip.
    
    Args:
        df (pandas.DataFrame): DataFrame containing bikeshare data
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    popular_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {popular_start_station}")
    
    popular_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {popular_end_station}")
    
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print(f"Most frequent combination of start station and end station trip: {popular_trip}")
    
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def trip_duration_stats(df):
    """
    Display statistics on the total and average trip duration.
    
    Args:
        df (pandas.DataFrame): DataFrame containing bikeshare data
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time}")
    
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time: {mean_travel_time}")
    
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def user_stats(df):
    """
    Display statistics on bikeshare users including user types, gender, and birth year.
    
    Args:
        df (pandas.DataFrame): DataFrame containing bikeshare data
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    for user_type, count in user_types.items():
        print(f"{user_type}: {count}")
    
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        for gender, count in gender_counts.items():
            print(f"{gender}: {count}")
    
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year'].dropna()
        earliest_year = int(birth_year.min())
        most_recent_year = int(birth_year.max())
        most_common_year = int(birth_year.mode()[0])
        
        print(f"\nEarliest year of birth: {earliest_year}")
        print(f"Most recent year of birth: {most_recent_year}")
        print(f"Most common year of birth: {most_common_year}")
    
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*40)

def display_raw_data(df):
    """
    Display raw data upon user request, showing 5 rows at a time.
    
    Args:
        df (pandas.DataFrame): DataFrame containing bikeshare data
    """
    start_loc = 0
    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
        
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            
            if start_loc >= len(df):
                print("You have reached the end of the data.")
                break
        elif view_data == 'no':
            break
        else:
            print("Please enter yes or no.")

def main():
    """
    Main function that orchestrates the bikeshare data analysis program.
    Continuously runs the analysis until the user chooses to exit.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()