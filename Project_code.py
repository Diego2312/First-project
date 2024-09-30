import pandas as pd
from matplotlib import pyplot as plt

#Vizualize all columns in df when printing in terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)



#Reading csv files

df_offers = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_offers.csv")
df_orders = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_orders.csv")



#Assignment 1

cancel_status_count = df_orders["order_status_key"].value_counts()
cancel_assigned_count = df_orders["is_driver_assigned_key"].value_counts() #Count of how many cancelations were by clients or by drivers

was_driver_assigned = pd.DataFrame(cancel_assigned_count).reset_index(drop=False) #Reset index and set drop flase so we dont loose previous index and it becomes a new column.
was_driver_assigned["is_driver_assigned_key"] = was_driver_assigned["is_driver_assigned_key"].apply(lambda x: "Yes" if x == 1 else "No") #substitute 1 and 0 for yes and no
was_driver_assigned.rename(columns={"is_driver_assigned_key": "Was driver assigned"}, inplace=True) #Rename column accordingly

who_cancels_plot = pd.DataFrame(cancel_status_count).reset_index(drop=False)
who_cancels_plot["order_status_key"] = who_cancels_plot["order_status_key"].apply(lambda x: "client" if x == 4 else "driver")
who_cancels_plot.rename(columns={"order_status_key": "Who canceled"}, inplace=True)

#Plots

#Who cancels more

plt.bar(who_cancels_plot["Who canceled"], who_cancels_plot["count"]) #Plot bar graph
plt.title("Who cancels more?") #Title
plt.ylabel("People (un)") #Labels

plt.savefig("Who-cancels-more.png") #Save fig
plt.show()


#Was driver assigned

plt.bar(was_driver_assigned["Was driver assigned"], was_driver_assigned["count"])
plt.title("Was driver assigned during cancellation?")
plt.ylabel("People (un)")

plt.savefig("Was-driver-assigned-during-cancellation.png")
plt.show()


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

df2_final = df2_filtered_hour_count.sort_index(ascending=False) #Sorted by hour decreasing. In this case used sort_index since we want to sort by the index and not the values.

df2_plot = pd.DataFrame(df2_final).reset_index()


#Plot

plt.figure(figsize=(8, 7)) #Resize graph

plt.plot(df2_plot["hour"], df2_plot["count"], label="cancellations", marker=".", markersize=10)

plt.title("Cancellations per hour") #Title

plt.yticks(range(0, 1300, 100)) #Ticks

plt.xlabel("Hour of day")
plt.ylabel("Cancellations")

plt.legend() #Show line label

plt.grid() #Show grid

plt.savefig("Cancellations-per-hour.png")
plt.show()



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


df3_final = pd.concat([df3_0_avgs, df3_1_avgs], axis=1) #Concatenating both dataframes
                                                       #Here the concat would usually concatenate vertically, but we can choose horizontally by setting axis=1

#Plots

plt.figure(figsize=(8, 7)) #Resize figure

plt.plot(df3_final.index, df3_final["0"], color="red", label="driver assigned", marker=".", markersize=10) #Plot driver assigned
plt.plot(df3_final.index, df3_final["1"], color="blue", label="driver not assigned", marker=".", markersize=10) #Plot driver not assigned

plt.title("Average time to cancellation per hour") #Title
plt.legend() #Show legend

plt.yticks(range(0, 350, 25))#Ticks

plt.xlabel("Hour") #Labels
plt.ylabel("Average time to cancellation (sec)")

plt.grid() #Show grid

plt.savefig("Average-time-to-cancellation-per-hour.png")
plt.show()



#Assignment 4

# Filter df to m_order_eta and hour

df4 = df_orders.copy()

df4["hour"] = df4["order_datetime"].str.split(":").str[0] #Create new column with hours

df4_filtered =df4.loc[0:, ["order_gk", "m_order_eta", "hour"]] #df filtered

#Group by hour and compute avg eta. I need to handle NaN. avg if only non NaN values

#Handle all NaN values by setting them equal to zero

df4_filtered["m_order_eta"] = df4_filtered["m_order_eta"].apply(lambda x: 0 if pd.isna(x) else x) #NaN equals 0

df4_gp_avg = df4_filtered.groupby(["hour"])["m_order_eta"].mean() #group hour and avg ETA

df4_final = df4_gp_avg.to_frame()


#Plot

plt.figure(figsize=(8,7))

plt.plot(df4_final.index, df4_final["m_order_eta"], label="Average ETA", marker=".", markersize=10)

plt.title("Average time before order arrival per hour")

plt.xlabel("Hour")
plt.ylabel("Avg ETA (sec)")

plt.yticks(range(0, 300, 25))

plt.legend()
plt.grid()

plt.savefig("Average-time-before-order-arrival-per-hour.png")
plt.show()
