import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class FinancialAnalyzer:
    """Advanced financial analysis and insights"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['Date'] = pd.to_datetime(self.df['Date'])
    
    def get_overview_metrics(self):
        """Calculate overview metrics"""
        total_income = self.df[self.df['Type'] == 'Income']['Amount'].sum()
        total_expenses = self.df[self.df['Type'] == 'Expense']['Amount'].sum()
        net_savings = total_income - total_expenses
        savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_savings': net_savings,
            'savings_rate': savings_rate,
            'current_balance': net_savings,
            'avg_monthly_income': total_income / 12,
            'avg_monthly_expenses': total_expenses / 12
        }
    
    def get_unusual_expenses(self, threshold_std=2):
        """Detect unusual expenses using statistical methods"""
        expenses = self.df[self.df['Type'] == 'Expense'].copy()
        
        if len(expenses) < 5:
            return pd.DataFrame()
        
        # Calculate z-score for amounts
        mean = expenses['Amount'].mean()
        std = expenses['Amount'].std()
        expenses['z_score'] = np.abs((expenses['Amount'] - mean) / std)
        
        unusual = expenses[expenses['z_score'] > threshold_std].sort_values('Amount', ascending=False)
        return unusual[['Date', 'Category', 'Description', 'Amount']].head(10)
    
    def get_spending_recommendations(self):
        """Generate spending reduction recommendations"""
        expenses = self.df[self.df['Type'] == 'Expense']
        category_spending = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        recommendations = []
        
        # Recommendation 1: Highest spending category
        if len(category_spending) > 0:
            top_category = category_spending.index[0]
            top_amount = category_spending.iloc[0]
            recommendations.append({
                'priority': 'High',
                'insight': f'Highest spending category is {top_category} (${top_amount:.2f})',
                'action': f'Consider reducing {top_category} expenses by 10-15%'
            })
        
        # Recommendation 2: Subscriptions (if any)
        subscriptions = expenses[expenses['Category'] == 'Subscriptions']
        if len(subscriptions) > 0:
            sub_total = subscriptions['Amount'].sum()
            recommendations.append({
                'priority': 'Medium',
                'insight': f'Subscriptions total ${sub_total:.2f}',
                'action': 'Review and cancel unused subscriptions'
            })
        
        # Recommendation 3: Dining out frequency
        dining = expenses[expenses['Category'] == 'Food & Dining']
        if len(dining) > 10:
            dining_total = dining['Amount'].sum()
            recommendations.append({
                'priority': 'Medium',
                'insight': f'Food & Dining: {len(dining)} transactions (${dining_total:.2f})',
                'action': 'Cook at home more often to reduce expenses'
            })
        
        return recommendations[:5]
    
    def calculate_financial_health_score(self):
        """Calculate overall financial health (0-100)"""
        metrics = self.get_overview_metrics()
        
        score = 50  # Base score
        
        # Savings rate (0-30 points)
        savings_rate = metrics['savings_rate']
        if savings_rate >= 20:
            score += 30
        elif savings_rate >= 15:
            score += 25
        elif savings_rate >= 10:
            score += 20
        elif savings_rate >= 5:
            score += 10
        
        # Income stability (0-20 points)
        income_df = self.df[self.df['Type'] == 'Income']
        monthly_income = income_df.groupby(income_df['Date'].dt.to_period('M'))['Amount'].sum()
        if len(monthly_income) > 1:
            income_std = monthly_income.std()
            income_mean = monthly_income.mean()
            cv = income_std / income_mean if income_mean > 0 else 1
            if cv < 0.2:
                score += 20
            elif cv < 0.4:
                score += 15
            elif cv < 0.6:
                score += 10
        
        # Expense control (0-20 points)
        expenses_df = self.df[self.df['Type'] == 'Expense']
        monthly_expenses = expenses_df.groupby(expenses_df['Date'].dt.to_period('M'))['Amount'].sum()
        if len(monthly_expenses) > 1:
            exp_cv = monthly_expenses.std() / monthly_expenses.mean() if monthly_expenses.mean() > 0 else 1
            if exp_cv < 0.3:
                score += 20
            elif exp_cv < 0.5:
                score += 15
        
        return min(100, max(0, score))
    
    def forecast_next_month(self):
        """Forecast next month's expenses and income"""
        # Expense forecast
        expense_df = self.df[self.df['Type'] == 'Expense'].copy()
        expense_df['date_num'] = (expense_df['Date'] - expense_df['Date'].min()).dt.days
        
        if len(expense_df) > 10:
            X = expense_df['date_num'].values.reshape(-1, 1)
            y = expense_df.groupby('date_num')['Amount'].sum().values
            
            if len(y) > 3:
                model = LinearRegression()
                model.fit(expense_df['date_num'].values.reshape(-1, 1), 
                         expense_df['Amount'].values)
                next_days = np.arange(expense_df['date_num'].max(), 
                                     expense_df['date_num'].max() + 30).reshape(-1, 1)
                forecast_expense = model.predict(next_days).sum()
            else:
                forecast_expense = expense_df['Amount'].sum() / 12
        else:
            forecast_expense = expense_df['Amount'].sum() / 12
        
        # Income forecast
        income_df = self.df[self.df['Type'] == 'Income'].copy()
        forecast_income = income_df['Amount'].sum() / 12
        
        return {
            'predicted_expenses': max(0, forecast_expense),
            'predicted_income': forecast_income,
            'predicted_savings': forecast_income - max(0, forecast_expense)
        }
    
    def get_category_breakdown(self):
        """Get spending by category"""
        expenses = self.df[self.df['Type'] == 'Expense']
        return expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    def get_monthly_trends(self):
        """Get monthly income and expense trends"""
        self.df['YearMonth'] = self.df['Date'].dt.to_period('M')
        
        monthly_data = self.df.groupby(['YearMonth', 'Type'])['Amount'].sum().unstack(fill_value=0)
        monthly_data = monthly_data.reset_index()
        monthly_data['YearMonth'] = monthly_data['YearMonth'].astype(str)
        
        return monthly_data
    
    def get_income_sources(self):
        """Get income breakdown by source"""
        income = self.df[self.df['Type'] == 'Income']
        return income.groupby('Income_Source')['Amount'].sum().sort_values(ascending=False)
