import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="ExpenseWEB")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://tailkits.com/hero-section-images-12.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

File = "expenses.csv"

st.markdown("<h1 style='color:#4B872D;'>Expense Tracker</h1>", unsafe_allow_html=True)

if os.path.exists(File):
    df = pd.read_csv(File)
else:
    df = pd.DataFrame(columns=["Item[Name]", "How many", "Amount", "Purpose", "Effective Date", "Date & Time Upload" , "Personnel"])

df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

st.header("Expenses")

col1, col2, col3= st.columns(3)

with col1:
    name = st.text_input("Expense name")
    amount = st.number_input("Amount [Input Total Amount]", min_value=0.0)
with col2:
    how_many = st.text_input("How Many")
    purpose = st.text_input("Purpose [For what?]")

with col3:
    date = st.text_input("Effective Date [mm/dd/yyyy]")
    person = st.text_input("Personnel [Name + POSITION]")

if st.button("Confirm"):
    if name and amount > 0:
        new_row = pd.DataFrame(
            [[name, how_many, amount, purpose,date, datetime.now(), person]],
            columns=df.columns
        )

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(File, index=False)
        st.success("✅ Expense added successfully!")
    else:
        st.warning("⚠️ Please fill all fields correctly.")

st.header("Expense Records")
st.dataframe(df, use_container_width=True)

st.header("Expense Deletor")
if not df.empty:
    df_display = df.reset_index()

    selected_index = st.selectbox(
        "Expense Deleter",
        df_display["index"],
        format_func=lambda x: f"{df.loc[x, 'Item[Name]']} - {df.loc[x, 'Amount']}"
    )

    if st.button("Delete expenses"):
        df = df.drop(index=selected_index).reset_index(drop=True)
        df.to_csv(File, index=False)
        st.success("Removed Successfully")

st.header("Summary")

if not df.empty:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])

    total = df["Amount"].sum()
    st.markdown(
        f"<h3 style='color:orange;'>Total Amount {total:.2f}</h3>",
        unsafe_allow_html=True
    )

    st.subheader("Expenses in PIE")

    item_data = df.groupby("Item[Name]")["Amount"].sum()

    fig1, ax1 = plt.subplots(figsize=(6, 6))
    fig1.patch.set_facecolor("none")
    ax1.pie(item_data, labels=item_data.index, autopct='%1.1f%%')

    st.pyplot(fig1)

st.header("Highest Expenses")

if not df.empty:
    highest = df.loc[df["Amount"].idxmax()]
    st.write("💡 Highest Expense:")
    st.write(highest)