import pandas as pd
import streamlit as st

URL = "https://docs.google.com/spreadsheets/d/1l6E_b0RWIk_W4d7paNr9-vSX4SEzuC75FCBAuqxhZbE/export?format=xlsx"

st.title("Dynamic Budget Analyzer")

xls = pd.ExcelFile(URL)

# -------- FILTER MONTH SHEETS --------
exclude = ["RandomList", "Fixed List", "Credit card track", "Income"]

month_sheets = [s for s in xls.sheet_names if s not in exclude]

selected_sheet = st.selectbox("Select Month", sorted(month_sheets))

# -------- FIXED LIST --------
fixed_df = pd.read_excel(xls, sheet_name="Fixed List")
fixed_df.columns = ["Category", "Amount"]
fixed_visible = fixed_df[fixed_df["Amount"].notna()]


st.subheader("Fixed Budget")
st.dataframe(fixed_visible)
st.metric("Total Fixed Budget", fixed_visible["Amount"].sum())

# -------- MONTH DATA --------
df = pd.read_excel(xls, sheet_name=selected_sheet)

df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d"-%m-%Y")

df["Category"] = df["Categories-Fixed"].fillna(df["Categories-Random"])
df = df[df["Category"].notna() & df["Debit"].notna()]
df = df[~df["Category"].str.strip().str.lower().eq("withdrawal")]

# -------- OVERALL --------
st.subheader("Category Spend")
st.bar_chart(df.groupby("Category")["Debit"].sum())

# -------- CATEGORY DRILL --------
selected_cat = st.selectbox(
    "Select Category",
    sorted(df["Category"].unique())
)

cat_df = df[df["Category"] == selected_cat]

st.metric("Total Spent", cat_df["Debit"].sum())

st.subheader("Transactions + Reasons")
st.dataframe(cat_df[["Date","Debit","Reason"]])

st.subheader("Reason Spend")
st.bar_chart(cat_df.groupby("Reason")["Debit"].sum())




