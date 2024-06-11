// Configuração do gráfico chart
const chartElement = document.getElementById('expenseRevenueChart');

// Verifica se o elemento do gráfico está presente na página
if (chartElement) {
    const ctx = chartElement.getContext('2d');
    const expenseRevenueChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Despesas e Receitas',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Tipos de Despesas e Receitas'
                }
            }
        },
    });
}


// Configuração modo escuro
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const body = document.body;
    const container = document.querySelector('.container');
    const header = document.querySelector('.header');
    const navLinks = document.querySelectorAll('.nav-link');
    const buttons = document.querySelectorAll('button');
    const inputs = document.querySelectorAll('input, select');
    const tables = document.querySelectorAll('table, th, td');
    const footer = document.querySelector('footer');

    // Função para alternar o modo escuro
    function toggleDarkMode() {
        body.classList.toggle('dark-mode');
        container.classList.toggle('dark-mode');
        header.classList.toggle('dark-mode');
        footer.classList.toggle('dark-mode');
        
        navLinks.forEach(link => link.classList.toggle('dark-mode'));
        buttons.forEach(button => button.classList.toggle('dark-mode'));
        inputs.forEach(input => input.classList.toggle('dark-mode'));
        tables.forEach(table => table.classList.toggle('dark-mode'));

        // Salvar a preferência no localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.removeItem('dark-mode');
        }
    }

    // Verificar a preferência salva no localStorage
    if (localStorage.getItem('dark-mode') === 'enabled') {
        toggleDarkMode();
    }

    // Adicionar o evento de clique ao botão de alternância
    toggleButton.addEventListener('click', toggleDarkMode);
});

