import pandas as pd


df_offers = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_offers.csv")
df_orders = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_orders.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)



#Assignment 1

cancel_status_count = df_orders["order_status_key"].value_counts()
cancel_assigned_count = df_orders["is_driver_assigned_key"].value_counts(normalize=True) * 100 #Count of how many cancelations were by clients or by drivers


#Separate ids by is_driver_assigned_key


#Case where driver was assigned

df_driver_assigned = df_orders[df_orders["is_driver_assigned_key"] == 1] #Df with only rows where is_driver_assigned_key is 1

df_driver_assigned_plot = df_driver_assigned.loc[0:, ["order_gk", "order_status_key"]] #Df containing only the order number and status columns

case1_count = df_driver_assigned["order_status_key"].value_counts(normalize=True) *100 #Count client and system cancelations and take percentages


#Case where driver was not assigned

df_driver_not_assigned = df_orders[df_orders["is_driver_assigned_key"] == 0]

df_driver_not_assigned_plot = df_driver_not_assigned.loc[0:, ["order_gk", "order_status_key"]]

case0_count = df_driver_not_assigned["order_status_key"].value_counts(normalize=True) *100






#Trying to make a df with the case counts

case0_count_temp = case0_count.to_frame()
case0_count_temp = case0_count_temp.rename(columns={"order_status_key": "0"})




case1_count_temp = case1_count.to_frame()
case1_count_temp = case1_count_temp.rename(columns={"order_status_key": "1"})

case_count = pd.concat([case0_count_temp, case1_count_temp])




print(case1_count)

print(" ")

print(case1_count_temp)
