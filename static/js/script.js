// Configuração do gráfico chart
// Seleciona o elemento do gráfico com o id 'expenseRevenueChart'
const chartElement = document.getElementById('expenseRevenueChart');

// Verifica se o elemento do gráfico está presente na página
if (chartElement) {
    // Obtém o 2D do elemento do gráfico
    const ctx = chartElement.getContext('2d');

    // Cria um novo gráfico do tipo barra com os dados
    const expenseRevenueChart = new Chart(ctx, {
        // Tipo de gráfico: barra
        type: 'bar',
        data: {
            // Rótulos para os eixos x
            labels: labels,
            // Conjunto de dados para o gráfico
            datasets: [{
                // Legenda para o conjunto de dados
                label: 'Despesas e Receitas',
                // Dados para o gráfico
                data: data,
                // Cores de fundo para as barras
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                // Cores de borda para as barras
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                // Largura da borda das barras
                borderWidth: 1
            }]
        },
        // Opções de configuração do gráfico
        options: {
            // Responsividade do gráfico, plugins, legendas
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                // Configuração do título
                title: {
                    display: true,
                    text: 'Tipos de Despesas e Receitas'
                }
            }
        },
    });
}


// Configuração modo escuro
// Evento de carregamento de página para configurar o modo escuro
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona os elementos necessários para o modo escuro
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
        // Alterna a classe 'dark-mode' nos elementos selecionados
        body.classList.toggle('dark-mode');
        container.classList.toggle('dark-mode');
        header.classList.toggle('dark-mode');
        footer.classList.toggle('dark-mode');
        
        // Alterna a classe 'dark-mode' nos links de navegação
        navLinks.forEach(link => link.classList.toggle('dark-mode'));
        // Alterna a classe 'dark-mode' nos botões
        buttons.forEach(button => button.classList.toggle('dark-mode'));
        // Alterna a classe 'dark-mode' nos inputs
        inputs.forEach(input => input.classList.toggle('dark-mode'));
        // Alterna a classe 'dark-mode' nas tabelas
        tables.forEach(table => table.classList.toggle('dark-mode'));

        // Salva a preferência no localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            localStorage.removeItem('dark-mode');
        }
    }

    // Verifica se a preferência do modo escuro está salva no localStorage
    if (localStorage.getItem('dark-mode') === 'enabled') {
        // Alterna o modo escuro se a preferência estiver salva
        toggleDarkMode();
    }

    // Adiciona o evento de clique ao botão de alternância do modo escuro
    toggleaddEventListener('click', toggleDarkMode);
});
