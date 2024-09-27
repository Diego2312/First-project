import pandas as pd


df_offers = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_offers.csv")
df_orders = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_orders.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)



#Assignment 1

cancel_status_count = df_orders["order_status_key"].value_counts(normalize=True) * 100
cancel_assigned_count = df_orders["is_driver_assigned_key"].value_counts(normalize=True) * 100 #Count of how many cancelations were by clients or by drivers




#Separate ids by is_driver_assigned_key


#Case where driver was assigned

df_driver_assigned = df_orders[df_orders["is_driver_assigned_key"] == 1] #Df with only rows where is_driver_assigned_key is 1

df_driver_assigned_plot = df_driver_assigned.loc[0:, ["order_gk", "order_status_key"]] #Df containing only the order number and status columns

case1_count = df_driver_assigned["order_status_key"].value_counts()#Count client and system cancelations and take percentages


#Case where driver was not assigned

df_driver_not_assigned = df_orders[df_orders["is_driver_assigned_key"] == 0]

df_driver_not_assigned_plot = df_driver_not_assigned.loc[0:, ["order_gk", "order_status_key"]]

case0_count = df_driver_not_assigned["order_status_key"].value_counts()



#Assignment 2

#I need to count the number of times each number appears from 00 to 23 from the HH in the data frame (Hour:Minutes:Seconds)



df2_filtered =df_orders.loc[0: , ["order_gk","order_datetime", "cancellations_time_in_seconds", "is_driver_assigned_key"]] #Filter the data frame to only order_datetime values

df2_filtered['hour'] = df2_filtered["order_datetime"].str.split(":").str[0] #Creating new column hour and assinging its values by spliting the values in the datetime column to extract the hour element.
df2_filtered_sorted = df2_filtered.sort_values(["hour"]) #Sorted by hour

df2_filtered_hour_count = df2_filtered_sorted["hour"].value_counts() #Counts how many times each hour is present in the df.

df2_filtered_hour_count_sorted = df2_filtered_hour_count.sort_index(ascending=False) #Sorted by hour decreasing. In this case used sort_index since we want to sort by the index and not the values.

#Plot





#ASSIGNMENT 3

#Use df2 which contains the needed columns order_datetime  cancellations_time_in_seconds  is_driver_assigned_key hour.
df3 = df2_filtered.copy()

#separate into with and without driver

df3_0 = df3[df3["is_driver_assigned_key"] == 0]
df3_1 = df3[df3["is_driver_assigned_key"] == 1]



#Now for each of them i have to compute the average time to cancelation per hour. for this i can sum all the values that belong to each hour combining this sum with the number of cancelations i have per hour compute the sum

#How to sum values that are equal in some other columns? groupby().mean


df3_0_avgs = df3_0.groupby(["hour"])["cancellations_time_in_seconds"].mean() #Here we are grouping the dataframe by the column hours and apllying the mean of the cancelations on eaach of these these groups. This becomes a series containing the groups as indexes and the means calculated as values
df3_0_avgs = df3_0_avgs.to_frame() #Change back into a data frame so it can be concatenated to the other df
df3_0_avgs = df3_0_avgs.rename(columns={"cancellations_time_in_seconds": "0"}) #Rename the column



df3_1_avgs = df3_1.groupby(["hour"])["cancellations_time_in_seconds"].mean() #Same is done with df3_1
df3_1_avgs = df3_1_avgs.to_frame()
df3_1_avgs = df3_1_avgs.rename(columns={"cancellations_time_in_seconds": "1"})


df3_avgs = pd.concat([df3_0_avgs, df3_1_avgs], axis=1) #Concatenating both dataframes
                                                       #Here the concat would usually concatenate vertically, but we can choose horizontally by setting axis=1


#Trying to remove outliers


#df3_1_out = df3_1.groupby(["hour"])["cancellations_time_in_seconds"].outliers()