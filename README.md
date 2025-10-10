# Books Scraper API

## Project Overview

Books Scraper API é uma aplicação desenvolvida com FastAPI que realiza o web scraping de livros do site [Books to Scrape](https://books.toscrape.com/), armazena os dados em um banco PostgreSQL (via Supabase) e expõe uma API REST completa para consulta, análise e integração com modelos de Machine Learning.

O projeto também inclui:
* Autenticação JWT
* SQLAlchemy ORM
* Registro estruturado de logs
* Dashboard interativo com Streamlit para visualização e análise de logs e estatísticas

Repositório no GitHub: [gustavo-leandro/MLEnginnering_techChallenge_1](https://github.com/gustavo-leandro/MLEnginnering_techChallenge_1.git)  
API em produção: [https://gleandro-book-api-996cbfb885c8.herokuapp.com/](https://gleandro-book-api-996cbfb885c8.herokuapp.com/)

## Architecture Overview

| Componente | Descrição |
|-------------|------------|
| FastAPI | Framework principal para criação dos endpoints da API |
| SQLAlchemy | ORM para definição de modelos e consultas |
| PostgreSQL (Supabase) | Banco de dados em nuvem para persistência dos dados |
| JWT Authentication | Controle de acesso seguro para rotas protegidas |
| Routers Modulares | Separação de responsabilidades entre os endpoints |
| Structured Logging | Registro de todas as requisições HTTP no banco |
| Streamlit | Dashboard para análise de logs e monitoramento da aplicação |

## Installation and Setup

### 1. Clonar o repositório

```bash
git clone https://github.com/gustavo-leandro/MLEnginnering_techChallenge_1.git
cd MLEnginnering_techChallenge_1
```

### 2. Instalar dependências (Python 3.12+)

```bash
poetry install
```

### 3. Configurar o banco de dados

1. Crie um projeto no Supabase e obtenha a connection string PostgreSQL.
2. No arquivo `app/database.py`, defina a URL:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://username:password@host:port/dbname"
   ```
3. Instale o driver do PostgreSQL:
   ```bash
   poetry add psycopg2-binary
   ```

### 4. Variáveis de ambiente (opcional)

Configure suas credenciais e segredos no arquivo `.env`.  

## API Routes Documentation

A API segue uma estrutura RESTful organizada em módulos.

### Authentication

| Método | Rota | Descrição |
|--------|------|------------|
| POST | `/api/v1/auth/login` | Autenticação via usuário e senha |
| POST | `/api/v1/auth/refresh` | Gera novo token JWT |

### Books

| Método | Rota | Descrição |
|--------|------|------------|
| GET | `/api/v1/books/` | Lista livros (paginação) |
| POST | `/api/v1/books/scraping/trigger` | Executa scraping e salva no banco |
| GET | `/api/v1/books/search` | Busca livros por título ou categoria |
| GET | `/api/v1/books/top-rated` | Lista livros com melhor avaliação |
| GET | `/api/v1/books/price-range` | Busca livros por faixa de preço |
| GET | `/api/v1/books/{id}` | Obtém livro por ID |

### Categories

| Método | Rota | Descrição |
|--------|------|------------|
| GET | `/api/v1/categories` | Lista todas as categorias |

### Health

| Método | Rota | Descrição |
|--------|------|------------|
| GET | `/api/v1/health` | Verifica status da API e do banco |

### Stats

| Método | Rota | Descrição |
|--------|------|------------|
| GET | `/api/v1/stats/overview` | Estatísticas gerais de livros |
| GET | `/api/v1/stats/categories` | Estatísticas por categoria |
| GET | `/api/v1/stats/top-rated` | Livros com maiores notas |
| GET | `/api/v1/stats/price-range` | Livros dentro de uma faixa de preço |

### Machine Learning

| Método | Rota | Descrição |
|--------|------|------------|
| GET | `/api/v1/ml/features` | Retorna features para uso em ML |
| GET | `/api/v1/ml/training-data` | Retorna amostra aleatória de 100 livros |
| POST | `/api/v1/ml/predictions` | Envia dados e retorna predições (autenticado) |

## Example Requests and Responses

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin"
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer"
}
```

## Running the Application

### Local

```bash
poetry run uvicorn app.main:app --reload
```

Acesse a API em:  
[http://localhost:8000](http://localhost:8000)

Documentação interativa:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Streamlit Dashboard

```bash
streamlit run dashboard.py
```

Disponível em:  
[http://localhost:8501](http://localhost:8501)

## Deployed Version

A versão de produção está disponível em:  
[https://gleandro-book-api-996cbfb885c8.herokuapp.com/](https://gleandro-book-api-996cbfb885c8.herokuapp.com/)

## Additional Notes

* Todas as requisições HTTP são registradas na tabela `request_logs`.
* Em produção, use variáveis de ambiente para segredos e conexões.
* A lógica de scraping é adaptada para books.toscrape.com e pode ser ajustada para outras fontes.
* Endpoints de ML estão prontos para integração com modelos personalizados.

## License

Este projeto é distribuído sob a Licença GNU General Public License v3.0 (GPL-3.0).
Você pode redistribuir e/ou modificar este software de acordo com os termos da GPL-3.0, conforme publicada pela Free Software Foundation.