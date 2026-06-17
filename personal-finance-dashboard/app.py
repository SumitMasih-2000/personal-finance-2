import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

from ui_components import set_page_config, apply_custom_css, get_metric_card_html
from financial_analyzer import FinancialAnalyzer
from generate_data import generate_sample_data

# Page configuration
set_page_config()
apply_custom_css()

# ============ SIDEBAR ============
st.sidebar.markdown("## 📊 Finance Dashboard")
st.sidebar.markdown("---")

# Load data
@st.cache_data
def load_data():
    if os.path.exists('sample_data.csv'):
        df = pd.read_csv('sample_data.csv')
        df['Date'] = pd.to_datetime(df['Date']).dt.date
    else:
        df = generate_sample_data(500)
    return df

df = load_data()

# Sidebar filters
st.sidebar.subheader("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

# Category filter
all_categories = ['All'] + sorted(df[df['Type'] == 'Expense']['Category'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Category", all_categories)

# Income source filter
all_sources = ['All'] + sorted(df[df['Type'] == 'Income']['Income_Source'].dropna().unique().tolist())
selected_source = st.sidebar.selectbox("Income Source", all_sources)

# Filter data
filtered_df = df[
    (df['Date'] >= date_range[0]) & 
    (df['Date'] <= date_range[1])
]

if selected_category != 'All':
    filtered_df = filtered_df[(filtered_df['Category'] == selected_category) | (filtered_df['Type'] == 'Income')]

if selected_source != 'All':
    filtered_df = filtered_df[(filtered_df['Income_Source'] == selected_source) | (filtered_df['Type'] == 'Expense')]

# Initialize analyzer
analyzer = FinancialAnalyzer(filtered_df)

# ============ MAIN CONTENT ============
st.markdown("# 💰 Personal Finance Dashboard")
st.markdown("_Your comprehensive financial overview and insights_")
st.markdown("---")

# ============ FINANCIAL OVERVIEW ============
st.markdown("## 📈 Financial Overview")

col1, col2, col3, col4, col5 = st.columns(5)

metrics = analyzer.get_overview_metrics()

with col1:
    st.markdown(get_metric_card_html(
        "Total Income",
        f"${metrics['total_income']:,.2f}",
        color="success"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(get_metric_card_html(
        "Total Expenses",
        f"${metrics['total_expenses']:,.2f}",
        color="danger"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(get_metric_card_html(
        "Net Savings",
        f"${metrics['net_savings']:,.2f}",
        color="primary"
    ), unsafe_allow_html=True)

with col4:
    color = "success" if metrics['savings_rate'] >= 20 else "warning"
    st.markdown(get_metric_card_html(
        "Savings Rate",
        f"{metrics['savings_rate']:.1f}%",
        color=color
    ), unsafe_allow_html=True)

with col5:
    st.markdown(get_metric_card_html(
        "Current Balance",
        f"${metrics['current_balance']:,.2f}",
        color="primary"
    ), unsafe_allow_html=True)

st.markdown("---")

# ============ TABS ============
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard",
    "🛍️ Spending",
    "💵 Income",
    "🎯 Budget",
    "💡 Insights",
    "🔮 Forecast"
])

# ============ TAB 1: DASHBOARD ============
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Cash Flow")
        monthly_trends = analyzer.get_monthly_trends()
        
        if not monthly_trends.empty:
            fig = go.Figure()
            
            if 'Income' in monthly_trends.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_trends['YearMonth'],
                    y=monthly_trends['Income'],
                    mode='lines+markers',
                    name='Income',
                    line=dict(color='#10b981', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(16, 185, 129, 0.1)'
                ))
            
            if 'Expense' in monthly_trends.columns:
                fig.add_trace(go.Scatter(
                    x=monthly_trends['YearMonth'],
                    y=monthly_trends['Expense'],
                    mode='lines+markers',
                    name='Expenses',
                    line=dict(color='#ef4444', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(239, 68, 68, 0.1)'
                ))
            
            fig.update_layout(
                hovermode='x unified',
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Financial Health Score")
        health_score = analyzer.calculate_financial_health_score()
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Health Score"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#2563eb"},
                'steps': [
                    {'range': [0, 33], 'color': "#fee2e2"},
                    {'range': [33, 66], 'color': "#fef3c7"},
                    {'range': [66, 100], 'color': "#dcfce7"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 2: SPENDING ANALYSIS ============
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Expense by Category")
        category_breakdown = analyzer.get_category_breakdown()
        
        if not category_breakdown.empty:
            fig = go.Figure(data=[go.Pie(
                labels=category_breakdown.index,
                values=category_breakdown.values,
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Set2)
            )])
            
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Spending Categories")
        category_breakdown = analyzer.get_category_breakdown()
        
        if not category_breakdown.empty:
            fig = go.Figure(data=[go.Bar(
                y=category_breakdown.index[::-1],
                x=category_breakdown.values[::-1],
                orientation='h',
                marker=dict(color='#ef4444')
            )])
            
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Amount ($)",
                yaxis_title="Category",
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Spending details
    st.subheader("Detailed Spending")
    expenses = filtered_df[filtered_df['Type'] == 'Expense'].copy()
    
    if not expenses.empty:
        expenses['Date'] = pd.to_datetime(expenses['Date']).dt.strftime('%Y-%m-%d')
        st.dataframe(
            expenses[['Date', 'Category', 'Description', 'Amount']].sort_values('Date', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No expenses in selected period")

# ============ TAB 3: INCOME ANALYSIS ============
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Income by Source")
        income_sources = analyzer.get_income_sources()
        
        if not income_sources.empty:
            fig = go.Figure(data=[go.Bar(
                x=income_sources.index,
                y=income_sources.values,
                marker=dict(color='#10b981')
            )])
            
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Source",
                yaxis_title="Amount ($)",
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Income Contribution %")
        income_sources = analyzer.get_income_sources()
        
        if not income_sources.empty:
            fig = go.Figure(data=[go.Pie(
                labels=income_sources.index,
                values=income_sources.values,
                marker=dict(colors=px.colors.qualitative.Pastel)
            )])
            
            fig.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Income details
    st.subheader("Detailed Income")
    income = filtered_df[filtered_df['Type'] == 'Income'].copy()
    
    if not income.empty:
        income['Date'] = pd.to_datetime(income['Date']).dt.strftime('%Y-%m-%d')
        st.dataframe(
            income[['Date', 'Income_Source', 'Description', 'Amount']].sort_values('Date', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No income in selected period")

# ============ TAB 4: BUDGET TRACKER ============
with tab4:
    st.subheader("Budget vs Actual")
    
    expenses = filtered_df[filtered_df['Type'] == 'Expense']
    
    if not expenses.empty:
        budget_data = expenses.groupby('Category').agg({
            'Amount': 'sum',
            'Budget': 'first'
        }).reset_index()
        
        budget_data = budget_data[budget_data['Budget'].notna()]
        
        if not budget_data.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Budget',
                x=budget_data['Category'],
                y=budget_data['Budget'],
                marker_color='#2563eb'
            ))
            
            fig.add_trace(go.Bar(
                name='Actual',
                x=budget_data['Category'],
                y=budget_data['Amount'],
                marker_color='#ef4444'
            ))
            
            fig.update_layout(
                barmode='group',
                height=500,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Category",
                yaxis_title="Amount ($)",
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Budget summary
            st.subheader("Budget Summary")
            for _, row in budget_data.iterrows():
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(row['Category'], f"${row['Amount']:.2f}", delta=f"Budget: ${row['Budget']:.2f}")
                
                with col2:
                    overage = row['Amount'] - row['Budget']
                    if overage > 0:
                        st.metric("Status", "⚠️ Over Budget", delta=f"${overage:.2f}")
                    else:
                        st.metric("Status", "✅ On Track", delta=f"${abs(overage):.2f}")
                
                with col3:
                    percentage = (row['Amount'] / row['Budget'] * 100) if row['Budget'] > 0 else 0
                    st.metric("Usage", f"{percentage:.1f}%")
    else:
        st.info("No budget data available")

# ============ TAB 5: INSIGHTS ============
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Unusual Expenses")
        unusual = analyzer.get_unusual_expenses()
        
        if not unusual.empty:
            for _, row in unusual.iterrows():
                st.warning(f"**${row['Amount']:.2f}** - {row['Description']} ({row['Category']})")
        else:
            st.info("No unusual expenses detected")
    
    with col2:
        st.subheader("💡 Recommendations")
        recommendations = analyzer.get_spending_recommendations()
        
        for rec in recommendations:
            if rec['priority'] == 'High':
                st.error(f"**{rec['priority']}:** {rec['insight']}")
                st.write(f"→ {rec['action']}")
            elif rec['priority'] == 'Medium':
                st.warning(f"**{rec['priority']}:** {rec['insight']}")
                st.write(f"→ {rec['action']}")
            else:
                st.info(f"**{rec['priority']}:** {rec['insight']}")
                st.write(f"→ {rec['action']}")
    
    # Health insights
    st.markdown("---")
    st.subheader("📊 Financial Health Analysis")
    
    metrics = analyzer.get_overview_metrics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Monthly Income", f"${metrics['avg_monthly_income']:,.2f}")
    
    with col2:
        st.metric("Average Monthly Expenses", f"${metrics['avg_monthly_expenses']:,.2f}")
    
    with col3:
        health_score = analyzer.calculate_financial_health_score()
        st.metric("Health Score", f"{health_score}/100")

# ============ TAB 6: FORECAST ============
with tab6:
    st.subheader("📈 Financial Forecast")
    
    forecast = analyzer.forecast_next_month()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Predicted Monthly Income",
            f"${forecast['predicted_income']:,.2f}"
        )
    
    with col2:
        st.metric(
            "Predicted Monthly Expenses",
            f"${forecast['predicted_expenses']:,.2f}"
        )
    
    with col3:
        st.metric(
            "Predicted Monthly Savings",
            f"${forecast['predicted_savings']:,.2f}",
            delta="Forecast"
        )
    
    st.markdown("---")
    
    # Yearly projection
    st.subheader("Yearly Projection")
    
    yearly_savings = forecast['predicted_savings'] * 12
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### 📊 Yearly Savings Projection
        
        **Monthly Savings:** ${forecast['predicted_savings']:,.2f}
        
        **Yearly Savings:** ${yearly_savings:,.2f}
        
        Based on current spending and income trends, you're projected to save approximately **${yearly_savings:,.2f}** in the next year.
        """)
    
    with col2:
        # Growth chart
        months = np.arange(0, 13)
        cumulative_savings = months * forecast['predicted_savings']
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months,
            y=cumulative_savings,
            mode='lines+markers',
            name='Cumulative Savings',
            line=dict(color='#10b981', width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Months",
            yaxis_title="Cumulative Savings ($)",
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>💰 Personal Finance Dashboard | Built with Streamlit & Plotly</p>
    <p>Data as of: """ + datetime.now().strftime("%B %d, %Y") + """</p>
</div>
""", unsafe_allow_html=True)
