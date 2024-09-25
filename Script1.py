import pandas as pd


df_offers = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_offers.csv")
df_orders = pd.read_csv(r"C:\Users\Owner\ACSAI\Extra\First-project\datasets\datasets\data_orders.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)



#Assignment 1

cancel_status_count = df_orders["order_status_key"].value_counts()
cancel_assigned_count = df_orders["is_driver_assigned_key"].value_counts(normalize=True) * 100


#Separate ids by is_driver_assigned_key


#Case where driver was assigned

df_driver_assigned = df_orders[df_orders["is_driver_assigned_key"] == 1]

df_driver_assigned_plot = df_driver_assigned.loc[0:, ["order_gk", "order_status_key"]]

case1_count = df_driver_assigned["order_status_key"].value_counts(normalize=True) *100


#Case where driver was not assigned

df_driver_not_assigned = df_orders[df_orders["is_driver_assigned_key"] == 0]

df_driver_not_assigned_plot = df_driver_not_assigned.loc[0:, ["order_gk", "order_status_key"]]

case0_count = df_driver_not_assigned["order_status_key"].value_counts(normalize=True) *100





print(cancel_assigned_count)


