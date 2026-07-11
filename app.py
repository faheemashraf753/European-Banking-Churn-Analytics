import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="European Banking Customer Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

df = pd.read_csv("data/European_Bank.csv")

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------

st.sidebar.title("Filters")

selected_country = st.sidebar.multiselect(
    "Select Country",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[
    (df["Geography"].isin(selected_country)) &
    (df["Gender"].isin(selected_gender))
]

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("🏦 European Banking Customer Churn Analytics Dashboard")

st.markdown("""
This dashboard analyzes customer churn patterns across:
- Geography
- Gender
- Age
- Credit Score
- Customer Engagement
""")

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

total_customers = len(filtered_df)
churned_customers = filtered_df["Exited"].sum()
retained_customers = total_customers - churned_customers
churn_rate = round((churned_customers / total_customers) * 100, 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", total_customers)

with col2:
    st.metric("Churned Customers", churned_customers)

with col3:
    st.metric("Retained Customers", retained_customers)

with col4:
    st.metric("Overall Churn Rate", f"{churn_rate}%")

st.divider()

# ----------------------------------------------------
# Geography Analysis
# ----------------------------------------------------

st.subheader("🌍 Geography Wise Churn Analysis")

geo_churn = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .reset_index()
)

geo_churn["Exited"] *= 100

fig_geo = px.bar(
    geo_churn,
    x="Geography",
    y="Exited",
    title="Churn Rate by Country",
    labels={
        "Exited": "Churn Rate (%)",
        "Geography": "Country"
    }
)

st.plotly_chart(fig_geo, width="stretch")

# ----------------------------------------------------
# Gender Analysis
# ----------------------------------------------------

st.subheader("👨‍💼👩‍💼 Gender Wise Churn Analysis")

gender_churn = (
    filtered_df.groupby("Gender")["Exited"]
    .mean()
    .reset_index()
)

gender_churn["Exited"] *= 100

fig_gender = px.bar(
    gender_churn,
    x="Gender",
    y="Exited",
    title="Churn Rate by Gender",
    labels={
        "Exited": "Churn Rate (%)"
    }
)

st.plotly_chart(fig_gender, width="stretch")

# ----------------------------------------------------
# Age Analysis
# ----------------------------------------------------

filtered_df["AgeGroup"] = pd.cut(
    filtered_df["Age"],
    bins=[0, 30, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)

age_churn = (
    filtered_df.groupby("AgeGroup")["Exited"]
    .mean()
    .reset_index()
)

age_churn["Exited"] *= 100

st.subheader("🎂 Age Group Churn Analysis")

fig_age = px.bar(
    age_churn,
    x="AgeGroup",
    y="Exited",
    title="Churn Rate by Age Group"
)

st.plotly_chart(fig_age, width="stretch")

# ----------------------------------------------------
# Credit Score Analysis
# ----------------------------------------------------

filtered_df["CreditCategory"] = pd.cut(
    filtered_df["CreditScore"],
    bins=[0, 580, 700, 850],
    labels=["Low", "Medium", "High"]
)

credit_churn = (
    filtered_df.groupby("CreditCategory")["Exited"]
    .mean()
    .reset_index()
)

credit_churn["Exited"] *= 100

st.subheader("💳 Credit Score Churn Analysis")

fig_credit = px.bar(
    credit_churn,
    x="CreditCategory",
    y="Exited",
    title="Churn Rate by Credit Score Category"
)

st.plotly_chart(fig_credit, width="stretch")

# ----------------------------------------------------
# Balance Analysis
# ----------------------------------------------------

st.subheader("💰 Balance Distribution")

fig_balance = px.histogram(
    filtered_df,
    x="Balance",
    nbins=30,
    title="Customer Balance Distribution"
)

st.plotly_chart(fig_balance, width="stretch")

# ----------------------------------------------------
# Active Member Analysis
# ----------------------------------------------------

st.subheader("📈 Active Member Analysis")

active_data = (
    filtered_df.groupby("IsActiveMember")["Exited"]
    .mean()
    .reset_index()
)

active_data["Exited"] *= 100

active_data["IsActiveMember"] = active_data["IsActiveMember"].replace(
    {
        0: "Inactive",
        1: "Active"
    }
)

fig_active = px.bar(
    active_data,
    x="IsActiveMember",
    y="Exited",
    title="Churn Rate by Activity Status"
)

st.plotly_chart(fig_active, width="stretch")

# ----------------------------------------------------
# Dataset Preview
# ----------------------------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head(20))

# ----------------------------------------------------
# Business Insights
# ----------------------------------------------------

st.subheader("📌 Key Business Insights")

st.success(
    f"""
    • Overall churn rate is {churn_rate}%.
    
    • Germany shows the highest churn risk in this dataset.
    
    • Customers aged 46-60 exhibit higher churn behaviour.
    
    • Inactive customers are significantly more likely to leave the bank.
    
    • Customer engagement programs should be prioritized.
    """
)