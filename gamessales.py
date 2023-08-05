import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(page_title="Sales Dashboard",page_icon=":bar_chart:",layout="wide", initial_sidebar_state = "auto",)

df=pd.read_csv("vgsales.csv")

df = df[df.Year.notnull()]
st.sidebar.header("Filter")
platform=st.sidebar.multiselect("Select a Platform",
options=df["Platform"].unique(),
default=df["Platform"].unique()
)
genre=st.sidebar.multiselect("Select a Genre",
options=df["Genre"].unique(),
default=df["Genre"].unique()
)
year=st.sidebar.multiselect("Select a Year",
options=df["Year"].unique(),
default=df["Year"].unique()
)
df_selection=df.query("Platform == @platform & Genre == @genre & Year==@year")
st.title(":bar_chart: Video Game Sales")
st.markdown("##")
total_sales=int(df_selection["Global_Sales"].sum())
avg=round(df_selection["Global_Sales"].mean(),2)
n = 1
poppub=df["Publisher"].value_counts()[:n].index.tolist()[0]
left_column,middle_column,right_column=st.columns(3)

with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US ${total_sales:,}")
with middle_column:
    st.subheader("Popular publisher:")
    st.subheader(f"{poppub}")
with right_column:
    st.subheader("Average Sales")
    st.subheader(f"US ${avg:,}")
st.markdown("---")
sales_by_platform=(
df.groupby(by=["Platform"]).sum()[["Global_Sales"]].sort_values(by="Global_Sales")
)
fig_sales=px.bar(
  sales_by_platform,
  x="Global_Sales",
  y=sales_by_platform.index,
  orientation="h",
  title="<b>Sales by Platform</b>",
  color_discrete_sequence=["#0083B8"]*len(sales_by_platform),
  template="plotly_white"
)
fig_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",xaxis=(dict(showgrid=False))
)



sales_by_genre=(
df.groupby(by=["Genre"]).sum()[["Global_Sales"]].sort_values(by="Global_Sales")
)
fig_gen_sales=px.bar(
  sales_by_genre,
  x="Global_Sales",
  y=sales_by_genre.index,
  
  title="<b>Sales by genre</b>",
  color_discrete_sequence=["#0083B8"]*len(sales_by_genre),
  template="plotly_white"
)
fig_gen_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",xaxis=(dict(showgrid=False))
)
left,right=st.columns(2)

left.plotly_chart(fig_gen_sales,use_container_width=True)
right.plotly_chart(fig_sales,use_container_width=True)
hide_st_style="""<style>
                #MainMenu{visibility:hidden;}
                footer {visibility:hidden;}
                header{visibility:hidden}
                </style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)


