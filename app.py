import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
   page_title="Amazon Sales Data Analysis",
   page_icon="📊",
   layout="wide",
   initial_sidebar_state="expanded",
)


st.title("Amazon Sales Dashboard📊")
st.write("""
Amazon is a multinational e-commerce company founded by Jeff Bezos in 1994. 
It is recognized as one of the largest online marketplaces in the world, offering a wide range of products such as electronics, fashion, books, and daily essentials. 
In addition to e-commerce, Amazon also provides services in cloud computing (Amazon Web Services), digital streaming, and smart devices.

This dashboard presents an analysis of Amazon sales data in India during **April – June 2022**. 
The goal is to provide a comprehensive overview of sales performance, including product categories, fulfillment methods, sales trends, and top-performing cities. 
With this dashboard, users can gain insights into customer behavior and sales patterns to support business strategies and performance evaluation.
""")
df = pd.read_csv("data_amazon.csv")

## Membuat agar KPI berjejer
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Sales", value="INR 77.31M")
with col2:
    st.metric(label="Total Order", value="116.50K")
with col3:
    st.metric(label="Total Quantity", value="112K")

# --- SIDEBAR FOR FILTERS ---
st.sidebar.header("Filter Your Product")

# Filter by Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.slider(
    "📅 Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter for categories
categories = st.sidebar.multiselect(
   "👚Select Product Categories",
   options=df["Category"].unique(),
   default=list(df["Category"].unique())
)

df_filtered = df[
    (df["Category"].isin(categories)) &
    (df["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

## ROW 1
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("Total Order by Category")

## Visualisasi Total Order by Category
    order_by_category = (
        df_filtered.groupby("Category")["Order ID"].nunique()
        .reset_index(name="Total Orders")
        .sort_values(by="Total Orders", ascending=False)
    )
    # Bar chart pakai Altair biar urut dari terbesar ke terkecil
    bar_chart = alt.Chart(order_by_category).mark_bar(color='#e47911').encode(
        x=alt.X("Category", sort=order_by_category["Category"].tolist()),
        y="Total Orders"
    )
    st.altair_chart(bar_chart, use_container_width=True)
    with st.expander("Interpretation"):
        st.write("""
    The best-selling product category is **Shirts**, with a total of **49,764** units sold. The second most popular category is **T-Shirts**, with **46,265** units sold, showing that apparel dominates customer preferences during the observed period.

    On the other hand, the category with the lowest number of orders is **Watches**, with only **3 units sold**, indicating that demand for accessories is significantly lower compared to clothing items. This trend suggests that customers primarily purchase essential or frequently worn apparel, while luxury or accessory items such as watches receive far less attention.

    From a business perspective, these insights highlight the importance of prioritizing inventory management, promotional strategies, and marketing efforts toward high-demand categories like shirts and T-shirts, while also exploring strategies to boost sales in underperforming categories.
    """)

## Visualisasi Total Sales by Category
with viz_col2:
    st.subheader("Total Sales by Category")
    sales_by_category = (
        df_filtered.groupby("Category")["Amount"].sum()   
        .reset_index(name="Total Sales")
        .sort_values(by="Total Sales", ascending=False)
    )

    bar_chart_sales = alt.Chart(sales_by_category).mark_bar(color='#e47911').encode(
        x=alt.X("Category", sort=sales_by_category["Category"].tolist()),
        y="Total Sales"
    )
    st.altair_chart(bar_chart_sales, use_container_width=True)
    with st.expander("Interpretation"):
        st.write("""
        The most profitable product category is **T-Shirts**, generating a total sales value of **INR 35,529,886**. This is followed by **Shirts**, which contributed **INR 23,120,763** in total sales.

        Although Shirts recorded slightly higher sales volume compared to T-Shirts, the latter produced significantly greater revenue, suggesting that T-Shirts have a higher average selling price or greater profitability per unit. This insight emphasizes the importance of not only tracking sales volume but also analyzing sales value to identify the most financially impactful product categories.
        """)
st.markdown("---")

## ROW 2
viz_col1, viz_col2 = st.columns(2)
COMMON_HEIGHT = 380

#Membuat visualasi monthly sales trend
with viz_col1:
    st.subheader("Monthly Sales Trend")
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], errors='coerce')
    df_filtered['Month'] = df_filtered['Date'].dt.month_name()
    month_ordered = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']

    monthly_sales_trend = df_filtered.groupby('Month')['Amount'].sum().reset_index()

    monthly_sales_trend['Month'] = pd.Categorical(
        monthly_sales_trend['Month'],
        categories=month_ordered,
        ordered=True
    )
    monthly_sales_trend = monthly_sales_trend.sort_values('Month').reset_index(drop=True)
    area_chart = alt.Chart(monthly_sales_trend).mark_area(opacity=0.6, color="#e47911").encode(
        x=alt.X("Month", sort=month_ordered, title="Month"),
        y=alt.Y("Amount", title="Total Sales")
    ).properties(height=COMMON_HEIGHT)

    st.altair_chart(area_chart, use_container_width=True)

    with st.expander("Interpretation"):
        st.write("""
        The monthly sales trend shows a consistent decline after April. The sharp increase observed from March to April should be interpreted with caution, as the data for March only covers a single day (March 31, 2022). This limited data creates a distorted comparison, making April appear as a significant jump in sales performance.

        From April onward, the downward trend indicates a gradual reduction in customer purchasing activity month over month, highlighting the need to further investigate potential seasonal effects, promotional factors, or changes in customer behavior during this period.
        """)

# Daily Sales Trend
with viz_col2:
    st.subheader("Daily Sales Trend")
    df_filtered["Date"] = pd.to_datetime(df_filtered["Date"])
    df_filtered["Month"] = df_filtered["Date"].dt.month_name() 
    df_filtered["Day"] = df_filtered["Date"].dt.day

    months = ["April", "May", "June"] 
    df_use = df_filtered[df_filtered["Month"].isin(months) & (df_filtered["Day"] <= 30)]

    agg = (df_use.groupby(["Day","Month"], as_index=False)["Amount"] .sum() .rename(columns={"Amount": "Total_Sales"}))

    pivot = agg.pivot(index="Day", columns="Month", values="Total_Sales")\
            .reindex(range(1,31))

    df_long = pivot.reset_index().melt(id_vars="Day", var_name="Month", value_name="Total_Sales")
    
    color_scale = alt.Scale(
    domain=["April", "May", "June"],       # urutan sesuai nama kolom
    range=["#e47911", "black", "brown"]  # April=orange, May=blue, June=green
)
    line_chart = alt.Chart(df_long).mark_line(point=True).encode(
        x="Day:O",
        y="Total_Sales:Q",
        color=alt.Color("Month:N",scale=color_scale, legend=alt.Legend(title="Month")),
        tooltip=["Day", "Month", "Total_Sales"]
    ).properties(height=COMMON_HEIGHT
    )

    st.altair_chart(line_chart, use_container_width=True)

    with st.expander("Interpretation"):
        st.write("""
**April**  
Sales fluctuated throughout the month, reaching a peak on **April 14** with a total sales of **INR 1,124,657.27**. After the peak, sales generally declined, hitting the lowest point on **April 28** at **INR 821,087.52**, before slightly recovering toward the end of the month  

**Mei**  
In early May, sales continued to rise, reaching the highest point on **May 3** with **INR 1,209,923.02.** Following this peak, the trend showed a continuous decline, dropping sharply on May 5, and eventually reaching the lowest point on **May 21** at **INR 666,512.08**. Although sales increased slightly after this point, the recovery remained minimal until the end of May.

**Juni**  
Sales began with a decline at the start of June but rebounded after June 3, reaching the highest point on **June 8** with **INR 970,602.98**. Afterward, the trend turned downward again, with a significant drop recorded on **June 29** at **INR 393,957.76**, marking the lowest point of the three-month period.
""")
st.markdown("---")

## ROW 3
viz_col1, viz_col2 = st.columns(2)
#Membuat visualisasi Sales by Fulfillment
with viz_col1:
    st.subheader("Sales by Fulfillment")
    fulfillment_data = df_filtered.groupby('Fulfilment')['Amount'].sum().reset_index()
    pie_chart = alt.Chart(fulfillment_data).mark_arc().encode(
        theta=alt.Theta(field="Amount", type="quantitative"),
        color=alt.Color(field="Fulfilment", type="nominal", scale=alt.Scale(domain=["Merchant", "Amazon"],range=["black", "#e47911"])),
        tooltip=["Fulfilment", "Amount"]
    )
    st.altair_chart(pie_chart, use_container_width=True)
    with st.expander ("Interpretation"):
        st.write("The analysis indicates that customers in India predominantly rely on Amazon’s fulfillment method, which suggests a strong preference for Amazon-managed logistics over merchant-managed services. This could be attributed to factors such as faster delivery times, better reliability, and customer trust in Amazon’s fulfillment network.")

#Membuat visualisasi Sales by Fulfillment
with viz_col2:
    st.subheader("Sales by Ship Service Level")
    ship_service_level = df_filtered.groupby('ship-service-level')['Amount'].sum().reset_index()
    pie_chart_ship = alt.Chart(ship_service_level).mark_arc().encode(
        theta=alt.Theta(field="Amount", type="quantitative"),
        color=alt.Color(field="ship-service-level", type="nominal",scale=alt.Scale(domain=["Standard", "Expedited"],range=["black", "#e47911"])),
        tooltip=["ship-service-level", "Amount"]
    )
    st.altair_chart(pie_chart_ship, use_container_width=True)
    with st.expander("Interpretation"):
        st.write("The analysis shows that customers predominantly choose the **Expedited** shipping service level. This preference indicates that faster delivery is a major priority for customers, even if it may come with higher shipping costs. It reflects the importance of speed and convenience in influencing purchasing decisions.")
st.markdown("---")

viz_col1 = st.columns(1)

## Visualisasi Top 10 Sales by Ship-City
with viz_col1[0]:
    st.subheader("Top 10 Sales by Ship-City")
    city_sales = df_filtered.groupby('ship-city')['Amount'].sum().reset_index(name='Total Sales').sort_values('Total Sales', ascending=False).head(10)
    # Bar chart pakai Altair biar urut dari terbesar ke terkecil
    bar_chart_ship = alt.Chart(city_sales).mark_bar(color='#e47911').encode(
        x=alt.X("ship-city", sort="-y"),
        y="Total Sales"
    )
    st.altair_chart(bar_chart_ship, use_container_width=True)
    with st.expander("Interpretation"):
        st.write("""
        **Bengaluru as the Leading Market**:
        Bengaluru remains the largest contributor to total sales. However, its performance shows a declining trend, with sales decreasing from 2.5M in April to 2.3M in both May and June. This indicates a potential challenge in sustaining growth in the city despite its market dominance.

        **Stable Second Position – Hyderabad**:
        Hyderabad consistently holds the second-largest market share, maintaining relatively stable sales performance between 1.8M and 1.9M. This stability highlights Hyderabad’s reliability as a steady contributor to overall sales.

        **Weaker Markets – Mumbai, Chennai, and New Delhi**:
        Other cities such as Mumbai, Chennai, and New Delhi contribute less to sales compared to Bengaluru and Hyderabad. Their performance also shows a downward trend, with Mumbai being the most significant example, dropping from 1.6M in April to 1.2M in June. This decline may point to weakening customer demand or increased competition in these markets.
            """)
st.markdown("---")

    ## ROW 4
#Melihatkan contoh dataset
viz_col1 = st.columns(1)
with viz_col1[0]:
    st.subheader("Dataset Example")
    st.dataframe(df_filtered.head())

st.markdown("---")
st.write("Data Source: https://www.kaggle.com/datasets/arpit2712/amazonsalesreport")
