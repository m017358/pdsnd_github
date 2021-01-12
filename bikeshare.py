import time
import pandas as pd
import numpy as np
import calendar
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #specify valid months to accept from user input
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    #specify valid days to accept from user input
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    #start user interaction
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    
    while True:
        city = input("Please enter the name of the city you would like to analyse (Chicago, New York City or Washington): ")
        if city.lower() in CITY_DATA :
            break
        else:
            print("{} is not a city currently available for analysis...".format(city))
                                   

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter the month you would like to analyse (all, january, february, ... , june): ")
        if month.lower() in months :
            break
        else:
            print("{} is not a valid month to search on...".format(month))

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the day you would like to analyse (all, monday, tuesday, ... sunday): ")
        if day.lower() in days :
            break
        else:
            print("{} is not a valid day of the week to search on...".format(day))

    print('-'*40)
    return city.lower(), month.lower(), day.lower()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df.month.mode().iloc[0]
    most_common_month_name = calendar.month_name[most_common_month]
    
    print('The most common month of travel for paramters specified is:', most_common_month_name.title())
          

    # Display the most common day of week
    most_common_day_of_the_week = df.day_of_week.mode().iloc[0]
    print('The most common day of travel for paramters specified is:', most_common_day_of_the_week.title())


    # Display the most common start hour
    most_common_hour = df.hour.mode().iloc[0]
    print('The most common start hour of travel for paramters specified is:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode().iloc[0]
    print('The most common Start Station of travel for paramters specified is:', most_common_start_station.title())


    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode().iloc[0]
    print('The most common End Station of travel for paramters specified is:', most_common_end_station.title())


    # Display most frequent combination of start station and end station trip
    most_common_start_end_station = (df['Start Station'] + ' - ' + df['End Station']).mode().iloc[0]
    print('The most common combination of Start Station and End Station of travel for paramters specified is:' , most_common_start_end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_HH_MM_SS = time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print('The total travel time for paramters specified is (HH:MM:SS):', total_travel_time_HH_MM_SS)


    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_HH_MM_SS = time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    print('The mean travel time for paramters specified is (HH:MM:SS):', mean_travel_time_HH_MM_SS)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of uset types for paramters specified are: \n', df.groupby(['User Type'])['User Type'].count())


    # Display counts of gender
    if "Gender" in df: # Not available in Washington 
        print('\nThe counts of gender for paramters specified are: \n', df.groupby(['Gender'])['Gender'].count())

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df: # Not available in Washington
        print('\nThe earliest year of birth for paramters specified is:', int(df['Birth Year'].min()))
    
        print('\nThe latest year of birth for paramters specified is:', int(df['Birth Year'].max()))
    
        print('\nThe most common year of birth for paramters specified is:', int(df['Birth Year'].mode()))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """Displays raw data on bikeshare users if desired by user"""
    
    print('\nDisplaying Raw Data...\n')
    start_time = time.time()
    
    #Set variables
    i=0
    
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5 
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
 
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
