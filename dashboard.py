import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Florida Gun Violence Dashboard", layout="wide")

st.markdown("""<style>.block-container {padding-top: 1rem; padding-bottom: 0rem;} header {visibility: hidden;} </style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Florida_Gun_Death_Rate.csv")
    df = df.iloc[19:] #Year selection 1990 - 2019
    return df

df = load_data()
average_percentage = df["Total Percent by Firearms"].mean()

col_title, col_selector = st.columns([3, 1])
with col_title:
    st.markdown("<h3 style='margin-bottom: 0px;'> Florida Murder by Firearm Rates (Stand your Ground)</h3>", unsafe_allow_html=True)

with col_selector:
    years  = df["Year"].unique()
    selected_year = st.selectbox("Select a year:", years, index=len(years)-1)

year_data = df[df["Year"] == selected_year].iloc[0]

num1, num2, num3, num4 = st.columns(4)

num1.metric(label="Population", 
            value=int(year_data['Population']), 
            delta=f"{year_data['Population Percentage Change']}%",
            delta_color="normal")

num2.metric(label="Murders by Firearm", 
            value=int(year_data['Total by Firearm']), 
            delta=f"{year_data['Total by Firearm Percentage change']}%",
            delta_color="inverse")

num3.metric(label="Murder per 100k hab.", 
            value=f"{year_data['Murder Rate by Firearm per 100000']}")

num4.metric(label="% Murders by firearm", 
            value=f"{year_data['Total Percent by Firearms']}%")

st.markdown("<hr style='margin: 0.5em 0px; border: 1px solid #e6e6e6;'>", unsafe_allow_html=True)

GRAPHIC = 300
MARGINS = dict(l=10, r=10, t=30, b=30)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["Year"], y=df["Total Murders"], mode='lines', line=dict(width=2, color="#837e84", shape='spline'), fill='tozeroy', fillcolor="#837e8479", name="Murders"))
    fig1.add_trace(go.Scatter(x=df["Year"], y=df["Total by Firearm"], mode='lines+markers', line=dict(width=3, color="#D75555", shape='spline'), marker=dict(size=8, color="#D75555"), fill='tozeroy', fillcolor="#A76C6C5A", name="Murder by Firearm"))
    fig1.update_layout(title="Total Murders vs. Murder by Firearm", height=GRAPHIC, margin=MARGINS, template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title="Year", yaxis_title="Number of Murders")
    fig1.update_xaxes(dtick=1, showgrid=False, tickangle=45)

    fig1.add_annotation(x=2005, y=521, text="<b>2005:</b><br>Florida enacted<br>'Stand your Ground' law", showarrow=True, arrowhead=2, arrowcolor="black",
        arrowsize=1, arrowwidth=2, ax=90, ay=30, bordercolor="black", borderwidth=1, borderpad=3, bgcolor="white", font=dict(size=11, color="black"), align="left")

    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["Year"], y=df["Murders Rate per 100,000"], mode='lines', line=dict(width=2, color="#837e84", shape='spline'), fill='tozeroy', fillcolor="#837e8479", name="Murder Rate"))
    fig2.add_trace(go.Scatter(x=df["Year"], y=df["Murder Rate by Firearm per 100000"], mode='lines+markers', line=dict(width=3, color="#F07C34", shape='spline'), marker=dict(size=8, color="#F07C34"), fill='tozeroy', fillcolor="#F07C342D", name="Murder by Firearm Rate"))
    fig2.update_layout(title="Murder by Firearm Rate per 100,000 population", height=GRAPHIC, margin=MARGINS, template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title="Year", yaxis_title="Murder Rate")
    fig2.update_xaxes(dtick=1, showgrid=False, tickangle=45)
    
    fig2.add_annotation(x=2005, y=2.9, text="<b>2005:</b><br>Florida enacted<br>'Stand your Ground' law", showarrow=True, arrowhead=2, arrowcolor="black",
    arrowsize=1, arrowwidth=2, ax=90, ay=30, bordercolor="black", borderwidth=1, borderpad=3, bgcolor="white", font=dict(size=11, color="black"), align="left")
    
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df["Year"], y=df["Population"], mode='lines+markers', line=dict(width=3, color="#0975c3", shape='spline'), marker=dict(size=6, color="#0975c3"), fill='tozeroy', fillcolor='rgba(31, 119, 180, 0.2)', name="Population"))
    fig3.update_layout(title="Population Growth in Florida", height=GRAPHIC, margin=MARGINS, template="plotly_white", showlegend=False,  xaxis_title="Year", yaxis_title="Population (Millions)")
    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    fig4 = go.Figure()
    colores = ['#d62728' if val > average_percentage else '#ff9896' for val in df["Total Percent by Firearms"]]
    fig4.add_trace(go.Bar(x=df["Year"], y=df["Total Percent by Firearms"], marker_color=colores))
    fig4.add_hline(y=average_percentage, line_dash="dot", line_color="#eef2f4")
    fig4.update_layout(title="% of Murders by Firearm", height=GRAPHIC, margin=MARGINS, template="plotly_white", showlegend=False, xaxis_title="Year", yaxis_title="Percentage")
    st.plotly_chart(fig4, use_container_width=True)

with row2_col3:
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=df["Year"], y=df["Total Handgun"], name='Handgun arms', marker_color="#93dc98"))
    fig5.add_trace(go.Bar(x=df["Year"], y=df["Total Other Firearm"], name='Other firearms', marker_color="#50b7e3"))
    fig5.update_layout(title="Division of Firearm Murders", barmode='stack', height=GRAPHIC, margin=MARGINS, template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), xaxis_title="Year", yaxis_title="Murdes")
    st.plotly_chart(fig5, use_container_width=True)