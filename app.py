import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sales Analytics Assistant")

uploaded_file = st.file_uploader(
    "Upload Sales CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    total_revenue = df["Revenue"].sum()
    total_units = df["Quantity"].sum()
    total_products = df["Product"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Units Sold", total_units)
    col3.metric("Products", total_products)

    

    st.subheader("Dataset Preview")
    st.dataframe(df)
    

    revenue_by_product = (
    df.groupby("Product")["Revenue"]
    .sum()
    .reset_index()
    )

    fig = px.bar(
        revenue_by_product,
        x="Product",
        y="Revenue",
        title="Revenue by Product"
    )

    st.plotly_chart(fig, use_container_width=True)



    question = st.text_input(
        "Ask a question about your sales data"
    )

    if question:

        question = question.lower()

        st.subheader("Analytics Response")

        if "producto más vendido" in question or "producto mas vendido" in question:

            best_product = (
                df.groupby("Product")["Quantity"]
                .sum()
                .idxmax()
            )

            units = (
                df.groupby("Product")["Quantity"]
                .sum()
                .max()
            )

            st.success(
                f"El producto más vendido fue {best_product} con {units} unidades vendidas."
            )

        elif "ingreso total" in question:

            total_revenue = df["Revenue"].sum()

            st.success(
                f"El ingreso total fue ${total_revenue:,.2f}"
            )

        elif "categoría" in question or "categoria" in question:

            best_category = (
                df.groupby("Category")["Revenue"]
                .sum()
                .idxmax()
            )

            revenue = (
                df.groupby("Category")["Revenue"]
                .sum()
                .max()
            )

            st.success(
                f"La categoría con mayores ingresos fue {best_category} con ${revenue:,.2f}"
            )

        elif "resumen" in question:

            total_revenue = df["Revenue"].sum()

            total_units = df["Quantity"].sum()

            best_product = (
                df.groupby("Product")["Quantity"]
                .sum()
                .idxmax()
            )

            st.write("### Executive Summary")

            st.write(f"✅ Total Revenue: ${total_revenue:,.2f}")
            st.write(f"✅ Total Units Sold: {total_units}")
            st.write(f"✅ Best Selling Product: {best_product}")

        else:

            st.warning(
                "Question not recognized. Try asking about the best-selling product, total revenue, top category, or executive summary."
            )
