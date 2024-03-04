import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sb
from datetime import datetime, timedelta

# Gathering Data
orders = pd.read_csv("dashboard/orders_dataset.csv")
order_items = pd.read_csv("dashboard/order_items_dataset.csv")
customers = pd.read_csv("dashboard/customers_dataset.csv")
sellers = pd.read_csv("dashboard/sellers_dataset.csv")
geolocation = pd.read_csv("dashboard/geolocation_dataset.csv")

monthly_order = pd.read_csv("dashboard/monthly_order_dataset.csv")
top_monthly_order = pd.read_csv("dashboard/top_monthly_order_dataset.csv")
order_fix = pd.read_csv("dashboard/order_fix_dataset.csv")

st.title('Analisis Data E-commerce')

st.markdown(
    """
    # Data Analytics Dashboard ( E-commerce Public Dataset)
    Hai ini adalah dashboard untuk representasi hasil data yang sudah diolah dari hasil analisis data yang sudah saya lakukan sebelumnya

    - **Nama:** Yoel Mountanus Sitorus
    - **Email:** m004d4ky2327@bangkit.academy
    - **ID Dicoding:** yoel_mountanus

    Table yang digunakan:
    - Order Dataset
    - Order Items Dataset
    - Customer Dataset
    - Seller Dataset
    - Geolocation Dataset
    """
)

st.header("Ini adalah dataset yang saya pakai")

st.markdown("### Orders Dataset")
st.write(orders)

st.markdown("### Order Items Dataset")
st.write(order_items)

st.markdown("### Customers Dataset")
st.write(customers)

st.markdown("### Sellers Dataset")
st.write(sellers)

st.markdown("### Geolocation Dataset")
st.write(geolocation)

st.markdown("## Question 1")
st.markdown("### Monthly State Order Dataset")
st.write(monthly_order)

st.markdown("### Top State Monthly Order Dataset")
st.write(top_monthly_order)

top_monthly_order['date'] = pd.to_datetime(top_monthly_order[['year', 'month']].assign(DAY=1))
fig, ax = plt.subplots()
ax.plot(top_monthly_order['date'], top_monthly_order["0"], marker='o', linestyle='-', color='b')
ax.set_title('Amount over Time (Year-Month)')
ax.set_xlabel('Year-Month')
ax.set_ylabel('Amount')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
st.pyplot(fig)

st.write('> Kesimpulan: Ini cukup menarik karena kita dapat melihat 2 hal yaitu dari data tersebut kecuali 2016 bulan 9 dan 2016 bulan 11 state SP / Sao Paulo di Brazil selalu menjadi konsumen terbesar, dan dari data tersebut dapat dilihat bahwa setiap bulannya pembelian yang "delivered" naik terus setiap bulannya.')

st.markdown("## Question 2")
st.markdown("### Order dengan lama pengiriman dan jarak")

st.write(order_fix)

order_fix.sort_values(by='distance', inplace=True)
order_fix = order_fix[order_fix['distance'] < 4000]

order_fix_view = order_fix[["distance", "carrier_to_customer"]]
# order_fix_view.set_index('distance', inplace=True)
order_fix_view["carrier_to_customer"] = pd.to_timedelta(order_fix_view["carrier_to_customer"])
order_fix_view["carrier_to_customer"] = order_fix_view["carrier_to_customer"].apply(lambda x: x.total_seconds()/3600)

rolling_mean_timedelta = order_fix_view.rolling(window=100).mean()

fig, ax = plt.subplots()
ax.plot(order_fix_view["distance"], rolling_mean_timedelta["carrier_to_customer"], marker='', linestyle='-', color='b')
ax.set_title('Rolling Mean Time Delta over Distance')
ax.set_xlabel('Distance (dalam Kilometer)')
ax.set_ylabel('Rolling Mean Time Delta')
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

order_fix_view = order_fix[["distance", "carrier_to_customer"]]
# order_fix_view.set_index('distance', inplace=True)

order_fix_view["carrier_to_customer"] = pd.to_timedelta(order_fix_view["carrier_to_customer"])
order_fix_view["carrier_to_customer"] = order_fix_view["carrier_to_customer"].apply(lambda x: x.total_seconds()/3600)

rolling_mean_timedelta = order_fix_view.rolling(window=100).mean()

order_fix_view["carrier_to_customer"] = rolling_mean_timedelta["carrier_to_customer"] 

corr = order_fix_view.corr()
fig, ax = plt.subplots()
ax = sb.heatmap(corr, annot=True, cmap='coolwarm', fmt='.3f', linewidths=.5)
ax.set_title('Korelasi')
st.pyplot(fig)


st.write('> Kesimpulan: Dari data hasil visualisasi data yaitu lama pengiriman dengan jarak lalu dilakukan rolling sebanyak 100 windows lalu dirata-ratakan lalu kita dapat melihat tren naik, semakin jauh jaraknya semakin lama jarak waktu deliverynya dengan noise yang cukup signifikan. sehingga kita dapat melihat korelasi yang cukup jelas antara jarak dan waktunya. dan memiliki korelasi yang 91%')

st.markdown("""
## Thanks untuk penilaiannya
""")

