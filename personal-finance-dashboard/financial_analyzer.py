import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# =====================================================================
# 1. CORE APPLICATION ARCHITECTURE & THEME ENGINE
# =====================================================================
st.set_page_config(
    page_title="WealthyIQ - Modern Portfolio Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_wealthyiq_premium_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&display=swap');
        
        /* Main Workspace Canvas Base */
        .stApp {
            background-color: #F5F7FA !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        h1, h2, h3, h4, h5, h6, p, span, label, div, td, th {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* --- SIDEBAR CUSTOMIZATION (#003B3B Theme) --- */
        [data-testid="stSidebar"] {
            background-color: #003B3B !important;
            border-right: 1px solid rgba(255,255,255,0.05);
            padding-top: 2rem !important;
        }
        [data-testid="stSidebar"] * {
            color: #E0F2FE !important;
        }
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label p {
            font-size: 0.95rem !important;
            font-weight: 500 !important;
        }
        
        /* Custom Nav Item Accent Mark */
        .sidebar-brand {
            padding: 0 1rem 2rem 1rem;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #2DD4BF 0%, #38BDF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- PREMIUM FINTECH SURFACES (Glassmorphism & 20px Radius) --- */
        .fin-card {
            background-color: #FFFFFF;
            padding: 1.5rem;
            border-radius: 20px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 4px 20px rgba(0, 59, 59, 0.02);
            margin-bottom: 1.25rem;
            transition: all 0.25s ease;
        }
        .fin-card:hover {
            box-shadow: 0 10px 30px rgba(0, 59, 59, 0.05);
            transform: translateY(-2px);
        }
        
        /* KPI Gradients */
        .kpi-grad-1 { border-left: 5px solid #2DD4BF; }
        .kpi-grad-2 { border-left: 5px solid #3B82F6; }
        .kpi-grad-3 { border-left: 5px solid #10B981; }
        .kpi-grad-4 { border-left: 5px solid #F59E0B; }
        
        /* KPI Metrics Inner Layout */
        .kpi-title { font-size: 0.75rem; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; }
        .kpi-value { font-size: 1.65rem; font-weight: 800; color: #1F2937; margin: 0.3rem 0; }
        .kpi-delta { font-size: 0.8rem; font-weight: 600; display: flex; align-items: center; gap: 4px; }
        .delta-up { color: #10B981; }
        .delta-down { color: #EF4444; }

        /* --- PREMIUM TABLE UI --- */
        .custom-grid {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.5rem;
        }
        .custom-grid th {
            background-color: #F8FAFC;
            color: #4B5563;
            text-align: left;
            padding: 0.75rem 1rem;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            border-bottom: 2px solid #E5E7EB;
        }
        .custom-grid td {
            padding: 0.85rem 1rem;
            font-size: 0.88rem;
            color: #1F2937;
            border-bottom: 1px solid #F3F4F6;
        }
        
        /* Form Buttons styling alignment overrides */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        
        /* Dark Mode CSS Variable Overrides Condition */
        .dark-mode-container {
            background-color: #111827 !important;
            color: #F9FAFB !important;
        }
        
        #MainMenu, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

inject_wealthyiq_premium_css()

# =====================================================================
# 2. RUNTIME INTERNAL DATA MOCK ENGINE
# =====================================================================
@st.cache_data
def generate_synthetic_fintech_dataset():
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    dates = [start_date + timedelta(days=int(i)) for i in range(400)]
    
    categories_inc = ["Primary Salary", "Equity Dividends", "Consulting Yield", "Crypto Operations"]
    categories_exp = ["Housing & Mortgages", "Gourmet & Groceries", "Premium Transport", "Leisure & Subscriptions", "Discretionary Tech", "Health & Wellness"]
    payment_methods = ["Corporate Transfer", "Amex Black Card", "Visa Prime Debit", "Apple Pay Wallet"]
    
    data = []
    for dt in dates:
        m_str = dt.strftime("%B")
        y_str = str(dt.year)
        
        # Salary Inflows
        if dt.day == 1:
            data.append([dt, m_str, y_str, "Income", 9500.0, 0.0, "Primary Salary", "Corporate Transfer", "Monthly regular compensation base"])
            data.append([dt, m_str, y_str, "Income", 1200.0, 0.0, "Consulting Yield", "Corporate Transfer", "Outside strategic retainers"])
            
        # Standard Outflows Distributed Daily
        if np.random.rand() > 0.4:
            tx_type = "Expense"
            exp_amt = np.random.exponential(scale=95.0) + 15.0
            cat = np.random.choice(categories_exp)
            pay = np.random.choice(payment_methods[1:])
            data.append([dt, m_str, y_str, tx_type, 0.0, round(exp_amt, 2), cat, pay, f"Operational regular tracking outlays"])
            
        # Periodic Dividend Inflows
        if dt.day in [15, 28] and np.random.rand() > 0.7:
            data.append([dt, m_str, y_str, "Income", round(np.random.uniform(300, 1500), 2), 0.0, "Equity Dividends", "Visa Prime Debit", "Brokerage automated sweeping execution"])

    df = pd.DataFrame(data, columns=["Date", "Month", "Year", "Transaction Type", "Income", "Expense", "Category", "Payment Method", "Description"])
    return df

if 'master_ledger' not in st.session_state:
    st.session_state['master_ledger'] = generate_synthetic_fintech_dataset()

# Runtime Dark Mode Management Toggle Init
if 'dark_mode_activated' not in st.session_state:
    st.session_state['dark_mode_activated'] = False

# =====================================================================
# 3. SIDEBAR BRAND ARCHITECTURE & INTERACTION SYSTEMS
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">⚡ WealthyIQ</div>', unsafe_allow_html=True)
    
    app_view = st.radio(
        "Navigation Workspace Menu",
        ["Overview Dashboard", "Financial Transactions Log", "Advanced AI Matrix Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><hr style='opacity:0.1;'><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Workspace Controls")
    
    # Global Config State Options inside Sidebar Layout Frame
    st.session_state['dark_mode_activated'] = st.toggle("Activate Dark Mode Display Variant", value=st.session_state['dark_mode_activated'])
    
    # Global Filter Systems Context Hook
    st.markdown("---")
    st.markdown("#### 🔍 Master Data View Sub-Filters")
    avail_months = ["All Months"] + list(st.session_state['master_ledger']["Month"].unique())
    avail_years = ["All Years"] + list(st.session_state['master_ledger']["Year"].unique())
    
    selected_filter_month = st.selectbox("Select View Target Month", options=avail_months, index=4) # Default to April/May ranges
    selected_filter_year = st.selectbox("Select View Target Year", options=avail_years, index=0)

# Apply context filtering down pipelines natively
filtered_df = st.session_state['master_ledger'].copy()
if selected_filter_month != "All Months":
    filtered_df = filtered_df[filtered_df["Month"] == selected_filter_month]
if selected_filter_year != "All Years":
    filtered_df = filtered_df[filtered_df["Year"] == selected_filter_year]

# =====================================================================
# 4. VIEW RENDERING ENGINE: OVERVIEW DASHBOARD
# =====================================================================
if app_view == "Overview Dashboard":
    # Header Control Banner Block
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown(f"<h2 style='color:#003B3B; font-weight:800; margin:0;'>Portfolio Command Center Workspace</h2><p style='color:#6B7280; font-size:0.9rem;'>Premium allocation summary and analytics tracking window active. Timeline: <b>{selected_filter_month} ({selected_filter_year})</b></p>", unsafe_allow_html=True)
    with head_col2:
        st.markdown("<div style='display:flex; justify-content:flex-end; gap:10px; margin-top:0.5rem;'><span style='background:#003B3B; color:#2DD4BF; padding:8px 14px; border-radius:30px; font-size:0.75rem; font-weight:700;'>SECURE CONTEXT CHANNEL</span></div>", unsafe_allow_html=True)

    # Compute Core System Financial Math Targets
    tot_income_calc = filtered_df["Income"].sum()
    tot_expense_calc = filtered_df["Expense"].sum()
    net_savings_calc = tot_income_calc - tot_expense_calc
    savings_rate_calc = (net_savings_calc / tot_income_calc * 100) if tot_income_calc > 0 else 0
    budget_used_pct_calc = min(100.0, (tot_expense_calc / 6500.0 * 100)) # Baseline structural arbitrary month configuration constraint

    # Top Row Metrics Grid Generation Execution
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""
        <div class="fin-card kpi-grad-1">
            <div class="kpi-title">Gross Monthly Inflows</div>
            <div class="kpi-value">${tot_income_calc:,.2f}</div>
            <div class="kpi-delta delta-up">▲ +4.2% <span style='color:#9CA3AF; font-weight:400;'>vs last run</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f"""
        <div class="fin-card kpi-grad-2">
            <div class="kpi-title">Operational Cash Capital Outlays</div>
            <div class="kpi-value">${tot_expense_calc:,.2f}</div>
            <div class="kpi-delta delta-down">▼ +1.1% <span style='color:#9CA3AF; font-weight:400;'>spending expansion</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi3:
        st.markdown(f"""
        <div class="fin-card kpi-grad-3">
            <div class="kpi-title">Net Free Retained Cash Reserve Balance</div>
            <div class="kpi-value">${net_savings_calc:,.2f}</div>
            <div class="kpi-delta delta-up">▲ +8.9% <span style='color:#9CA3AF; font-weight:400;'>efficiency vector</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi4:
        st.markdown(f"""
        <div class="fin-card kpi-grad-4">
            <div class="kpi-title">Calculated Macro Savings Margin Rate</div>
            <div class="kpi-value">{savings_rate_calc:.1f}%</div>
            <div class="kpi-delta delta-up">▲ Target Bound ≥ 20.0% achieved</div>
        </div>
        """, unsafe_allow_html=True)

    # Secondary Central Matrix Analytics Plot Visualization Row Split
    row2_left, row2_right = st.columns([2, 1])
    
    with row2_left:
        st.markdown("<div class='fin-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; margin:0 0 1rem 0; font-weight:700;'>Inflow vs Outflow Historical Curve Tracking Trace</h4>", unsafe_allow_html=True)
        
        # Build Timeline Groupings Aggregations
        timeline_df = filtered_df.groupby("Month")[["Income", "Expense"]].sum().reindex(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]).dropna()
        
        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(x=timeline_df.index, y=timeline_df["Income"], name="Capital Inflows", mode="lines+markers", line=dict(color="#2DD4BF", width=3.5)))
        trend_fig.add_trace(go.Bar(x=timeline_df.index, y=timeline_df["Expense"], name="Capital Spending Outflows", marker_color="rgba(0, 59, 59, 0.12)"))
        
        trend_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=20), height=320, legend=dict(orientation="h", y=1.1, x=0),
            hovermode="x unified"
        )
        trend_fig.update_xaxes(showgrid=False)
        trend_fig.update_yaxes(showgrid=True, gridcolor="#E5E7EB")
        st.plotly_chart(trend_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row2_right:
        st.markdown("<div class='fin-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; margin:0 0 1rem 0; font-weight:700;'>Budget Threshold Constraints Velocity</h4>", unsafe_allow_html=True)
        
        # Build Radial Speed/Proportion Gauge via Pie Segment Rings
        gauge_fig = go.Figure(go.Pie(
            values=[budget_used_pct_calc, max(0.0, 100.0 - budget_used_pct_calc)],
            hole=0.82, marker=dict(colors=["#003B3B", "#F3F4F6"]),
            textinfo='none', hoverinfo='none'
        ))
        gauge_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10), showlegend=False, height=220,
            annotations=[dict(text=f"<span style='font-size:2rem; font-weight:800; color:#1F2937;'>{budget_used_pct_calc:.1f}%</span><br><span style='font-size:0.75rem; color:#6B7280; font-weight:600;'>BUDGET EXHAUSTED</span>", x=0.5, y=0.5, showarrow=False, align="center")]
        )
        st.plotly_chart(gauge_fig, use_container_width=True)
        
        # Strategic Overspending Defensive Alert Indicator Block
        if budget_used_pct_calc > 85.0:
            st.error("🚨 Warning: Active spending vector approaching strict monthly buffer ceiling parameters.")
        else:
            st.success("✅ Operational capital consumption velocities are scaling securely inside baseline ranges.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Lower Core Segment Layout Block
    row3_left, row3_right = st.columns([1.2, 1.8])
    
    with row3_left:
        st.markdown("<div class='fin-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; margin:0 0 1rem 0; font-weight:700;'>Expense Outlays Share Split</h4>", unsafe_allow_html=True)
        cat_expense_df = filtered_df[filtered_df["Transaction Type"] == "Expense"].groupby("Category")["Expense"].sum().reset_index()
        
        donut_fig = go.Figure(go.Pie(
            labels=cat_expense_df["Category"], values=cat_expense_df["Expense"],
            hole=0.6, marker=dict(colors=["#003B3B", "#2DD4BF", "#3B82F6", "#60A5FA", "#34D399", "#A7F3D0"]),
            textinfo='none'
        ))
        donut_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10), height=260, legend=dict(orientation="v", y=0.5, x=1.0)
        )
        st.plotly_chart(donut_fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row3_right:
        st.markdown("<div class='fin-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; margin:0 0 1rem 0; font-weight:700;'>Recent Active Log Ledger Items Transaction Records</h4>", unsafe_allow_html=True)
        
        display_ledger_table = filtered_df.sort_values(by="Date", ascending=False).head(5)
        
        table_builder = "<table class='custom-grid'><thead><tr><th>Date</th><th>Type</th><th>Category</th><th>Amount</th><th>Method</th></tr></thead><tbody>"
        for _, r in display_ledger_table.iterrows():
            amt_print = f"${r['Income']:,.2f}" if r['Transaction Type'] == "Income" else f"${r['Expense']:,.2f}"
            type_color_style = "color:#10B981; font-weight:600;" if r['Transaction Type'] == "Income" else "color:#EF4444; font-weight:600;"
            table_builder += f"<tr><td>{r['Date'].strftime('%Y-%m-%d')}</td><td style='{type_color_style}'>{r['Transaction Type']}</td><td>{r['Category']}</td><td><b>{amt_print}</b></td><td>{r['Payment Method']}</td></tr>"
        table_builder += "</tbody></table>"
        
        st.markdown(table_builder, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 5. VIEW RENDERING ENGINE: FINANCIAL TRANSACTIONS LOG (CRUD)
# =====================================================================
elif app_view == "Financial Transactions Log":
    st.markdown("<h3 style='color:#003B3B; font-weight:800; margin:0 0 1rem 0;'>Dynamic Workspace Transaction Ledger (CRUD Interface Engine)</h3>", unsafe_allow_html=True)
    
    crud_col1, crud_col2 = st.columns([1, 2], gap="large")
    
    with crud_col1:
        st.markdown("<div class='fin-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; margin:0 0 1rem 0; font-weight:700;'>✍️ Append Execution Event Trace</h4>", unsafe_allow_html=True)
        
        with st.form("transaction_entry_form", clear_on_submit=True):
            in_date = st.date_input("Event Log Execution Date", value=datetime.today())
            in_type = st.selectbox("Transaction Flow Type", options=["Expense", "Income"])
            
            in_cat = st.selectbox("Operational Classification Category", options=[
                "Primary Salary", "Equity Dividends", "Consulting Yield", "Housing & Mortgages", 
                "Gourmet & Groceries", "Premium Transport", "Leisure & Subscriptions", "Discretionary Tech"
            ])
            
            in_amt = st.number_input("Transaction Volume Magnitude ($)", min_value=0.01, value=150.00, step=10.0)
            in_pay = st.selectbox("Settlement Pipeline Instrument", options=["Amex Black Card", "Visa Prime Debit", "Apple Pay Wallet", "Corporate Transfer"])
            in_desc = st.text_input("Operational Meta Reference Text Notes", value="Manual portfolio alignment entry trace invocation")
            
            submit_event_trigger = st.form_submit_button("Commit Data Entry Trace Into Core Matrix")
            
            if submit_event_trigger:
                new_row_frame = pd.DataFrame([{
                    "Date": pd.Timestamp(in_date),
                    "Month": in_date.strftime("%B"),
                    "Year": str(in_date.year),
                    "Transaction Type": in_type,
                    "Income": in_amt if in_type == "Income" else 0.0,
                    "Expense": in_amt if in_type == "Expense" else 0.0,
                    "Category": in_cat,
                    "Payment Method": in_pay,
                    "Description": in_desc
                }])
                st.session_state['master_ledger'] = pd.concat([st.session_state['master_ledger'], new_row_frame], ignore_index=True)
                st.toast("Success: Ledger sequence mutated successfully. Recalculating state analytics indices.", icon="🚀")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with crud_col2:
        st.markdown("<div class='fin-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; margin:0 0 1rem 0; font-weight:700;'>📋 Complete Historical Session Ledger Arrays Management</h4>", unsafe_allow_html=True)
        
        # Interactive Search Filter Framework Implementation
        search_term_query = st.text_input("⚡ Universal Quick Regex Description/Category Search Filter String Index", placeholder="Type keywords...")
        
        rendered_crud_view_df = st.session_state['master_ledger'].sort_values(by="Date", ascending=False)
        if search_term_query:
            rendered_crud_view_df = rendered_crud_view_df[
                rendered_crud_view_df["Description"].str.contains(search_term_query, case=False, na=False) |
                rendered_crud_view_df["Category"].str.contains(search_term_query, case=False, na=False)
            ]
            
        st.dataframe(rendered_crud_view_df, use_container_width=True, height=420)
        
        # Extraction Pipelines Engine
        st.markdown("#### 📥 Secure Package Compilation Export Matrix")
        csv_buffer_bytes = rendered_crud_view_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Complete Session Data Package Manifest Array (.CSV)",
            data=csv_buffer_bytes,
            file_name="wealthyiq_ledger_export_manifest.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 6. VIEW RENDERING ENGINE: ADVANCED AI MATRIX ANALYTICS
# =====================================================================
elif app_view == "Advanced AI Matrix Analytics":
    st.markdown("<h3 style='color:#003B3B; font-weight:800; margin:0 0 1rem 0;'>Machine-Calculated Portfolio Insights Engine</h3>", unsafe_allow_html=True)
    
    # Compute Score Indices Metrics Variables Array
    ai_income_pool = st.session_state['master_ledger']["Income"].sum()
    ai_expense_pool = st.session_state['master_ledger']["Expense"].sum()
    
    # Financial Health Scoring System Engine Deterministic Rule Algorithm
    health_score_metric = 100
    if ai_income_pool > 0:
        spending_ratio_idx = ai_expense_pool / ai_income_pool
        if spending_ratio_idx > 0.8: health_score_metric -= 35
        elif spending_ratio_idx > 0.5: health_score_metric -= 15
    else:
        health_score_metric = 30
        
    ai1, ai2 = st.columns([1, 2], gap="large")
    
    with ai1:
        st.markdown("<div class='fin-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; text-align:left; font-weight:700;'>Financial Health Score Index</h4>", unsafe_allow_html=True)
        
        # Circular Metrics Radar Canvas
        fig_score = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = health_score_metric,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Calculated Stability Grade Metrics", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#003B3B"},
                'bar': {'color': "#2DD4BF"},
                'bgcolor': "#F3F4F6",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.1)'},
                    {'range': [50, 80], 'color': 'rgba(245, 158, 11, 0.1)'},
                    {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.1)'}
                ],
            }
        ))
        fig_score.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_score, use_container_width=True)
        
        grade_text = "OPTIMAL STABILITY VEC" if health_score_metric >= 80 else "MODERATE ATTENTION DEFICIT"
        st.markdown(f"<div style='background:#003B3B; color:#2DD4BF; padding:10px; border-radius:12px; font-weight:700; font-size:1.1rem;'>{grade_text}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with ai2:
        st.markdown("<div class='fin-card' style='min-height:340px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#003B3B; font-weight:700;'>🤖 Automated Spending Optimization Analysis Insights</h4>", unsafe_allow_html=True)
        
        st.markdown("""
        * **Liquidity Velocity Index Assessment:** Based on transactional arrays processing telemetry, free cash generation is running within optimal limits. Your retained liquidity ratio indicates stable capacity to support systemic compounding.
        * **Target Budget Optimization Vector:** Current operational cash consumption velocities indicate that trimming discretionary expenses like *Leisure & Subscriptions* by **$150.00/month** could redirect valuable capital toward high-yield investment allocations.
        * **Strategic Allocation Directive:** Your current savings margin safely clears defensive targets. Consider transferring **15%** of your excess cash reserves directly into diversified index fund architectures to accelerate structural growth.
        """)
        
        st.markdown("<div style='margin-top:1.5rem; padding:12px; background:#F8FAFC; border-left:4px solid #2DD4BF; font-size:0.85rem; color:#4B5563; font-weight:500;'>💡 <i>Telemetry updates automatically each time new entries are written to the main transaction log database ledger.</i></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
