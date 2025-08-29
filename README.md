# TFM — Pipeline ETL Serverless en Google Cloud para Detección de Fraude

Este repositorio acompaña al Trabajo Fin de Máster (TFM) y documenta la construcción de un **pipeline ETL 100% serverless en Google Cloud Platform (GCP)** para preparar y exponer **datos financieros sintéticos** orientados a la **detección de fraude**.  
La solución automatiza la **ingesta** (GCS → BigQuery), la **transformación** (SQL en BigQuery) y la **exposición** (Looker Studio), todo ello **orquestado con Cloud Composer (Airflow)**.

---

## 📌 Alcance y objetivos

- Diseñar una **arquitectura cloud nativa** y **serverless**.
- Automatizar **ingesta**, **transformación** y **disponibilización** de datos.
- Generar una **capa analítica clean** con **variables derivadas y métricas de riesgo**.
- Exponer resultados en **dashboards** (Looker Studio) para negocio y analítica.

**Caso de uso**: Detección de patrones de fraude a partir de un dataset sintético con millones de transacciones.

---

## 🏗️ Arquitectura (alto nivel)

**Flujo ETL**  
`GCS (entrada CSV) → Cloud Composer/Airflow → BigQuery (raw → clean) → Looker Studio`

**Servicios GCP empleados**
- **Google Cloud Storage (GCS)**: *datalake* de entrada  
  - `gs://tfm-fraude-datalake-1754407122/entradas/`
- **Cloud Composer (Airflow)**: orquestación y monitorización  
  - Entorno: `fraude-composer-env` (Composer 2.13.8 · Airflow 2.10.5)  
  - Bucket DAGs: `gs://us-central1-fraude-composer-8ec45861-bucket/dags/`
- **BigQuery**: almacenamiento y transformación (SQL)  
  - Proyecto: `fraude-tfm-2025`  
  - Dataset: `fraude_dataset`  
  - Tablas: `financial_transactions_raw` y `financial_transactions_clean`
- **Looker Studio**: visualización interactiva

---

## 📂 Estructura del repositorio
```bash
.
├── fraude_pipeline_dag.py          # DAG de Airflow (Composer)
├── README.md                       # Este documento
├── looker/                         # Capturas de dashboards
│   ├── dashboard_overview.png
│   ├── analisis_fraude.png
│   ├── patrones_riesgo.png
│   └── importes_fraude.png
└── resultados/                     # Evidencias de ejecución
    ├── dag_ejecucion.png           # Airflow en verde (success)
    └── bigquery_tablas.png         # Validación tablas raw/clean
``` 
---

## ⚙️ Requisitos previos

- Proyecto en **GCP** con facturación activa.
- Permisos para: GCS, Composer, BigQuery y Looker Studio.
- **APIs habilitadas**: BigQuery, Cloud Composer, Cloud Storage.
- **gsutil** y **gcloud** (opcional si subes desde consola).

---

## 🚦 Despliegue

### 1) Subir el DAG a Cloud Composer
Copia el DAG al bucket de Composer:

```bash
gsutil cp fraude_pipeline_dag.py gs://us-central1-fraude-composer-8ec45861-bucket/dags/
```

### 2) Ubicar los datos de entrada en GCS

```bash
gs://tfm-fraude-datalake-1754407122/entradas/financial_fraud_detection_dataset.csv
```
### 3) Ejecutar el pipeline
Desde la UI de airflow:
  1. Abre fraude_pipeline_dag.
  2. Trigger DAG.
  3. Verifica nodos en verde (success): inicio → cargar_csv_gcs → transformar_datos → fin.

---

## 🗄️ Modelo de datos (BigQuery)

fraude-tfm-2025.fraude_dataset.financial_transactions_raw
Capa raw con los datos tal y como llegan desde GCS. Base para auditoría, reprocesos y trazabilidad.

fraude-tfm-2025.fraude_dataset.financial_transactions_clean
Capa clean con limpieza, normalización y variables derivadas: métricas temporales, bins de importe, scores de riesgo, contadores por ventana, indicadores por canal y dispositivo, etc. Es la tabla base para dashboards y analítica.

---

## 🧠 Transformación principal (BigQuery)

La transformación de datos se realiza directamente en **BigQuery** a través de SQL, orquestada desde el DAG `fraude_pipeline_dag.py`.  

### Objetivos principales
- Conversión de la capa **raw** en **clean**.  
- Derivación de variables temporales (hora, día, semana, trimestre).  
- Normalización de campos (ubicaciones, categorías de dispositivos y canales).  
- Cálculo de métricas de riesgo:  
  - `transaction_risk_score` (combinación de anomalías geográficas, velocidad y desviación de gasto).  
  - Señales de riesgo (`risk_signals_count`).  
  - Bins de importe y franjas horarias.  
  - Variables dummy por canal/dispositivo.  

### Ejemplo (extracto de la query dentro del DAG)

```sql
CREATE OR REPLACE TABLE `fraude-tfm-2025.fraude_dataset.financial_transactions_clean` AS
SELECT
  transaction_id,
  TIMESTAMP(timestamp) AS timestamp,
  EXTRACT(YEAR FROM TIMESTAMP(timestamp)) AS year,
  EXTRACT(MONTH FROM TIMESTAMP(timestamp)) AS month,
  ...
FROM `fraude-tfm-2025.fraude_dataset.financial_transactions_raw`
WHERE amount IS NOT NULL;

---

## 🔎 Validación (consultas útiles)

### Conteo de registros
```sql
SELECT 'raw'  AS capa, COUNT(*) AS n FROM `fraude-tfm-2025.fraude_dataset.financial_transactions_raw`
UNION ALL
SELECT 'clean' AS capa, COUNT(*) AS n FROM `fraude-tfm-2025.fraude_dataset.financial_transactions_clean`;
...

---

