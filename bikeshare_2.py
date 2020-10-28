import time
import pandas as pd
import numpy as np

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
    day, month = 'all', 'all'

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city would you like to explore chicago, new york city or washingto?')
    city = input("the city is: ").lower()
    while city not in CITY_DATA:
        print('Please enter the city correctly')
        city = input("the city is: ").lower()

    # get user input for month (all, january, february, ... , june)
    Filters = ['month', 'day', 'both', 'none']
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    print('would you like to filter the data by month, day, both or none?')
    FilterOption = input("the Filter is: ").lower()

    while FilterOption.lower() not in Filters:
        print('please choose from (month, day, both or none)')
        FilterOption = input("the Filter is: ").lower()

    if FilterOption == 'month':
        print('Please choose a month from (january, february, march, april, may, june)')
        month = input("the month is: ").title()
        while month not in months:
            print('you typed worng inputs, you can startover. please enter the inputs properly \n')
            month = input("the month is: ").title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif FilterOption == 'day':
        print('Please type a day (e.g: Sunday)')
        day = input("the day is: ").title()
        while day not in days:
            print('you typed worng inputs, you can startover. please enter the inputs properly \n')
            day = input("the day is: ").title()

    elif FilterOption == 'both':
        print('Please choose a month (january, february, march, april, may, june) \nand a day (e.g: Sunday)\n')
        month = input("the month is: ").title()
        day = input("the day is: ").title()
        while month not in months or day not in days:
            print('you typed worng inputs, you can startover. please enter the inputs properly \n')
            month = input("the month is: ").title()
            day = input("the day is: ").title()

    elif FilterOption == 'none':
        day, month = 'all', 'all'

    print('-'*40)
    return city, month, day, FilterOption

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day]

    return df

def time_stats(df, FilterOption):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = df['Start Time'].dt.hour
    most_common_day = df['day_of_week'].value_counts().index[0]
    most_common_month = df['month'].value_counts().index[0]

    print(f"the most common starting hour is : {df['hour'].value_counts().index[0]}" + f" , counted for: {df['hour'].value_counts().max()} times")
    # display the most common month
    # display the most common day of week
    # display the most common start hour

    if FilterOption == 'none':
        print(f"the most common month is : {most_common_month}" )
        print(f"and the most common day is : {most_common_day} \n" )
    elif FilterOption == 'day':
        print(f"the most common month is : {most_common_month}" )
    elif FilterOption == 'month':
        print(f"and the most common day is : {most_common_day}" )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"the most common start station is : {df['Start Station'].value_counts().index[0]}" + f" , counted for: {df['Start Station'].value_counts().max()} times")
    # display most commonly used end station
    print(f"and the most common end station is : {df['End Station'].value_counts().index[0]}" + f" , counted for: {df['End Station'].value_counts().max()} times")

    # display most frequent combination of start station and end station trip
    most_frequent_trip = df.groupby(['Start Station', 'End Station']).count().sort_values(by=['Start Time'], ascending=False)
    print(f"and the most frequent trip is from : ({most_frequent_trip.iloc[0].name[0]})" + f" to: ({most_frequent_trip.iloc[0].name[1]})")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"the total travel time is : {df['Trip Duration'].sum()/60} mins.")
    # display mean travel time
    print(f"the average travel time is : {round(df['Trip Duration'].mean()/60, 2)} mins.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"{user_type.index[0]} : {user_type[0]}")
    print(f"{user_type.index[1]} : {user_type[1]} \n")

    if city !='washington' :
        # Display counts of gender
        print('gender and year of birth Stats atr also available for this city')
        print('\nCalculating gender Stats...')
        gender = df['Gender'].value_counts()
        print(f"{gender.index[0]} : {gender.max()}")
        print(f"{gender.index[1]} : {gender.min()}")
        # Display earliest, most recent, and most common year of birth
        print('\nCalculating year of birth Stats...')
        df = df.dropna(axis = 0)
        print(f"the earliest year of birth is : {df['Birth Year'].min()}")
        print(f"the most recent year of birth is : {df['Birth Year'].max()}")
        print(f"the most common year of birth is : {df['Birth Year'].value_counts().index[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    answer = input('would you like to view raw data? type \'yes\' or \'no\' : ')
    count = 0
    while answer.lower() == 'yes':
        print(df.iloc[count:count + 5])
        count += 5
        answer = input('would you like to view more data? type \'yes\' or \'no\' : ')

def main():
    while True:
        city, month, day, FilterOption = get_filters()
        df = load_data(city, month, day)

        time_stats(df, FilterOption)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
