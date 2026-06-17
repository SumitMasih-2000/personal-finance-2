// API Base URL
const API_URL = 'http://localhost:5000/api';

// Chart instances
let incomeExpenseChart = null;
let categoryChart = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  loadIncomeData();
  loadExpenseData();
  updateSummary();
  setupFormListeners();
  
  // Refresh data every 5 seconds
  setInterval(updateSummary, 5000);
});

// Setup form event listeners
function setupFormListeners() {
  document.getElementById('incomeForm').addEventListener('submit', addIncome);
  document.getElementById('expenseForm').addEventListener('submit', addExpense);
}

// Set default dates to today
function setDefaultDate() {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('incomeDate').value = today;
  document.getElementById('expenseDate').value = today;
}

document.addEventListener('DOMContentLoaded', setDefaultDate);

// ============ INCOME FUNCTIONS ============

async function loadIncomeData() {
  try {
    const response = await fetch(`${API_URL}/income`);
    const incomeList = await response.json();
    displayIncomeList(incomeList);
  } catch (error) {
    console.error('Error loading income:', error);
  }
}

function displayIncomeList(incomeList) {
  const tbody = document.getElementById('incomeList');
  
  if (incomeList.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" class="empty-state">No income entries yet</td></tr>';
    return;
  }

  tbody.innerHTML = incomeList.map(income => `
    <tr>
      <td>${income.source}</td>
      <td>$${income.amount.toFixed(2)}</td>
      <td>${new Date(income.date).toLocaleDateString()}</td>
      <td>
        <button class="btn btn-danger" onclick="deleteIncome(${income.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

async function addIncome(e) {
  e.preventDefault();

  const source = document.getElementById('incomeSource').value;
  const amount = parseFloat(document.getElementById('incomeAmount').value);
  const date = document.getElementById('incomeDate').value;

  if (!source || !amount || !date) {
    alert('Please fill in all fields');
    return;
  }

  try {
    const response = await fetch(`${API_URL}/income`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source, amount, date })
    });

    if (response.ok) {
      document.getElementById('incomeForm').reset();
      setDefaultDate();
      loadIncomeData();
      updateSummary();
    }
  } catch (error) {
    console.error('Error adding income:', error);
    alert('Error adding income');
  }
}

async function deleteIncome(id) {
  if (confirm('Are you sure you want to delete this income entry?')) {
    try {
      await fetch(`${API_URL}/income/${id}`, { method: 'DELETE' });
      loadIncomeData();
      updateSummary();
    } catch (error) {
      console.error('Error deleting income:', error);
      alert('Error deleting income');
    }
  }
}

// ============ EXPENSE FUNCTIONS ============

async function loadExpenseData() {
  try {
    const response = await fetch(`${API_URL}/expenses`);
    const expenseList = await response.json();
    displayExpenseList(expenseList);
  } catch (error) {
    console.error('Error loading expenses:', error);
  }
}

function displayExpenseList(expenseList) {
  const tbody = document.getElementById('expenseList');
  
  if (expenseList.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No expense entries yet</td></tr>';
    return;
  }

  tbody.innerHTML = expenseList.map(expense => `
    <tr>
      <td><span class="category-badge">${expense.category}</span></td>
      <td>${expense.description || '-'}</td>
      <td>$${expense.amount.toFixed(2)}</td>
      <td>${new Date(expense.date).toLocaleDateString()}</td>
      <td>
        <button class="btn btn-danger" onclick="deleteExpense(${expense.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

async function addExpense(e) {
  e.preventDefault();

  const category = document.getElementById('expenseCategory').value;
  const description = document.getElementById('expenseDescription').value;
  const amount = parseFloat(document.getElementById('expenseAmount').value);
  const date = document.getElementById('expenseDate').value;

  if (!category || !amount || !date) {
    alert('Please fill in all required fields');
    return;
  }

  try {
    const response = await fetch(`${API_URL}/expenses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, description, amount, date })
    });

    if (response.ok) {
      document.getElementById('expenseForm').reset();
      setDefaultDate();
      loadExpenseData();
      updateSummary();
    }
  } catch (error) {
    console.error('Error adding expense:', error);
    alert('Error adding expense');
  }
}

async function deleteExpense(id) {
  if (confirm('Are you sure you want to delete this expense entry?')) {
    try {
      await fetch(`${API_URL}/expenses/${id}`, { method: 'DELETE' });
      loadExpenseData();
      updateSummary();
    } catch (error) {
      console.error('Error deleting expense:', error);
      alert('Error deleting expense');
    }
  }
}

// ============ SUMMARY & CHARTS ============

async function updateSummary() {
  try {
    const response = await fetch(`${API_URL}/summary`);
    const summary = await response.json();

    // Update summary cards
    document.getElementById('totalIncome').textContent = `$${summary.totalIncome.toFixed(2)}`;
    document.getElementById('totalExpenses').textContent = `$${summary.totalExpenses.toFixed(2)}`;
    document.getElementById('balance').textContent = `$${summary.balance.toFixed(2)}`;

    // Update balance card color
    const balanceCard = document.getElementById('balanceCard');
    if (summary.balance < 0) {
      balanceCard.classList.add('negative');
    } else {
      balanceCard.classList.remove('negative');
    }

    // Update charts
    updateCharts(summary);
  } catch (error) {
    console.error('Error updating summary:', error);
  }
}

async function updateCharts(summary) {
  // Get all data for detailed charts
  const incomeResponse = await fetch(`${API_URL}/income`);
  const incomeData = await incomeResponse.json();
  
  const expenseResponse = await fetch(`${API_URL}/expenses`);
  const expenseData = await expenseResponse.json();

  // Calculate totals for income/expense comparison
  const totalIncome = incomeData.reduce((sum, item) => sum + item.amount, 0);
  const totalExpenses = expenseData.reduce((sum, item) => sum + item.amount, 0);

  // Update Income vs Expenses Chart
  updateIncomeExpenseChart(totalIncome, totalExpenses);

  // Update Category Chart
  updateCategoryChart(summary.expensesByCategory);
}

function updateIncomeExpenseChart(income, expenses) {
  const ctx = document.getElementById('incomeExpenseChart').getContext('2d');
  
  if (incomeExpenseChart) {
    incomeExpenseChart.data.datasets[0].data = [income, expenses];
    incomeExpenseChart.update();
  } else {
    incomeExpenseChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Income', 'Expenses'],
        datasets: [{
          label: 'Amount ($)',
          data: [income, expenses],
          backgroundColor: [
            '#27ae60',
            '#e74c3c'
          ],
          borderColor: [
            '#229954',
            '#c0392b'
          ],
          borderWidth: 2,
          borderRadius: 5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + value.toFixed(2);
              }
            }
          }
        }
      }
    });
  }
}

function updateCategoryChart(expensesByCategory) {
  const ctx = document.getElementById('categoryChart').getContext('2d');
  
  const categories = Object.keys(expensesByCategory);
  const amounts = Object.values(expensesByCategory);
  
  const colors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
    '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
  ];

  if (categoryChart) {
    categoryChart.data.labels = categories;
    categoryChart.data.datasets[0].data = amounts;
    categoryChart.data.datasets[0].backgroundColor = colors.slice(0, categories.length);
    categoryChart.update();
  } else {
    categoryChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categories.length > 0 ? categories : ['No expenses'],
        datasets: [{
          data: amounts.length > 0 ? amounts : [1],
          backgroundColor: colors.slice(0, Math.max(categories.length, 1)),
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return '$' + context.parsed.toFixed(2);
              }
            }
          }
        }
      }
    });
  }
}
