# 🚀 Proyecto TFM – Pipeline ETL Serverless en Google Cloud para Detección de Fraude

Este repositorio contiene el código, recursos y documentación asociados al **Trabajo Fin de Máster (TFM)**, cuyo objetivo es diseñar e implementar un **pipeline ETL serverless en Google Cloud Platform (GCP)** para el tratamiento y análisis de datos financieros sintéticos orientados a la **detección de fraude**.

---

## 📌 Objetivos del proyecto

- Diseñar una arquitectura cloud **serverless** y modular.  
- Automatizar la ingesta, transformación y almacenamiento de datos.  
- Generar una capa analítica enriquecida para la detección de patrones de fraude.  
- Desplegar dashboards interactivos en **Looker Studio** que faciliten el análisis por perfiles técnicos y de negocio.  

---

## 🏗️ Arquitectura

La solución implementada se compone de los siguientes servicios de Google Cloud:

- **Google Cloud Storage (GCS)** → almacenamiento de los ficheros CSV (datalake).  
- **Cloud Composer (Airflow)** → orquestación y monitorización del pipeline ETL.  
- **BigQuery** → motor de análisis para las capas *raw* y *clean*.  
- **Looker Studio** → visualización de métricas y patrones de fraude.  

📌 **Flujo ETL:**  
`GCS → Composer (Airflow) → BigQuery (raw / clean) → Looker Studio`

---

## 📂 Estructura del repositorio
┣ 📂 dags/ # DAG de Airflow (fraude_pipeline_dag.py)
┣ 📂 looker/ # Capturas de los dashboards de Looker Studio
┣ 📂 logs/ # Evidencias de ejecución y validación
┣ 📜 README.md # Documentación principal
┣ 📜 LICENSE # Licencia del proyecto

---

🔒 Licencia

Este proyecto se distribuye bajo licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, siempre citando al autor original.

👤 Autor
Diego Rubianes Sousa
Trabajo Fin de Máster – Ingeniería de Datos
UNED – 2025
