import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

# ---- SESSION STATE STORAGE ----
if "incomes" not in st.session_state:
    st.session_state["incomes"] = []
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# ---- SUPPORTED CURRENCIES ----
CURRENCIES = ["USD", "INR", "EUR", "GBP", "JPY"]

# ---- HELPERS ----
def add_income(amount, date, source, notes, currency):
    st.session_state["incomes"].append({
        "amount": float(amount),
        "date": pd.to_datetime(date),
        "source": source,
        "notes": notes,
        "currency": currency
    })

def add_expense(amount, date, category, etype, notes, currency):
    st.session_state["expenses"].append({
        "amount": float(amount),
        "date": pd.to_datetime(date),
        "category": category,
        "type": etype,
        "notes": notes,
        "currency": currency
    })

def show_summary():
    df_income = pd.DataFrame(st.session_state["incomes"])
    df_expense = pd.DataFrame(st.session_state["expenses"])

    st.subheader("📊 Summary")

    if df_income.empty and df_expense.empty:
        st.info("No data yet. Add income or expenses to see your dashboard.")
        return

    # Display metrics grouped by currency
    currencies = sorted(set(df_income["currency"].unique()).union(set(df_expense["currency"].unique())))
    for cur in currencies:
        st.markdown(f"### Currency: {cur}")

        total_income = df_income[df_income["currency"] == cur]["amount"].sum() if not df_income.empty else 0
        total_expense = df_expense[df_expense["currency"] == cur]["amount"].sum() if not df_expense.empty else 0
        balance = total_income - total_expense

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"{cur} {total_income:,.2f}")
        col2.metric("Total Expense", f"{cur} {total_expense:,.2f}")
        col3.metric("Balance", f"{cur} {balance:,.2f}")

        # Charts per currency
        if not df_expense.empty:
            df_cur_exp = df_expense[df_expense["currency"] == cur]
            if not df_cur_exp.empty:
                st.bar_chart(df_cur_exp.groupby("category")["amount"].sum())

        if not df_income.empty:
            df_cur_inc = df_income[df_income["currency"] == cur]
            if not df_cur_inc.empty:
                st.line_chart(df_cur_inc.groupby(df_cur_inc["date"].dt.to_period("M"))["amount"].sum())

# ---- UI ----
st.title("💰 Personal Finance Tracker (Multi-Currency)")

tab1, tab2, tab3 = st.tabs(["➕ Add Income", "➖ Add Expense", "📊 Dashboard"])

with tab1:
    st.header("Add Income")
    with st.form("income_form"):
        col1, col2 = st.columns(2)
        amount = col1.number_input("Amount", min_value=0.0, step=0.01)
        date = col2.date_input("Date", datetime.date.today())
        currency = st.selectbox("Currency", CURRENCIES)
        source = st.selectbox("Source", ["Salary", "Business", "Investments", "Other"])
        notes = st.text_area("Notes (Optional)")
        submitted = st.form_submit_button("Add Income")
        if submitted and amount > 0:
            add_income(amount, date, source, notes, currency)
            st.success(f"Income added in {currency}!")

with tab2:
    st.header("Add Expense")
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        amount = col1.number_input("Amount", min_value=0.0, step=0.01)
        date = col2.date_input("Date", datetime.date.today())
        currency = st.selectbox("Currency", CURRENCIES)
        category = st.selectbox("Category", ["Food", "Transport", "Housing", "Entertainment", "Other"])
        etype = st.radio("Type", ["Need", "Want"])
        notes = st.text_area("Notes (Optional)")
        submitted = st.form_submit_button("Add Expense")
        if submitted and amount > 0:
            add_expense(amount, date, category, etype, notes, currency)
            st.success(f"Expense added in {currency}!")

with tab3:
    show_summary()
