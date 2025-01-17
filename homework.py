import pandas as pd

# Load the taxi zone lookup data
taxi_zone_lookup = pd.read_csv('taxi_zone_lookup.csv')

# Load the trip data (assuming you have a CSV file with trip data)
# Replace 'trip_data.csv' with the actual file name
trip_data = pd.read_csv('green_tripdata_2019-10.csv')

# Convert pickup and dropoff datetime columns to datetime objects
trip_data['lpep_pickup_datetime'] = pd.to_datetime(trip_data['lpep_pickup_datetime'])
trip_data['lpep_dropoff_datetime'] = pd.to_datetime(trip_data['lpep_dropoff_datetime'])

# Filter data for the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive)
october_trips = trip_data[(trip_data['lpep_pickup_datetime'] >= '2019-10-01') & 
                          (trip_data['lpep_pickup_datetime'] < '2019-11-01')]

# Question 3: Trip Segmentation Count
def trip_segmentation(trips):
    up_to_1_mile = trips[trips['trip_distance'] <= 1].shape[0]
    between_1_and_3_miles = trips[(trips['trip_distance'] > 1) & (trips['trip_distance'] <= 3)].shape[0]
    between_3_and_7_miles = trips[(trips['trip_distance'] > 3) & (trips['trip_distance'] <= 7)].shape[0]
    between_7_and_10_miles = trips[(trips['trip_distance'] > 7) & (trips['trip_distance'] <= 10)].shape[0]
    over_10_miles = trips[trips['trip_distance'] > 10].shape[0]
    return up_to_1_mile, between_1_and_3_miles, between_3_and_7_miles, between_7_and_10_miles, over_10_miles

segmentation_counts = trip_segmentation(october_trips)
print("Trip Segmentation Counts:", segmentation_counts)

# Question 4: Longest trip for each day
longest_trip_per_day = october_trips.loc[october_trips.groupby(october_trips['lpep_pickup_datetime'].dt.date)['trip_distance'].idxmax()]

# Find the day with the longest trip distance
longest_trip_day = longest_trip_per_day.loc[longest_trip_per_day['trip_distance'].idxmax()]['lpep_pickup_datetime'].date()

print("Longest trip day:", longest_trip_day)

# Question 5: Three biggest pickup zones
october_18_trips = trip_data[trip_data['lpep_pickup_datetime'].dt.date == pd.to_datetime('2019-10-18').date()]
top_pickup_zones = october_18_trips.groupby('PULocationID')['total_amount'].sum().sort_values(ascending=False)
top_pickup_zones = top_pickup_zones[top_pickup_zones > 13000].index
top_pickup_zones_names = taxi_zone_lookup[taxi_zone_lookup['LocationID'].isin(top_pickup_zones)]['Zone'].tolist()
print("Top pickup zones:", top_pickup_zones_names)

# Question 6: Largest tip in East Harlem North
east_harlem_north_trips = october_trips[october_trips['PULocationID'] == taxi_zone_lookup[taxi_zone_lookup['Zone'] == 'East Harlem North']['LocationID'].values[0]]
largest_tip_dropoff = east_harlem_north_trips.loc[east_harlem_north_trips['tip_amount'].idxmax()]['DOLocationID']
largest_tip_dropoff_zone = taxi_zone_lookup[taxi_zone_lookup['LocationID'] == largest_tip_dropoff]['Zone'].values[0]
print("Largest tip dropoff zone:", largest_tip_dropoff_zone)