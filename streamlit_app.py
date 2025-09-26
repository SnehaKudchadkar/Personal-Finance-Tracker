import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize session state
if "income" not in st.session_state:
    st.session_state["income"] = []
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# Convert session state to DataFrame
def get_dataframes():
    df_income = pd.DataFrame(st.session_state["income"])
    df_expense = pd.DataFrame(st.session_state["expenses"])
    return df_income, df_expense

def add_income():
    st.header("➕ Add Income")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    source = st.text_input("Source (e.g., Salary, Freelance, Gift)")
    currency = st.selectbox("Currency", ["₹", "$", "€", "£", "¥"])
    date = st.date_input("Date", datetime.today())
    notes = st.text_area("Notes (Optional)")

    if st.button("Add Income"):
        st.session_state["income"].append({
            "amount": amount,
            "source": source,
            "currency": currency,
            "date": str(date),
            "notes": notes
        })
        st.success("Income added successfully!")

def add_expense():
    st.header("➖ Add Expense")
    amount = st.number_input("Amount", min_value=0.0, step=0.01, key="exp_amount")
    category = st.text_input("Category (e.g., Food, Travel, Bills)")
    exp_type = st.selectbox("Type", ["Need", "Want", "Investment", "Insurance"])
    currency = st.selectbox("Currency", ["₹", "$", "€", "£", "¥"], key="exp_currency")
    date = st.date_input("Date", datetime.today(), key="exp_date")
    notes = st.text_area("Notes (Optional)", key="exp_notes")

    if st.button("Add Expense"):
        st.session_state["expenses"].append({
            "amount": amount,
            "category": category,
            "type": exp_type,
            "currency": currency,
            "date": str(date),
            "notes": notes
        })
        st.success("Expense added successfully!")

def show_summary():
    st.header("📊 Summary")

    df_income, df_expense = get_dataframes()

    if df_income.empty and df_expense.empty:
        st.info("No data yet. Add income or expenses to see the summary.")
        return

    # Safely handle missing columns
    currencies_income = set(df_income["currency"].unique()) if "currency" in df_income.columns else set()
    currencies_expense = set(df_expense["currency"].unique()) if "currency" in df_expense.columns else set()
    currencies = sorted(currencies_income.union(currencies_expense))

    if not currencies:
        st.info("No currency data available yet.")
        return

    selected_currency = st.selectbox("Select currency to view summary", currencies)

    # Filter
    income_filtered = df_income[df_income["currency"] == selected_currency] if "currency" in df_income.columns else pd.DataFrame()
    expense_filtered = df_expense[df_expense["currency"] == selected_currency] if "currency" in df_expense.columns else pd.DataFrame()

    total_income = income_filtered["amount"].sum() if "amount" in income_filtered.columns else 0
    total_expense = expense_filtered["amount"].sum() if "amount" in expense_filtered.columns else 0
    balance = total_income - total_expense

    st.metric("Total Income", f"{selected_currency} {total_income:,.2f}")
    st.metric("Total Expense", f"{selected_currency} {total_expense:,.2f}")
    st.metric("Balance", f"{selected_currency} {balance:,.2f}")

    if not expense_filtered.empty and "type" in expense_filtered.columns:
        fig, ax = plt.subplots()
        expense_filtered.groupby("type")["amount"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        ax.set_title("Expenses by Type")
        st.pyplot(fig)

def main():
    st.title("💰 Personal Finance Tracker")

    menu = ["Add Income", "Add Expense", "Summary"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Income":
        add_income()
    elif choice == "Add Expense":
        add_expense()
    elif choice == "Summary":
        show_summary()

if __name__ == "__main__":
    main()
