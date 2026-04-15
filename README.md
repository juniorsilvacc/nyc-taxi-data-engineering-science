# 🗽 NYC Taxi Data Engineering Project: 46M+ Rows

Este projeto demonstra a construção de um pipeline de dados de ponta a ponta, processando mais de **46 milhões de registros** do dataset público de Taxi de Nova York (NYC Taxi). O objetivo principal é transformar dados brutos (Bronze) em uma camada analítica altamente otimizada (Gold) utilizando o padrão **Star Schema**.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python & SQL
* **Processamento de Dados:** PySpark (Dockerized)
* **Transformação & Modelagem:** dbt (data build tool)
* **Banco de Dados:** PostgreSQL (Docker)
* **Infraestrutura:** WSL2 (Ubuntu), Docker & Docker Compose
* **Documentação:** dbt Docs & Excalidraw

---

## 🏗️ Arquitetura do Projeto

<img width="1750" height="874" alt="Image" src="https://github.com/juniorsilvacc/nyc-taxi-data-engineering-science/blob/master/assets/arquitetura.png" />

---

## 🧱 Demonstração da Linhagem (Lineage Graph)

<img width="1750" height="874" alt="Image" src="https://github.com/juniorsilvacc/nyc-taxi-data-engineering-science/blob/master/assets/lineage-graph.png" />

---

## 🏛️ Medallion Architecture
O projeto segue a **Medallion Architecture**, garantindo qualidade e governança em cada etapa:

1.  **Bronze (Raw):** Dados brutos ingeridos de arquivos CSV/Parquet.
2.  **Silver (Cleaned):** Processamento com **PySpark** para limpeza, tipagem, filtragem de outliers (ex: `total_amount > 0`) e cálculos de duração (`trip_duration_minutes`).
3.  **Gold (Marts):** Modelagem dimensional no **dbt** transformando a camada Silver em um **Star Schema** otimizado para BI.

--- 

## 🌌 Modelagem Dimensional (Star Schema)

A camada Gold foi estruturada para máxima performance analítica, permitindo responder perguntas complexas de negócio com joins simples.

### Central: Tabela Fato
* **`fct_taxi_trips`**: Contém as métricas quantitativas (distância, valores, duração) e as chaves estrangeiras.

### Periferia: Tabelas Dimensão
* **`dim_date`**: Atributos temporais (ano, mês, dia da semana, flag de final de semana).
* **`dim_time`**: Divisão por turnos (Manhã, Tarde, Noite, Madrugada) e identificação de **Rush Hour**.
* **`dim_vendors`**: Nome legível dos fornecedores de tecnologia.
* **`dim_passengers`**: Categorização por capacidade (Single, Small Group, Large Group).
* **`dim_trip_type`**: Classificação por distância (Short, Medium, Long Trip).
* **`dim_payments`**: Descrição dos métodos de pagamento (Credit Card, Cash, etc).
* **`dim_rate_codes`**: Identificação do tipo de tarifa (Standard, Aeroportos, Negociada).

---

## 📂 Estrutura de Camadas (Medallion)
Para manter a Governança e organização dos modelos:

```text
dbt_dw/
├── models/
│   ├── staging/                         # Camada Silver (Tratamento Inicial)
│   │   ├── _stg_models.yml
│   │   └── stg_nyc_taxi.sql
│   │
│   ├── marts/                           # Camada Gold (Business & Analytics)
│   │   ├── _marts_models.yml
│   │   ├── dimensions/                  # Tabelas de suporte (Quem, Onde, Quando)
│   │   │   ├── dim_date.sql
│   │   │   ├── dim_payments.sql
│   │   │   ├── dim_rate_codes.sql
│   │   │   ├── dim_passengers.sql
│   │   │   └── dim_time.sql
│   │   │
│   │   └── facts/                       # Tabelas de eventos (O que aconteceu)
│   │       └── fct_taxi_trips.sql
└── 
```

---

# 📊 Visualização de Demanda (Heatmaps 3D)
Utilizamos o Streamlit e Pydeck para mapear a densidade de coletas em Manhattan. A visualização permite identificar zonas de alta demanda por turno, auxiliando na compreensão do comportamento urbano de Nova York.

## Densidade por Turno

Manhã
<img width="1750" height="874" alt="Image" src="https://github.com/juniorsilvacc/nyc-taxi-data-engineering-science/blob/master/assets/densidade-manha.png" />

Tarde
<img width="1750" height="874" alt="Image" src="https://github.com/juniorsilvacc/nyc-taxi-data-engineering-science/blob/master/assets/densidade-tarde.png" />

Noite
<img width="1750" height="874" alt="Image" src="https://github.com/juniorsilvacc/nyc-taxi-data-engineering-science/blob/master/assets/densidade-noite.png" />

Madrugada
<img width="1750" height="874" alt="Image" src="https://github.com/juniorsilvacc/nyc-taxi-data-engineering-science/blob/master/assets/densidade-madrugada.png" />

- Insight: As visualizações em 3D (Hexagon Layer) mostram claramente o deslocamento do tráfego financeiro durante o dia e a concentração em zonas de entretenimento durante a noite.

--- 

# 🤖 Modelagem Preditiva
Construímos um regressor utilizando Random Forest para prever o total_amount das corridas.

Especificações Técnicas:
- Algoritmo: Random Forest Regressor.
- Features: trip_distance, hour_of_day, day_of_week, is_weekend.
- Performance: MAE de ~$2.15, provando alta aderência para corridas urbanas comuns.
- Feature Importance: A distância da viagem e o horário (trânsito) foram os fatores determinantes para a precisão do modelo.

---

## 🚀 Como Executar

1.  **Levantar Ambiente:**
    ```bash
    docker-compose up -d
    ```
2.  **Processamento Spark (Silver):**
    Execute o job PySpark para limpar os 46M de linhas e carregar no Postgres.
3.  **Transformação dbt (Gold):**
    ```bash
    cd dbt_dw
    dbt deps
    dbt run
    dbt test
    ```

---

## 📊 Resultados e Performance

* **Volume Processado:** 46.942.600 de linhas.
* **Tempo de Processamento Gold:** ~50 segundos para consolidar a tabela fato no PostgreSQL.
* **Data Quality:** Implementação de testes de `not_null`, `accepted_values` e validações customizadas via `schema.yml`.

---

## 📈 Insights Possíveis
Com esta modelagem, é possível analisar:
* Correlação entre clima/feriados e o volume de gorjetas.
* Bairros (Pickup/Dropoff) com maior ticket médio durante a hora do rush.
* Preferência de método de pagamento baseada na distância da viagem.

---

### 👷 Autor
[Linkedin](https://www.linkedin.com/in/juniiorsilvadev/) 
