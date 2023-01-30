import datetime as dt
from email.mime import image
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from dateutil import parser


theme_plotly = None

st.set_page_config(page_title='NEAR Developer Activity', page_icon= 'Images/near-logo.png', layout='wide')
st.title('Analysis of Developer Activity on NEAR Blockchain')

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] .css-163ttbj e1fqkh3o1l { width: 250px; }
    </style>
    """,
    unsafe_allow_html=True,
)
c1, c2 = st.columns(2)
c1.image(Image.open('Images/NEAR-Protocol.png'))
c2.subheader('What is NEAR?')
c2.write(
    """
    NEAR Protocol is a decentralized application (dApp) platform and Ethereum competitor 
    that focuses on developer and user-friendliness. Its native NEAR tokens are used to pay 
    for transaction fees and storage on the Near crypto platform. NEAR is a Proof-of-Stake 
    blockchain that uses sharding technology to achieve scalability.
    \n 
    NEAR’s native token is also called NEAR, and is used to pay for transaction fees and storage. 
    NEAR tokens can also be staked by token holders who participate in achieving network consensus 
    as transaction validators.
    Projects building on NEAR include Mintbase, a non-fungible token (NFT) minting platform, 
    and Flux, a protocol that allows developers to create markets based on assets, commodities, 
    real-world events, and more.
    """
)

st.subheader('Price Chart')
c1, c2 = st.columns([1,3])
with c1:
    current_price = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/6b0abb21-08e5-4aff-860b-7881ab5213ee/data/latest')
    st.metric(label='**Current Price**', value=str(current_price['HOURLY_PRICE'].values[0]), help='USD')
with c2:
    time_range = st.selectbox(
        'Select the time range',
        [
            "All Time", "24 Hours", "7 Days", "30 Days", "90 Days", "1 Year"
        ],
        key="select_timerange",
    )

hourly_price = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a0ffdf60-8fb8-4305-bd7e-985c9cfbfd08/data/latest')
df = hourly_price.query("BLOCKCHAIN == 'NEAR'")
df['HOUR'] = pd.to_datetime(df['HOUR'])

if time_range == "All Time":
    df = df
elif time_range == "24 Hours":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(hours=24))]
elif time_range == "7 Days":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=7))]
elif time_range == "30 Days":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=30))]
elif time_range == "90 Days":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=90))]
elif time_range == "1 Year":
    df = df[ df['HOUR'] >= (dt.datetime.now()-pd.Timedelta(days=365))]

fig = px.line(df, x='HOUR', y='HOURLY_PRICE', title='Hourly Price Trend of NEAR')
fig.update_layout(legend_title=None, xaxis_title='Hour', yaxis_title='Price (in $)')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


st.header('**Methodology**')
c1,c2,c3 = st.columns([1,1,1])
with c1:
    st.info('**[My Tweet](https://twitter.com/ZazuCoco/status/1618444933433790466)**', icon="📄")
with c2:
    st.info('**[GitHub Repository](https://github.com/zazu9249/near-developer-activity)**', icon="💻")
with c3:
    st.info('**[Queries Collection](https://app.flipsidecrypto.com/velocity/collections/ae31a929-d872-445c-8e50-de18711266d6)**', icon="❓")    
st.write(
    """
    This Dashboard (Near - Developer Activity) was particularly created for the
    **NEAR's Developer Activity** challenge on [**MetricsDAO**](https://metricsdao.xyz).
    The data for this dashboard was imported from the [**Flipside Crypto**](https://flipsidecrypto.xyz)
    data platform by using its **REST API**. 
    This data was curated by using Electric Capital's NEAR sub-ecosystems available through their
    [**GitHub repository**](https://github.com/electric-capital/crypto-ecosystems/tree/master/data/ecosystems/n).
    
    The code for this report is saved and accessible in the **home.py** file of its
    [**GitHub Repository**](https://github.com/zazu9249/near-developer-activity). The links to the SQL queries
    collection is [**Query Collection**](https://app.flipsidecrypto.com/velocity/collections/ae31a929-d872-445c-8e50-de18711266d6)
    """
)

st.header('**Overall Metrics**')
metrics = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/dec1c3d0-c890-453d-a7d8-7ae34e76768c/data/latest')
c1, c2, c3 = st.columns([1,1,1])
with c1:
    st.metric(label='**Number of Organizations**', value=str(metrics['Organizations'].values[0]))
with c2:
    st.metric(label='**Number of Repositories**', value=str(metrics['Repositories'].values[0]))
with c3:
    st.metric(label='**Number of Developers**', value=str(metrics['Developers'].values[0]))

c1, c2, c3 = st.columns([1,1,1])
with c1:
    st.metric(label='**Number of PRs**', value=str(metrics['PRs'].values[0]))
with c2:
    st.metric(label='**Number of GIT Actions**', value=str(metrics['Actions'].values[0]))
with c3:
    st.metric(label='**Number of Issues**', value=str(metrics['Issues'].values[0]))

st.header('**Activity over Time**')

activity_time = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9268584b-cb5d-48ea-a654-dcb089c4bdaa/data/latest')

fig=px.bar(activity_time, title='Number of Active Developers working over Time', x='DATE', y='Developers')
fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title="Number of Developers")
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig=px.bar(activity_time, title='Number of PRs created over Time', x='DATE', y='PRs')
fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title="Number of PRs created")
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

fig=px.bar(activity_time, title='Number of Issues raised over Time', x='DATE', y='Issues')
fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title="Number of Issues")
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

developer_role = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/8ad5c1ad-5d19-4b1c-a8e5-5bdb83a47538/data/latest')
fig = px.pie(developer_role, values='COUNT', names='AUTHORASSOCIATION', title='Developers by Role')
fig.update_layout(showlegend = True)
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1, c2 = st.columns([1,1])
with c1:
    devs_by_org = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/474aee08-d8b9-495a-a9d3-235825c27d7d/data/latest')
    fig = px.pie(devs_by_org, values='NO_OF_DEVELOPERS', names='ORG', title='Popular Organizations by Developers Count')
    fig.update_layout(showlegend = True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    devs_by_repo = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/addc8a16-7625-4341-b9ca-7b0c06fb139c/data/latest')
    fig = px.pie(devs_by_repo, values='NO_OF_DEVELOPERS', names='REPO', title='Popular Repos by Developers Count')
    fig.update_layout(showlegend = True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

