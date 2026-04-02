// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add date validation
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            if (selectedDate > today) {
                alert('Please select a date that is not in the future');
                this.value = '';
            }
        });
    });

    // Add number input validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (parseFloat(this.value) <= 0) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Format currency inputs
    const amountInputs = document.querySelectorAll('input[name="amount"]');
    amountInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });
});

// Utility function to format currency
function formatCurrency(amount) {
    return '₹' + amount.toFixed(2);
}

// Utility function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Function to get summary statistics
function getSummaryStats() {
    return fetch('/api/get-data')
        .then(response => response.json())
        .then(data => {
            return {
                totalExpenses: data.expenses.reduce((sum, e) => sum + parseFloat(e[0]), 0),
                totalInvestments: data.investments.reduce((sum, i) => sum + parseFloat(i[1]), 0),
                totalSavings: data.savings.reduce((sum, s) => sum + parseFloat(s[0]), 0),
                expenseCount: data.expenses.length,
                investmentCount: data.investments.length,
                savingsCount: data.savings.length
            };
        });
}

// Function to refresh all data
function refreshAllData() {
    console.log('Refreshing all data...');
    fetch('/api/get-data')
        .then(response => response.json())
        .then(data => {
            console.log('Data refreshed:', data);
            // Dispatch custom event that other parts of the app can listen to
            window.dispatchEvent(new CustomEvent('dataRefreshed', { detail: data }));
        })
        .catch(error => console.error('Error refreshing data:', error));
}

// Function to show toast notifications
function showToast(message, type = 'info', duration = 3000) {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const container = document.getElementById('toastContainer') || createToastContainer();
    const toastElement = new DOMParser().parseFromString(toastHTML, 'text/html').body.firstChild;
    container.appendChild(toastElement);
    
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    setTimeout(() => toastElement.remove(), duration);
}

// Helper function to create toast container
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// Export functions for use in templates
window.financeApp = {
    formatCurrency,
    formatDate,
    getSummaryStats,
    refreshAllData,
    showToast
};
