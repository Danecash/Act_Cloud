import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# 🌸 Set page config
st.set_page_config(page_title="Cutesy Sales Dashboard", layout="centered", page_icon="🛍️")

# 🐣 Custom CSS for cutesy vibe
st.markdown("""
    <style>
        body {
            background-color: #fff0f5;
        }
        .stApp {
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        h1, h2, h3 {
            color: #d291bc;
        }
        .stPlotlyChart {
            border-radius: 15px;
            border: 2px solid #ffb6c1;
            padding: 10px;
            background-color: #fffafc;
        }
    </style>
""", unsafe_allow_html=True)

# 🎀 PostgreSQL connection string
warehouse = "postgresql://faith_bmap_user:LEl3WG9otK9TCLJuqcCkGHriQqKtWDYi@dpg-d0apl3uuk2gs73c20hb0-a.singapore-postgres.render.com/faith_bmap"

# 🎀 Create SQLAlchemy engine
engine = create_engine(warehouse, connect_args={"options": "-c client_encoding=utf8"})

# 🧁 Cached data loader
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

# 🍬 Load data
df = load_data()

# 💗 Header UI
st.title("🛍️✨ Kawaii Sales Dashboard ✨")
st.subheader("🎀 Most Loved Products by Our Customers 💖")

if not df.empty:
    # 🌈 Define cute pastel color scale manually
    pastel_colors = [
        "#ffd1dc", "#fbc4ab", "#cdb4db", "#b5ead7", "#ffdac1", "#e2f0cb"
    ]

    # 🧁 Create bar chart
    fig = px.bar(
        df,
        x="Product",
        y="count",
        title="💗 Product Popularity",
        labels={"count": "💫 Purchases", "Product": "🎀 Product"},
        color="count",
        color_continuous_scale=pastel_colors,
        text="count",
    )
    fig.update_traces(
        texttemplate='%{text:.0f}',
        textposition='outside'
    )
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_tickangle=-35,
        plot_bgcolor='rgba(255,255,255,0.95)',
        paper_bgcolor='rgba(255,240,245,0.8)',
        font=dict(family="Comic Sans MS", size=14, color="black"),
        yaxis=dict(title='💫 Number of Purchases', showgrid=True, gridcolor='LightPink'),
        xaxis=dict(title='🎀 Product'),
        title_font=dict(size=20, color='#d291bc', family='Comic Sans MS')
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ No data found in the 'all_data' table.")
