import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

st.set_page_config(page_title="EU Energy Dashboard", page_icon="⚡", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect('data/energy.db')
    
    renewable = pd.read_sql('SELECT * FROM renewable_energy', conn)
    consumption = pd.read_sql('SELECT * FROM energy_consumption', conn)
    production = pd.read_sql('SELECT * FROM energy_production', conn)
    countries = pd.read_sql('SELECT * FROM countries', conn)
    sources = pd.read_sql('SELECT * FROM energy_sources', conn)
    
    conn.close()
    
    renewable = renewable.merge(countries[['country_code', 'country_name']], on='country_code')
    consumption = consumption.merge(countries[['country_code', 'country_name']], on='country_code')
    production = production.merge(countries[['country_code', 'country_name']], on='country_code')
    production = production.merge(sources[['source_name', 'category']], 
                                   left_on='energy_source', right_on='source_name')
    
    return renewable, consumption, production, countries

renewable_df, consumption_df, production_df, countries_df = load_data()

st.title("⚡ European Energy Market Dashboard")
st.markdown("**Analysis of 8 EU countries' energy transition (2020-2024)**")

st.sidebar.header("🎛️ Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=renewable_df['country_name'].unique(),
    default=['Belgium', 'Germany', 'France', 'Netherlands']
)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(renewable_df['year'].min()),
    max_value=int(renewable_df['year'].max()),
    value=(int(renewable_df['year'].min()), int(renewable_df['year'].max()))
)

if not selected_countries:
    st.warning("Please select at least one country")
    st.stop()

filtered_renewable = renewable_df[
    (renewable_df['country_name'].isin(selected_countries)) &
    (renewable_df['year'] >= year_range[0]) &
    (renewable_df['year'] <= year_range[1])
]

filtered_consumption = consumption_df[
    (consumption_df['country_name'].isin(selected_countries)) &
    (consumption_df['year'] >= year_range[0]) &
    (consumption_df['year'] <= year_range[1])
]

filtered_production = production_df[
    (production_df['country_name'].isin(selected_countries)) &
    (production_df['year'] >= year_range[0]) &
    (production_df['year'] <= year_range[1])
]

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_renewable = filtered_renewable['renewable_percentage'].mean()
    st.metric(
        "Avg Renewable %", 
        f"{avg_renewable:.1f}%",
        delta=f"{avg_renewable - 15:.1f}% vs 15% baseline"
    )

with col2:
    total_consumption = filtered_consumption['total_consumption_twh'].sum()
    st.metric(
        "Total Consumption",
        f"{total_consumption:.0f} TWh",
        delta=None
    )

with col3:
    total_solar = filtered_renewable['solar_electricity_twh'].sum()
    st.metric(
        "Total Solar",
        f"{total_solar:.0f} TWh",
        delta=None
    )

with col4:
    total_wind = filtered_renewable['wind_electricity_twh'].sum()
    st.metric(
        "Total Wind",
        f"{total_wind:.0f} TWh",
        delta=None
    )

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Energy Mix", "Comparison", "2030 Targets"])

with tab1:
    st.subheader("Renewable Energy Trends Over Time")
    
    fig = px.line(
        filtered_renewable,
        x='year',
        y='renewable_percentage',
        color='country_name',
        markers=True,
        title='Renewable Energy Percentage by Country'
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Renewable Percentage (%)",
        legend_title="Country",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Solar vs Wind Growth")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_solar = px.line(
            filtered_renewable,
            x='year',
            y='solar_electricity_twh',
            color='country_name',
            title='Solar Electricity Generation',
            markers=True
        )
        fig_solar.update_layout(yaxis_title="Solar (TWh)")
        st.plotly_chart(fig_solar, use_container_width=True)
    
    with col2:
        fig_wind = px.line(
            filtered_renewable,
            x='year',
            y='wind_electricity_twh',
            color='country_name',
            title='Wind Electricity Generation',
            markers=True
        )
        fig_wind.update_layout(yaxis_title="Wind (TWh)")
        st.plotly_chart(fig_wind, use_container_width=True)

with tab2:
    st.subheader("Energy Production Mix")
    
    selected_year_mix = st.selectbox(
        "Select Year for Energy Mix",
        options=sorted(filtered_production['year'].unique(), reverse=True),
        key='mix_year'
    )
    
    production_year = filtered_production[filtered_production['year'] == selected_year_mix]
    
    fig_mix = px.bar(
        production_year,
        x='country_name',
        y='production_twh',
        color='energy_source',
        title=f'Energy Production by Source ({selected_year_mix})',
        labels={'production_twh': 'Production (TWh)', 'country_name': 'Country'}
    )
    fig_mix.update_layout(barmode='stack')
    st.plotly_chart(fig_mix, use_container_width=True)
    
    st.subheader("Fossil vs Renewable Production")
    
    fossil_renewable = production_year.groupby(['country_name', 'category'])['production_twh'].sum().reset_index()
    
    fig_compare = px.bar(
        fossil_renewable,
        x='country_name',
        y='production_twh',
        color='category',
        title=f'Fossil vs Renewable vs Nuclear ({selected_year_mix})',
        barmode='stack',
        color_discrete_map={'Fossil': 'gray', 'Renewable': 'green', 'Nuclear': 'purple'}
    )
    st.plotly_chart(fig_compare, use_container_width=True)

with tab3:
    st.subheader("Country Comparison")
    
    comparison_year = st.selectbox(
        "Select Year for Comparison",
        options=sorted(filtered_renewable['year'].unique(), reverse=True),
        key='comp_year'
    )
    
    comparison_data = filtered_renewable[filtered_renewable['year'] == comparison_year].sort_values(
        'renewable_percentage', ascending=False
    )
    
    fig_ranking = px.bar(
        comparison_data,
        x='country_name',
        y='renewable_percentage',
        title=f'Renewable Energy Ranking ({comparison_year})',
        color='renewable_percentage',
        color_continuous_scale='RdYlGn'
    )
    fig_ranking.update_layout(xaxis_title="Country", yaxis_title="Renewable %")
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    st.subheader("Scatter: Consumption vs Renewable %")
    
    merged_data = filtered_renewable.merge(
        filtered_consumption[['country_code', 'year', 'total_consumption_twh']],
        on=['country_code', 'year']
    )
    
    fig_scatter = px.scatter(
        merged_data,
        x='total_consumption_twh',
        y='renewable_percentage',
        color='country_name',
        size='solar_electricity_twh',
        hover_data=['year'],
        title='Energy Consumption vs Renewable Adoption',
        labels={'total_consumption_twh': 'Consumption (TWh)', 'renewable_percentage': 'Renewable %'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    st.subheader("2030 Climate Targets Progress")
    
    targets = {
        'BEL': 42.5, 'FRA': 40.0, 'NLD': 45.0, 'DEU': 50.0,
        'POL': 32.0, 'ESP': 48.0, 'ITA': 40.0, 'SWE': 65.0
    }
    
    latest_year = filtered_renewable['year'].max()
    latest_data = filtered_renewable[filtered_renewable['year'] == latest_year].copy()
    latest_data['target_2030'] = latest_data['country_code'].map(targets)
    latest_data['gap'] = latest_data['target_2030'] - latest_data['renewable_percentage']
    latest_data = latest_data.sort_values('gap', ascending=False)
    
    fig_targets = go.Figure()
    
    fig_targets.add_trace(go.Bar(
        name='Current %',
        x=latest_data['country_name'],
        y=latest_data['renewable_percentage'],
        marker_color='lightblue'
    ))
    
    fig_targets.add_trace(go.Bar(
        name='Gap to 2030',
        x=latest_data['country_name'],
        y=latest_data['gap'],
        marker_color='coral'
    ))
    
    fig_targets.update_layout(
        barmode='stack',
        title=f'Progress Toward 2030 Renewable Targets (as of {latest_year})',
        xaxis_title='Country',
        yaxis_title='Renewable Percentage (%)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_targets, use_container_width=True)
    
    st.subheader("Target Status")
    
    for _, row in latest_data.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"**{row['country_name']}**")
        with col2:
            st.write(f"Current: {row['renewable_percentage']:.1f}%")
        with col3:
            st.write(f"Target: {row['target_2030']:.1f}%")
        with col4:
            if row['gap'] > 20:
                st.error(f"Gap: {row['gap']:.1f}%")
            elif row['gap'] > 10:
                st.warning(f"Gap: {row['gap']:.1f}%")
            else:
                st.success(f"Gap: {row['gap']:.1f}%")

st.markdown("---")
st.subheader("Key Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("""
    **Main Findings:**
    - Netherlands achieved largest fossil fuel reduction (29.5%)
    - Germany dominates renewable production (222 TWh in 2023)
    - Belgium ranks last among Western neighbors (11.5% renewable)
    - All countries behind 2030 targets at current growth rates
    """)

with insights_col2:
    st.markdown("""
    **Statistical Insights:**
    - Strong correlation between wind capacity and renewable %
    - No correlation between total consumption and renewables
    - Belgium needs 7x acceleration to meet 2030 commitments
    - Wind power drives success more than solar
    """)

st.markdown("---")
st.caption(f"Data: Our World in Data (2020-2024) | Last updated: {datetime.now().strftime('%Y-%m-%d')}")