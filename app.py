import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Movie Rental Analysis", layout="wide")

st.title("🎬 Movie Rental Data Analysis Dashboard")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    actor = pd.read_csv("actor.csv")
    film = pd.read_csv("film.csv")
    rental = pd.read_csv("rental.csv")
    payment = pd.read_csv("payment.csv")
    category = pd.read_csv("category.csv")
    film_category = pd.read_csv("film_category.csv")

    rental["rental_date"] = pd.to_datetime(rental["rental_date"])
    payment["payment_date"] = pd.to_datetime(payment["payment_date"])

    return actor, film, rental, payment, category, film_category

actor, film, rental, payment, category, film_category = load_data()

# ---------------------------
# Feature Engineering
# ---------------------------
actor["full_name"] = actor["first_name"] + " " + actor["last_name"]
rental["rental_month"] = rental["rental_date"].dt.month
payment["payment_month"] = payment["payment_date"].dt.month

# ---------------------------
# KPIs
# ---------------------------
st.header("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", round(payment["amount"].sum(), 2))
col2.metric("Total Rentals", rental.shape[0])
col3.metric("Average Payment", round(payment["amount"].mean(), 2))

# ---------------------------
# Revenue Trend
# ---------------------------
st.header("📈 Monthly Revenue")

monthly_revenue = payment.groupby("payment_month")["amount"].sum()

fig1, ax1 = plt.subplots()
monthly_revenue.plot(ax=ax1)
ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

# ---------------------------
# Top Categories
# ---------------------------
st.header("🏆 Top Categories")

film_cat = film.merge(film_category, on="film_id").merge(category, on="category_id")
top_categories = film_cat["name"].value_counts().head(10)

fig2, ax2 = plt.subplots()
top_categories.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Number of Films")
st.pyplot(fig2)

# ---------------------------
# Payment Distribution
# ---------------------------
st.header("💰 Payment Distribution")

fig3, ax3 = plt.subplots()
payment["amount"].hist(ax=ax3)
ax3.set_xlabel("Amount")
st.pyplot(fig3)

# ---------------------------
# Footer
# ---------------------------
st.write("This dashboard was built using Python and Streamlit.")