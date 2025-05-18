import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Set Streamlit page config at the very top
st.set_page_config(page_title="Sales Dashboard", layout="centered")

# PostgreSQL connection string
warehouse = "postgresql://faith_bmap_user:LEl3WG9otK9TCLJuqcCkGHriQqKtWDYi@dpg-d0apl3uuk2gs73c20hb0-a.singapore-postgres.render.com/faith_bmap"

# Create SQLAlchemy engine
engine = create_engine(warehouse, connect_args={"options": "-c client_encoding=utf8"})

@st.cache_data
def load_data():
    query = """
        SELECT "Product", COUNT(*) AS count
        FROM all_data
        GROUP BY "Product";
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return pd.DataFrame(result.mappings().all())

# Load data
df = load_data()

# Streamlit UI header
st.title("📊 Sales Dashboard")
st.subheader("🛒 Most Bought Products")

if not df.empty:
    fig = px.bar(
        df,
        x="Product",
        y="count",
        title="Most Bought Products",
        labels={"count": "Number of Purchases", "Product": "Product"},
        color="count",
        color_continuous_scale="Viridis",
        text="count",
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(family="Arial", size=14, color="black"),
        yaxis=dict(title='Count', showgrid=True, gridcolor='LightGray'),
        xaxis=dict(title='Product')
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data found in the 'all_data' table.")