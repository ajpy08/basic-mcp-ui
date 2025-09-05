class MCPCalculator {
    constructor() {
        this.history = [];
        this.config = null;
        this.initializeElements();
        this.loadConfig().then(() => {
            this.bindEvents();
        });
    }

    async loadConfig() {
        try {
            const response = await fetch('/config');
            this.config = await response.json();
            this.updateFooter();
        } catch (error) {
            console.error('Error loading config:', error);
            // Fallback to default values
            this.config = {
                mcp_host: '127.0.0.1',
                mcp_port: 8000,
                ui_host: '127.0.0.1',
                ui_port: 8001
            };
            this.updateFooter();
        }
    }

    updateFooter() {
        const mcpUrl = document.getElementById('mcp-url');
        const uiUrl = document.getElementById('ui-url');
        
        if (mcpUrl) {
            mcpUrl.textContent = `http://${this.config.mcp_host}:${this.config.mcp_port}`;
        }
        if (uiUrl) {
            uiUrl.textContent = `http://${this.config.ui_host}:${this.config.ui_port}`;
        }
    }

    initializeElements() {
        this.num1Input = document.getElementById('num1');
        this.num2Input = document.getElementById('num2');
        this.resultDisplay = document.getElementById('result');
        this.historyList = document.getElementById('history');
        this.clearHistoryBtn = document.getElementById('clearHistory');
        this.operationBtns = document.querySelectorAll('.operation-btn');
    }

    bindEvents() {
        this.operationBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const operation = e.target.dataset.operation;
                this.performOperation(operation);
            });
        });

        this.clearHistoryBtn.addEventListener('click', () => {
            this.clearHistory();
        });

        // Enter key support
        [this.num1Input, this.num2Input].forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performOperation('add'); // Default to add on Enter
                }
            });
        });
    }

    async performOperation(operation) {
        const num1 = parseFloat(this.num1Input.value);
        const num2 = parseFloat(this.num2Input.value);

        if (isNaN(num1) || isNaN(num2)) {
            this.showError('Por favor, ingresa números válidos');
            return;
        }

        this.setLoading(true);

        try {
            const result = await this.callMCPTool(operation, num1, num2);
            this.displayResult(result);
            this.addToHistory(operation, num1, num2, result);
        } catch (error) {
            this.showError(`Error: ${error.message}`);
            this.addToHistory(operation, num1, num2, null, error.message);
        } finally {
            this.setLoading(false);
        }
    }

    async callMCPTool(operation, x, y) {
        const url = `http://${this.config.ui_host}:${this.config.ui_port}/call_tool`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: operation,
                arguments: { x, y }
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en la operación');
        }

        const data = await response.json();
        return data.content[0].text;
    }

    displayResult(result) {
        this.resultDisplay.textContent = result;
        this.resultDisplay.style.color = '#667eea';
    }

    showError(message) {
        this.resultDisplay.textContent = message;
        this.resultDisplay.style.color = '#dc3545';
    }

    addToHistory(operation, num1, num2, result, error = null) {
        const timestamp = new Date().toLocaleTimeString();
        const operationSymbols = {
            add: '+',
            subtract: '-',
            multiply: '×',
            divide: '÷'
        };

        const historyItem = {
            operation,
            num1,
            num2,
            result,
            error,
            timestamp
        };

        this.history.unshift(historyItem);
        this.renderHistory();

        // Keep only last 10 items
        if (this.history.length > 10) {
            this.history = this.history.slice(0, 10);
        }
    }

    renderHistory() {
        this.historyList.innerHTML = '';

        if (this.history.length === 0) {
            this.historyList.innerHTML = '<div class="history-item">No hay operaciones realizadas</div>';
            return;
        }

        this.history.forEach(item => {
            const historyElement = document.createElement('div');
            historyElement.className = `history-item ${item.error ? 'error' : ''}`;
            
            if (item.error) {
                historyElement.innerHTML = `
                    <strong>${item.timestamp}</strong><br>
                    ${item.num1} ${this.getOperationSymbol(item.operation)} ${item.num2} = <span style="color: #dc3545;">Error</span><br>
                    <small>${item.error}</small>
                `;
            } else {
                historyElement.innerHTML = `
                    <strong>${item.timestamp}</strong><br>
                    ${item.num1} ${this.getOperationSymbol(item.operation)} ${item.num2} = <strong>${item.result}</strong>
                `;
            }

            this.historyList.appendChild(historyElement);
        });
    }

    getOperationSymbol(operation) {
        const symbols = {
            add: '+',
            subtract: '-',
            multiply: '×',
            divide: '÷'
        };
        return symbols[operation] || operation;
    }

    clearHistory() {
        this.history = [];
        this.renderHistory();
    }

    setLoading(loading) {
        const container = document.querySelector('.calculator-section');
        
        if (loading) {
            container.classList.add('loading');
            this.operationBtns.forEach(btn => btn.disabled = true);
        } else {
            container.classList.remove('loading');
            this.operationBtns.forEach(btn => btn.disabled = false);
        }
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MCPCalculator();
});
