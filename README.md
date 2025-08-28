# 🚀 Proyecto TFM – Detección de Fraude Financiero con Google Cloud Platform

Este repositorio contiene el desarrollo del Trabajo Fin de Máster (TFM) centrado en la **implementación de un pipeline ETL serverless en Google Cloud Platform (GCP)**, diseñado para la **detección y análisis de fraude financiero** utilizando datos sintéticos.

---

## 📂 Estructura del repositorio
.
├── dags/ # Código del DAG en Apache Airflow (Cloud Composer)
│ └── fraude_pipeline_dag.py
├── sql/ # Scripts de transformación en BigQuery
│ └── transformaciones.sql
├── looker/ # Capturas del dashboard en Looker Studio
│ ├── dashboard_overview.png
│ ├── analisis_fraude.png
│ ├── patrones_riesgo.png
│ └── visualizaciones.png
├── resultados/ # Evidencias de ejecución y validación
│ ├── composer_ejecucion.png
│ └── validacion_bq.png
└── README.md


---

## 🛠️ Tecnologías utilizadas

- **Google Cloud Storage (GCS)** → Almacenamiento de los datos de entrada.
- **BigQuery** → Procesamiento, transformación y enriquecimiento de datos.
- **Cloud Composer (Airflow)** → Orquestación del pipeline ETL.
- **Looker Studio** → Creación de dashboards interactivos para la visualización de resultados.
- **GitHub** → Control de versiones y documentación del proyecto.

---

## 📊 Descripción del pipeline

1. **Ingesta**: los datos sintéticos en formato CSV se cargan en un bucket de GCS.  
2. **Carga RAW**: los datos se almacenan en la tabla `financial_transactions_raw` en BigQuery.  
3. **Transformación CLEAN**: mediante SQL se crean nuevas variables, se normalizan campos y se calculan métricas de riesgo.  
4. **Visualización**: Looker Studio consume la capa *clean* para mostrar indicadores y patrones de fraude.  
5. **Orquestación**: todo el proceso es gestionado por un DAG en Cloud Composer (Airflow).

---

## 📈 Dashboard en Looker Studio

El dashboard diseñado permite analizar:

- **Volumen total de transacciones** y porcentaje de fraude.  
- **Distribución por canal de pago y dispositivo**.  
- **Evolución temporal de fraudes** con patrones de riesgo.  
- **Análisis geográfico** de operaciones sospechosas.  

📷 Las capturas del dashboard se encuentran en la carpeta [`/looker`](./looker).

---

## ✅ Resultados y validación

- El pipeline se ejecuta correctamente en Cloud Composer.  
- Se generan las tablas `financial_transactions_raw` y `financial_transactions_clean` en BigQuery.  
- Los datos limpios permiten construir dashboards interactivos y representativos para el análisis de fraude.  

📷 Evidencias de ejecución y validación disponibles en [`/resultados`](./resultados).

---

## 📚 Referencias

- Kaggle – *Synthetic Financial Datasets for Fraud Detection*  
- Google Cloud Documentation: BigQuery, Cloud Composer, Looker Studio  
- TFM – Universidad Nacional de Educación a Distancia (UNED)  

---

## 👨‍💻 Autor

- **Nombre y Apellidos**  
- Máster en [nombre del máster] – UNED  
- Año: 2025
