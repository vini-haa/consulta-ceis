from flask import Flask, request, jsonify
import requests
import os
import shutil
from flask_cors import CORS

# Cria a pasta static se não existir
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

app = Flask(__name__, static_folder=static_folder)
CORS(app)  # Habilita CORS para permitir requisições do frontend

# URL da API do Portal da Transparência CEIS
API_URL = "https://api.infosimples.com/api/v2/consultas/portal-transparencia/ceis"

@app.route('/api/consulta-ceis', methods=['POST'])
def consulta_ceis():
    """
    Endpoint para consultar CEIS na API da Infosimples
    
    Parâmetros esperados:
    - token: Token de acesso à API
    - cnpj: CNPJ da empresa (opcional)
    - cpf: CPF do indivíduo (opcional)
    """
    # Recupera os dados do formulário
    token = request.form.get('token')
    cnpj = request.form.get('cnpj')
    cpf = request.form.get('cpf')
    
    # Valida parâmetros obrigatórios
    if not token:
        return jsonify({
            "code": 400,
            "code_message": "Parâmetro obrigatório não informado",
            "errors": ["O token de acesso é obrigatório"]
        }), 400
    
    # Verifica se pelo menos um parâmetro de consulta foi informado
    if not cnpj and not cpf:
        return jsonify({
            "code": 400,
            "code_message": "Parâmetro obrigatório não informado",
            "errors": ["Informe um CNPJ ou CPF para realizar a consulta"]
        }), 400
    
    # Prepara os parâmetros para enviar à API
    params = {
        "token": token,
        "timeout": 300  # Timeout de 5 minutos
    }
    
    # Adiciona CNPJ ou CPF aos parâmetros, se informados
    if cnpj:
        params["cnpj"] = cnpj
    if cpf:
        params["cpf"] = cpf
    
    try:
        # Realiza a requisição para a API do CEIS
        response = requests.post(API_URL, data=params)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Retorna os dados recebidos da API
            return jsonify(response.json())
        else:
            # Trata erros de comunicação com a API
            return jsonify({
                "code": response.status_code,
                "code_message": "Erro ao comunicar com a API externa",
                "errors": [f"A API retornou o código {response.status_code}"]
            }), 500
            
    except requests.exceptions.RequestException as e:
        # Trata exceções na requisição
        return jsonify({
            "code": 500,
            "code_message": "Erro ao processar a requisição",
            "errors": [str(e)]
        }), 500
    except Exception as e:
        # Trata outras exceções não previstas
        return jsonify({
            "code": 500,
            "code_message": "Erro interno do servidor",
            "errors": [str(e)]
        }), 500

# Rota para servir a página principal
@app.route('/')
def index():
    return app.send_static_file('index.html')

def create_html_file():
    """
    Cria o arquivo HTML no diretório static
    """
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta CEIS - Portal da Transparência</title>
    <style>
        :root {
            --primary-color: #1a73e8;
            --secondary-color: #f1f3f4;
            --error-color: #d93025;
            --success-color: #0f9d58;
            --text-color: #202124;
            --light-text: #5f6368;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #f8f9fa;
            color: var(--text-color);
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        h1 {
            color: var(--primary-color);
            margin-bottom: 10px;
        }
        
        .description {
            color: var(--light-text);
            margin-bottom: 15px;
        }
        
        .search-form {
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 16px;
            transition: border 0.3s;
        }
        
        input[type="text"]:focus {
            border-color: var(--primary-color);
            outline: none;
        }
        
        .input-group {
            display: flex;
            gap: 15px;
        }
        
        .input-group .form-group {
            flex: 1;
        }
        
        .submit-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.3s;
            width: 100%;
        }
        
        .submit-btn:hover {
            background-color: #0d62d0;
        }
        
        .submit-btn:disabled {
            background-color: #a9c7f5;
            cursor: not-allowed;
        }
        
        .result-container {
            background-color: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
            display: none;
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .result-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        .result-status {
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .status-positive {
            background-color: #e6f4ea;
            color: var(--success-color);
        }
        
        .status-negative {
            background-color: #fce8e6;
            color: var(--error-color);
        }
        
        .result-info {
            margin-bottom: 25px;
        }
        
        .info-item {
            margin-bottom: 15px;
        }
        
        .info-label {
            font-weight: 500;
            margin-bottom: 5px;
            color: var(--light-text);
        }
        
        .info-value {
            font-size: 16px;
        }
        
        .sanction-details {
            background-color: var(--secondary-color);
            padding: 20px;
            border-radius: 6px;
            margin-top: 20px;
        }
        
        .sanction-title {
            font-weight: 600;
            margin-bottom: 15px;
            font-size: 17px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid var(--primary-color);
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error-message {
            color: var(--error-color);
            background-color: #fce8e6;
            padding: 12px 15px;
            border-radius: 4px;
            margin-top: 15px;
            display: none;
        }
        
        .no-results {
            text-align: center;
            padding: 30px 0;
            color: var(--light-text);
            display: none;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: var(--light-text);
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .input-group {
                flex-direction: column;
                gap: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Consulta CEIS</h1>
            <p class="description">Cadastro de Empresas Inidôneas e Suspensas - Portal da Transparência</p>
        </header>
        
        <div class="search-form">
            <div class="input-group">
                <div class="form-group">
                    <label for="cnpj">CNPJ</label>
                    <input type="text" id="cnpj" name="cnpj" placeholder="Ex: 00.000.000/0000-00">
                </div>
                
                <div class="form-group">
                    <label for="cpf">CPF</label>
                    <input type="text" id="cpf" name="cpf" placeholder="Ex: 000.000.000-00">
                </div>
            </div>
            
            <div class="form-group">
                <label for="token">Token de Acesso</label>
                <input type="text" id="token" name="token" placeholder="Insira seu token de acesso à API">
            </div>
            
            <button type="button" id="search-btn" class="submit-btn">Consultar</button>
            
            <div class="error-message" id="error-message"></div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Consultando dados, por favor aguarde...</p>
        </div>
        
        <div class="no-results" id="no-results">
            <p>Nenhum registro encontrado para os dados informados.</p>
        </div>
        
        <div class="result-container" id="result-container">
            <div class="result-header">
                <div class="result-title" id="result-entity-name"></div>
                <div class="result-status" id="result-status"></div>
            </div>
            
            <div class="result-info">
                <div class="info-item">
                    <div class="info-label">Nome/Razão Social:</div>
                    <div class="info-value" id="result-nome"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Nome Fantasia:</div>
                    <div class="info-value" id="result-nome-fantasia"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Órgão Sancionador:</div>
                    <div class="info-value" id="result-orgao"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">UF:</div>
                    <div class="info-value" id="result-uf"></div>
                </div>
            </div>
            
            <div class="sanction-details">
                <div class="sanction-title">Detalhes da Sanção</div>
                
                <div class="info-item">
                    <div class="info-label">Tipo de Sanção:</div>
                    <div class="info-value" id="result-tipo-sancao"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Fundamentação Legal:</div>
                    <div class="info-value" id="result-fundamento"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Data de Início:</div>
                    <div class="info-value" id="result-data-inicio"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Data de Fim:</div>
                    <div class="info-value" id="result-data-fim"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Data de Publicação:</div>
                    <div class="info-value" id="result-data-publicacao"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Processo:</div>
                    <div class="info-value" id="result-processo"></div>
                </div>
                
                <div class="info-item">
                    <div class="info-label">Observações:</div>
                    <div class="info-value" id="result-observacoes"></div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>Consulta CEIS - Cadastro de Empresas Inidôneas e Suspensas © 2025</p>
            <p>Dados fornecidos pelo Portal da Transparência</p>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const cnpjInput = document.getElementById('cnpj');
            const cpfInput = document.getElementById('cpf');
            const tokenInput = document.getElementById('token');
            const searchBtn = document.getElementById('search-btn');
            const errorMessage = document.getElementById('error-message');
            const loading = document.getElementById('loading');
            const resultContainer = document.getElementById('result-container');
            const noResults = document.getElementById('no-results');
            
            // Mascaras para CNPJ e CPF
            cnpjInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\\D/g, '');
                if (value.length > 14) value = value.slice(0, 14);
                
                if (value.length > 12) {
                    value = value.replace(/^(\\d{2})(\\d{3})(\\d{3})(\\d{4})(\\d{2}).*/, '$1.$2.$3/$4-$5');
                } else if (value.length > 8) {
                    value = value.replace(/^(\\d{2})(\\d{3})(\\d{3})(\\d*)/, '$1.$2.$3/$4');
                } else if (value.length > 5) {
                    value = value.replace(/^(\\d{2})(\\d{3})(\\d*)/, '$1.$2.$3');
                } else if (value.length > 2) {
                    value = value.replace(/^(\\d{2})(\\d*)/, '$1.$2');
                }
                
                e.target.value = value;
                
                // Limpar CPF se CNPJ estiver sendo preenchido
                if (value.length > 0) {
                    cpfInput.value = '';
                }
            });
            
            cpfInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\\D/g, '');
                if (value.length > 11) value = value.slice(0, 11);
                
                if (value.length > 9) {
                    value = value.replace(/^(\\d{3})(\\d{3})(\\d{3})(\\d{2}).*/, '$1.$2.$3-$4');
                } else if (value.length > 6) {
                    value = value.replace(/^(\\d{3})(\\d{3})(\\d*)/, '$1.$2.$3');
                } else if (value.length > 3) {
                    value = value.replace(/^(\\d{3})(\\d*)/, '$1.$2');
                }
                
                e.target.value = value;
                
                // Limpar CNPJ se CPF estiver sendo preenchido
                if (value.length > 0) {
                    cnpjInput.value = '';
                }
            });
            
            // Função para validar os campos antes da consulta
            function validateFields() {
                errorMessage.style.display = 'none';
                errorMessage.textContent = '';
                
                if (!tokenInput.value.trim()) {
                    showError('O token de acesso é obrigatório.');
                    return false;
                }
                
                if (!cnpjInput.value.trim() && !cpfInput.value.trim()) {
                    showError('Informe um CNPJ ou CPF para realizar a consulta.');
                    return false;
                }
                
                return true;
            }
            
            // Função para mostrar mensagens de erro
            function showError(message) {
                errorMessage.textContent = message;
                errorMessage.style.display = 'block';
            }
            
            // Função para formatar a exibição dos dados
            function formatDisplayValue(value) {
                return value && value !== '**' ? value : 'Não informado';
            }
            
            // Função para realizar a consulta à API
            async function consultCEIS() {
                if (!validateFields()) return;
                
                // Preparando os dados da requisição
                const formData = new FormData();
                formData.append('token', tokenInput.value.trim());
                
                if (cnpjInput.value.trim()) {
                    formData.append('cnpj', cnpjInput.value.replace(/\\D/g, ''));
                }
                
                if (cpfInput.value.trim()) {
                    formData.append('cpf', cpfInput.value.replace(/\\D/g, ''));
                }
                
                // Configurando a exibição durante a consulta
                loading.style.display = 'block';
                resultContainer.style.display = 'none';
                noResults.style.display = 'none';
                errorMessage.style.display = 'none';
                
                try {
                    // Realizando a chamada à API
                    const response = await fetch('/api/consulta-ceis', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    // Processando a resposta
                    if (data.code === 200) {
                        if (data.data_count > 0) {
                            displayResults(data.data[0]);
                        } else {
                            noResults.style.display = 'block';
                        }
                    } else {
                        // Tratando erros retornados pela API
                        let errorMsg = `Erro ${data.code}: ${data.code_message}`;
                        if (data.errors && data.errors.length > 0) {
                            errorMsg += ` - ${data.errors.join('; ')}`;
                        }
                        showError(errorMsg);
                    }
                } catch (error) {
                    showError(`Erro ao realizar a consulta: ${error.message}`);
                } finally {
                    loading.style.display = 'none';
                }
            }
            
            // Função para exibir os resultados na interface
            function displayResults(data) {
                // Preenchendo os dados básicos
                document.getElementById('result-entity-name').textContent = data.cadastro_receita || 'Consulta CEIS';
                document.getElementById('result-status').textContent = 'Sancionado';
                document.getElementById('result-status').className = 'result-status status-negative';
                
                document.getElementById('result-nome').textContent = formatDisplayValue(data.cadastro_receita);
                document.getElementById('result-nome-fantasia').textContent = formatDisplayValue(data.nome_fantasia);
                
                // Preenchendo dados do órgão sancionador
                if (data.orgao_sancionador) {
                    document.getElementById('result-orgao').textContent = formatDisplayValue(data.orgao_sancionador.nome);
                    document.getElementById('result-uf').textContent = formatDisplayValue(data.orgao_sancionador.uf);
                }
                
                // Preenchendo dados da sanção
                if (data.sancao) {
                    document.getElementById('result-tipo-sancao').textContent = formatDisplayValue(data.sancao.tipo);
                    document.getElementById('result-fundamento').textContent = formatDisplayValue(data.sancao.fundamentacao_legal);
                    document.getElementById('result-data-inicio').textContent = formatDisplayValue(data.sancao.inicio_data);
                    document.getElementById('result-data-fim').textContent = formatDisplayValue(data.sancao.fim_data);
                    document.getElementById('result-data-publicacao').textContent = formatDisplayValue(data.sancao.publicacao_data);
                    document.getElementById('result-processo').textContent = formatDisplayValue(data.sancao.processo);
                    document.getElementById('result-observacoes').textContent = formatDisplayValue(data.sancao.observacoes);
                }
                
                // Exibindo o container de resultados
                resultContainer.style.display = 'block';
            }
            
            // Event listener para o botão de consulta
            searchBtn.addEventListener('click', consultCEIS);
            
            // Permitir usar Enter para submeter o formulário
            [cnpjInput, cpfInput, tokenInput].forEach(input => {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        consultCEIS();
                    }
                });
            });
        });
    </script>
</body>
</html>
"""
    
    # Cria o arquivo index.html no diretório static
    with open(os.path.join(static_folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

def run():
    """
    Função para iniciar a aplicação quando instalada como pacote
    """
    # Cria o arquivo HTML na pasta static
    create_html_file()
    
    # Configura a porta do servidor (padrão: 5000)
    port = int(os.environ.get('PORT', 5000))
    
    # Inicia o servidor
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run()
