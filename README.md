# Dashboard de Produção GDB
Este é um sistema simples desenvolvido em **Django** e **Python**, rodando em containers **Docker**, projetado para monitorar processos industriais em rede local.

### 2. Tecnologias Utilizadas

* **Backend:** Python 3.11 / Django
* **Banco de Dados:** PostgreSQL (Alpine)
* **Infraestrutura:** Docker & Docker Compose
* **Sistema Operacional de Destino:** Debian (Otimizado para hardware Core 2 Duo)
 
### 3. Pré-requisitos

* Docker
* Docker Compose

### 4. Quick Start
#### 1. Clone o repositório
  git clone https://github.com/mactromel/dashsys.git

#### 2. Entre na pasta
  cd dashsys

#### 3. Crie o arquivo .env (use o .env.example como base)
  cp .env_example .env

#### 4. Suba os containers
  docker compose up -d

#### 5. Execute as migrações do banco
  docker compose exec web python manage.py migrate

### 5. Notas sobre o Hardware
#### Otimização para Hardware Legado
Este projeto foi configurado para rodar em hardware com recursos limitados (Core 2 Duo, 4GB RAM):
* Uso de imagens **Python-Slim** e **Postgres-Alpine** para reduzir o footprint de memória.
* Limites de recursos definidos no `docker-compose.yml` para garantir estabilidade do SO host.
