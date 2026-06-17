import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data(num_records=500):
    """Generate sample financial data for the dashboard"""
    
    # Date range
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    
    # Categories
    expense_categories = {
        'Food & Dining': ['Groceries', 'Restaurants', 'Coffee', 'Delivery'],
        'Transportation': ['Gas', 'Uber', 'Public Transit', 'Parking'],
        'Entertainment': ['Movies', 'Gaming', 'Concerts', 'Streaming'],
        'Utilities': ['Electricity', 'Water', 'Internet', 'Phone'],
        'Healthcare': ['Gym', 'Doctor', 'Pharmacy', 'Dental'],
        'Shopping': ['Clothing', 'Electronics', 'Home', 'Books'],
        'Travel': ['Flights', 'Hotels', 'Vacation', 'Car Rental'],
        'Subscriptions': ['Netflix', 'Spotify', 'Software', 'Services']
    }
    
    income_sources = ['Salary', 'Freelance', 'Investments', 'Bonus', 'Side Project']
    
    data = []
    
    # Generate expense transactions
    for _ in range(int(num_records * 0.7)):
        date = start_date + timedelta(days=random.randint(0, 365))
        category = random.choice(list(expense_categories.keys()))
        subcategory = random.choice(expense_categories[category])
        amount = round(random.uniform(5, 500), 2)
        
        data.append({
            'Date': date,
            'Type': 'Expense',
            'Category': category,
            'Sub_Category': subcategory,
            'Description': f'{subcategory} purchase',
            'Amount': amount,
            'Income_Source': None,
            'Budget': random.choice([50, 100, 200, 300, 500, 1000]),
            'Savings_Goal': None
        })
    
    # Generate income transactions
    for _ in range(int(num_records * 0.3)):
        date = start_date + timedelta(days=random.randint(0, 365))
        income_source = random.choice(income_sources)
        
        if income_source == 'Salary':
            amount = round(random.uniform(3000, 5000), 2)
        elif income_source == 'Freelance':
            amount = round(random.uniform(100, 800), 2)
        elif income_source == 'Investments':
            amount = round(random.uniform(50, 500), 2)
        elif income_source == 'Bonus':
            amount = round(random.uniform(500, 2000), 2)
        else:
            amount = round(random.uniform(100, 500), 2)
        
        data.append({
            'Date': date,
            'Type': 'Income',
            'Category': None,
            'Sub_Category': None,
            'Description': f'{income_source} received',
            'Amount': amount,
            'Income_Source': income_source,
            'Budget': None,
            'Savings_Goal': None
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df

def save_sample_data(filename='sample_data.csv'):
    """Generate and save sample data to CSV"""
    df = generate_sample_data(500)
    df.to_csv(filename, index=False)
    print(f"Sample data saved to {filename}")
    return df

if __name__ == "__main__":
    df = save_sample_data('sample_data.csv')
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData Info:")
    print(df.info())
