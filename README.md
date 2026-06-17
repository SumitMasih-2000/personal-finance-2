# Personal Finance Dashboard

A comprehensive personal finance dashboard for tracking income and expenses with beautiful visualizations.

## Features

✨ **Income & Expense Tracking**
- Add income entries with source and amount
- Add expenses by category with descriptions
- Delete entries you no longer need

📊 **Visual Analytics**
- Income vs Expenses comparison bar chart
- Expense breakdown by category (doughnut chart)
- Real-time summary cards showing total income, expenses, and balance

💾 **Data Persistence**
- SQLite database for storing all financial data
- Automatic date tracking for entries
- Full CRUD operations

🎨 **User-Friendly Interface**
- Clean, modern dashboard design
- Responsive layout (works on desktop, tablet, mobile)
- Easy-to-use forms for data entry
- Sortable data tables

## Installation

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Setup

1. **Install dependencies**
```bash
npm install
```

2. **Start the server**
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

3. **Open in browser**
```
http://localhost:5000
```

## Usage

### Adding Income
1. Fill in the income source (e.g., "Salary", "Freelance Project")
2. Enter the amount
3. Select the date
4. Click "Add Income"

### Adding Expenses
1. Select an expense category from the dropdown
2. Optionally add a description
3. Enter the amount
4. Select the date
5. Click "Add Expense"

### Viewing Data
- All income and expenses are displayed in tables below the forms
- Summary cards at the top show totals and current balance
- Charts visualize your income vs expenses and expense breakdown by category

### Deleting Entries
- Click the "Delete" button next to any entry
- Confirm the deletion when prompted

## Project Structure

```
personal-finance-dashboard/
├── server.js              # Express server & API endpoints
├── package.json           # Project dependencies
├── public/
│   ├── index.html        # Main dashboard HTML
│   ├── style.css         # Styling
│   └── app.js            # Client-side JavaScript
├── finance.db            # SQLite database (created automatically)
└── README.md             # This file
```

## API Endpoints

### Income Endpoints
- `GET /api/income` - Get all income entries
- `POST /api/income` - Add new income
- `DELETE /api/income/:id` - Delete income entry

### Expense Endpoints
- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Add new expense
- `DELETE /api/expenses/:id` - Delete expense entry

### Summary Endpoint
- `GET /api/summary` - Get financial summary (totals, balance, category breakdown)

## Data Model

### Income Table
```
id (INTEGER) - Primary key
source (TEXT) - Income source
amount (REAL) - Income amount
date (TEXT) - Date of income
created_at (DATETIME) - Record creation timestamp
```

### Expenses Table
```
id (INTEGER) - Primary key
category (TEXT) - Expense category
description (TEXT) - Optional description
amount (REAL) - Expense amount
date (TEXT) - Date of expense
created_at (DATETIME) - Record creation timestamp
```

## Expense Categories

- Food & Groceries
- Transportation
- Utilities
- Entertainment
- Healthcare
- Shopping
- Education
- Other

## Technologies Used

- **Backend**: Node.js, Express.js
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charts**: Chart.js
- **Styling**: Custom CSS with gradients and animations

## Features Coming Soon

- 📈 Monthly/yearly trends
- 📱 Mobile app version
- 🔐 User authentication
- 📤 Export reports (PDF/CSV)
- 💳 Multi-currency support
- 🎯 Budget goals and alerts
- 📊 Advanced analytics and insights

## Browser Compatibility

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

If you encounter any issues or have suggestions, please create an issue on GitHub.

---

**Happy budgeting! 💰**
