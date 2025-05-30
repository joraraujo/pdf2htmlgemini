
# Conversor de PDF para HTML

Aplicação web em Streamlit que converte arquivos PDF em páginas HTML acessíveis, utilizando a API Google GenAI.

---

## Funcionalidades

- Upload de arquivos PDF
- Conversão do PDF para HTML semântico e acessível (WCAG 2.1 AA)
- Download do HTML gerado
- Uso da variável de ambiente para configurar a chave da API (`GOOGLE_API_KEY`)

---

## Tecnologias

- Python 3.x
- Streamlit
- Google GenAI SDK
- python-dotenv para variáveis de ambiente

---

## Como usar

### Pré-requisitos

- Python 3.7 ou superior
- Conta Google com acesso à API GenAI
- Chave da API Google GenAI

### Passos para rodar localmente

1. Clone o repositório:

```bash
git clone https://seu-repositorio.git
cd seu-projeto
```

2. Crie e ative seu ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

- Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

- Edite o arquivo `.env` e adicione sua chave de API:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

5. Execute o app Streamlit:

```bash
streamlit run app.py
```

### Uso

- Faça upload de um arquivo PDF
- Aguarde a conversão para HTML
- Baixe o arquivo HTML gerado

---

## Arquivo `.env.example`

```env
# Chave da API Google GenAI
GOOGLE_API_KEY=your_google_api_key_here
```

---

## Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

---

## Licença

Coloque aqui a licença do projeto (ex: MIT, GPL, etc.)
