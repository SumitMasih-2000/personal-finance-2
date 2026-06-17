const express = require('express');
const cors = require('cors');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Initialize SQLite database
const db = new sqlite3.Database('./finance.db', (err) => {
  if (err) console.error('Database connection error:', err);
  else console.log('Connected to SQLite database');
});

// Create tables if they don't exist
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS income (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source TEXT NOT NULL,
      amount REAL NOT NULL,
      date TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      category TEXT NOT NULL,
      description TEXT,
      amount REAL NOT NULL,
      date TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
});

// API Routes

// Get all income entries
app.get('/api/income', (req, res) => {
  db.all('SELECT * FROM income ORDER BY date DESC', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(rows || []);
    }
  });
});

// Add new income
app.post('/api/income', (req, res) => {
  const { source, amount, date } = req.body;
  if (!source || !amount || !date) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  db.run(
    'INSERT INTO income (source, amount, date) VALUES (?, ?, ?)',
    [source, amount, date],
    function(err) {
      if (err) {
        res.status(500).json({ error: err.message });
      } else {
        res.json({ id: this.lastID, source, amount, date });
      }
    }
  );
});

// Delete income entry
app.delete('/api/income/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM income WHERE id = ?', [id], (err) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json({ message: 'Income deleted' });
    }
  });
});

// Get all expenses
app.get('/api/expenses', (req, res) => {
  db.all('SELECT * FROM expenses ORDER BY date DESC', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json(rows || []);
    }
  });
});

// Add new expense
app.post('/api/expenses', (req, res) => {
  const { category, description, amount, date } = req.body;
  if (!category || !amount || !date) {
    return res.status(400).json({ error: 'Missing required fields' });
  }
  db.run(
    'INSERT INTO expenses (category, description, amount, date) VALUES (?, ?, ?, ?)',
    [category, description || '', amount, date],
    function(err) {
      if (err) {
        res.status(500).json({ error: err.message });
      } else {
        res.json({ id: this.lastID, category, description, amount, date });
      }
    }
  );
});

// Delete expense entry
app.delete('/api/expenses/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM expenses WHERE id = ?', [id], (err) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.json({ message: 'Expense deleted' });
    }
  });
});

// Get dashboard summary
app.get('/api/summary', (req, res) => {
  let totalIncome = 0;
  let totalExpenses = 0;
  let expensesByCategory = {};

  db.all('SELECT SUM(amount) as total FROM income', (err, rows) => {
    if (!err && rows[0].total) totalIncome = rows[0].total;

    db.all('SELECT SUM(amount) as total FROM expenses', (err, rows) => {
      if (!err && rows[0].total) totalExpenses = rows[0].total;

      db.all(
        'SELECT category, SUM(amount) as amount FROM expenses GROUP BY category',
        (err, rows) => {
          if (!err) {
            rows.forEach(row => {
              expensesByCategory[row.category] = row.amount;
            });
          }

          res.json({
            totalIncome,
            totalExpenses,
            balance: totalIncome - totalExpenses,
            expensesByCategory
          });
        }
      );
    });
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

// Close database connection on process exit
process.on('SIGINT', () => {
  db.close((err) => {
    if (err) console.error('Error closing database:', err);
    else console.log('Database connection closed');
    process.exit(0);
  });
});
