# Aplicação de Consulta CEIS

Esta aplicação permite realizar consultas ao Cadastro de Empresas Inidôneas e Suspensas (CEIS) do Portal da Transparência utilizando a API da Infosimples.

## Sobre o CEIS

O Cadastro Nacional de Empresas Inidôneas e Suspensas (CEIS) apresenta a relação de empresas e pessoas físicas que sofreram sanções que implicaram a restrição de participar de licitações ou de celebrar contratos com a Administração Pública.

## Estrutura do Projeto

- `app.py`: Backend em Flask para processar as requisições à API do CEIS
- `static/index.html`: Interface de usuário para realizar as consultas (gerado automaticamente)
- `requirements.txt`: Dependências Python necessárias
- `.gitignore`: Configurações para ignorar arquivos e diretórios no Git
- `LICENSE`: Licença MIT para o projeto
- `Procfile`: Configuração para deploy no Heroku

## Requisitos

- Python 3.7 ou superior
- Token de acesso à API da Infosimples
- CNPJ ou CPF para consulta

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/consulta-ceis.git
   cd consulta-ceis
   ```

2. Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Crie uma pasta `static` e coloque o arquivo `index.html` dentro dela:
   ```
   mkdir -p static
   ```
   (Copie o conteúdo do arquivo HTML fornecido no repositório para o arquivo `static/index.html`)

## Executando a Aplicação

1. Inicie o servidor Flask:
   ```
   python app.py
   ```

2. Acesse a aplicação no navegador:
   ```
   http://localhost:5000
   ```

3. Na interface, insira:
   - Token de acesso à API da Infosimples
   - CNPJ ou CPF para consulta
   - Clique em "Consultar"

## Testando a aplicação

Para fins de teste, você pode usar:
- CNPJ: 11.111.111/1111-11
- CPF: 111.111.111-11

## Implantação

Para implantar em um servidor de produção, recomenda-se:

1. Usar Gunicorn como servidor WSGI:
   ```
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

2. Configurar um servidor proxy reverso (Nginx ou Apache) na frente do Gunicorn

3. Configurar variáveis de ambiente para informações sensíveis (como tokens)

## Observações de Segurança

- Esta aplicação não armazena nenhum dado de consulta
- O token da API é enviado diretamente do frontend para o backend
- Em ambiente de produção, considere implementar autenticação e autorização
- Armazene tokens e chaves de API em variáveis de ambiente ou arquivos de configuração seguros

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
