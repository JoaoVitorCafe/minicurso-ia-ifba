# Repositório com alguns exemplos do curso de IA - 22/11

Scripts construídos para o minicurso de IA utilizando LangChain, demonstrando conceitos como RAG, indexação vetorial, middlewares, tool calling e gerenciamento de memória.

## Configuração do Ambiente

### Instalação do Python 3.13

Baixe e instale o Python 3.13 em: https://www.python.org/downloads/release/python-3130/

### Instalação do Docker

Baixe e instale o Docker Desktop em: https://www.docker.com/products/docker-desktop/

### Comandos Docker

**Build da imagem:**

```bash
docker build -t pgvector-ifba .
```

**Executar o container:**

```bash
docker run -d --name pgvector-ifba -e POSTGRES_PASSWORD=postgres -p 5433:5432 pgvector-ifba
```

### Instalação do Pipenv

**Importante:** É necessário ter privilégios de administrador. Abra o CMD ou PowerShell como Administrador e execute:

```bash
pip install pipenv
```

Após a instalação, crie e ative o ambiente virtual:

```bash
pipenv shell
```

Em seguida, instale as dependências do projeto:

```bash
pipenv install
```

### Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

**Obrigatórias:**

```
GOOGLE_API_KEY=
OPENAI_API_KEY=
```

**Opcionais:**

```
LANGSMITH_TRACING=
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
```

## Executando os Scripts

```bash
python 4_index_chroma.py
python 5_agent_rag.py
python 6_agent_dynamic_prompt.py
python 7_index_api.py
python 8_index_pgvector.py
python 9_memory.py
python 10_agent.py
python 11_tool_calling_agent.py
python 12_model_routing.py
python 13_middlewares.py
python 14_custom_middlewares.py
```
