import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# 🍭 Streamlit page setup
st.set_page_config(page_title="🌸 Cutesy Sales Dashboard", layout="centered", initial_sidebar_state="collapsed")

# 🍬 Custom cutesy CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #fff0f5;
        color: #6a5acd;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    h1, h2, h3, .stMarkdown {
        color: #d46a6a;
    }
    .stPlotlyChart {
        border: 2px dashed #ffc0cb;
        border-radius: 15px;
        padding: 10px;
        background-color: #fffafa;
    }
    footer {
        visibility: hidden;
    }
    .footer::after {
        content: "🌷 Made with love by your friendly dashboard 💕";
        visibility: visible;
        display: block;
        position: relative;
        text-align: center;
        padding: 10px;
        color: #ff69b4;
    }
    </style>
    <div class="footer"></div>
""", unsafe_allow_html=True)

# 🧸 Database connection
warehouse = "postgresql://faith_bmap_user:LEl3WG9otK9TCLJuqcCkGHriQqKtWDYi@dpg-d0apl3uuk2gs73c20hb0-a.singapore-postgres.render.com/faith_bmap"
engine = create_engine(warehouse, connect_args={"options": "-c client_encoding=utf8"})

# 🍡 Load and cache data
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

df = load_data()

# 🎀 Cutesy title
st.title("🧁 Welcome to Your Cutesy Sales Dashboard!")
st.markdown("✨ Dive into the magical world of product popularity! ✨")

# 🌸 Filter options
if not df.empty:
    product_list = ["All Products"] + sorted(df["Product"].unique().tolist())
    selected_product = st.selectbox("🎀 Select a product to spotlight:", product_list)

    if selected_product != "All Products":
        filtered_df = df[df["Product"] == selected_product]
        subtitle = f"🌟 Spotlight on: **{selected_product}**"
    else:
        filtered_df = df
        subtitle = "🛍️ Showing all most-loved products!"

    st.markdown(subtitle)

    # 🌈 Bar chart
    fig = px.bar(
        filtered_df,
        x="Product",
        y="count",
        title="💗 Product Popularity",
        labels={"count": "💫 Purchases", "Product": "🎀 Product"},
        color="count",
        color_continuous_scale=px.colors.sequential.Pastel,
        text="count",
    )

    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='#fffaf0',
        paper_bgcolor='#fffaf0',
        font=dict(family="Comic Sans MS, cursive", size=14, color="#ff69b4"),
        yaxis=dict(title='💖 Purchase Count', showgrid=True, gridcolor='#ffe4e1'),
        xaxis=dict(title='✨ Product', tickangle=-45),
        title_x=0.5,
        margin=dict(t=60, b=100)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("😿 Oh no! No product data found in the database.")

# 💌 Footer
st.markdown("<br><center>🌼 Thanks for visiting! Stay sparkly! 🌼</center>", unsafe_allow_html=True)
