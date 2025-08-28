# 🚀 TFM — Pipeline ETL Serverless en Google Cloud para Detección de Fraude

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

