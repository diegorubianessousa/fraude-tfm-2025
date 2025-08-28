from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    'start_date': days_ago(1)
}

with DAG(
    dag_id='fraude_pipeline_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['fraude', 'bigquery', 'gcs']
) as dag:

    inicio = DummyOperator(task_id='inicio')

    carga_gcs_a_bq = GCSToBigQueryOperator(
        task_id='cargar_csv_gcs',
        bucket='tfm-fraude-datalake-1754407122',
        source_objects=['entradas/*.csv'],
        destination_project_dataset_table='fraude-tfm-2025.fraude_dataset.financial_transactions_raw',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
        autodetect=True
    )

    transformacion_query = """\
    CREATE OR REPLACE TABLE `fraude-tfm-2025.fraude_dataset.financial_transactions_clean` AS
    SELECT
    transaction_id,
    TIMESTAMP(timestamp) AS timestamp,
    EXTRACT(YEAR FROM TIMESTAMP(timestamp)) AS year,
    EXTRACT(MONTH FROM TIMESTAMP(timestamp)) AS month,
    EXTRACT(DAY FROM TIMESTAMP(timestamp)) AS day,
    EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) AS day_of_week,
    EXTRACT(HOUR FROM TIMESTAMP(timestamp)) AS hour,

    CASE
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 1 THEN 'Domingo'
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 2 THEN 'Lunes'
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 3 THEN 'Martes'
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 4 THEN 'Miércoles'
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 5 THEN 'Jueves'
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 6 THEN 'Viernes'
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) = 7 THEN 'Sábado'
    END AS day_name,

    CASE WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 0 AND 6 THEN 1 ELSE 0 END AS is_night,
    CASE WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) IN (1, 7) THEN 1 ELSE 0 END AS is_weekend,
    CASE WHEN is_fraud THEN 1 ELSE 0 END AS is_fraud_num,

    amount,
    transaction_type,
    merchant_category,
    LOWER(location) AS location,
    device_used,
    payment_channel,

    SAFE_CAST(time_since_last_transaction AS FLOAT64) AS time_since_last_transaction,
    SAFE_CAST(spending_deviation_score AS FLOAT64) AS spending_deviation_score,
    SAFE_CAST(velocity_score AS FLOAT64) AS velocity_score,
    SAFE_CAST(geo_anomaly_score AS FLOAT64) AS geo_anomaly_score,

    CASE
      WHEN amount < 50 THEN '<50'
      WHEN amount < 200 THEN '50-200'
      WHEN amount < 1000 THEN '200-1000'
      ELSE '>1000'
    END AS amount_bin,

    CASE
      WHEN device_used = 'mobile' THEN 'Mobile'
      WHEN device_used = 'web' THEN 'Web'
      ELSE 'Physical'
    END AS device_type_category,

    CASE
      WHEN merchant_category IN ('online', 'travel') THEN 'Digital'
      WHEN merchant_category IN ('entertainment', 'retail') THEN 'Hibrido'
      ELSE 'Tradicional'
    END AS merchant_category_group,

    CASE
      WHEN (
        (CASE WHEN amount > 538.40 THEN 1 ELSE 0 END) +
        (CASE WHEN device_used = 'web' THEN 1 ELSE 0 END) +
        (CASE WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 0 AND 6 THEN 1 ELSE 0 END)
      ) >= 3 THEN 'ALTO'
      WHEN (
        (CASE WHEN amount > 538.40 THEN 1 ELSE 0 END) +
        (CASE WHEN device_used = 'web' THEN 1 ELSE 0 END) +
        (CASE WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 0 AND 6 THEN 1 ELSE 0 END)
      ) = 2 THEN 'MEDIO'
      ELSE 'BAJO'
    END AS riesgo_transaccion,

    LOG(amount + 1) AS log_amount,

    (
      COALESCE(SAFE_CAST(geo_anomaly_score AS FLOAT64), 0) +
      COALESCE(SAFE_CAST(velocity_score AS FLOAT64), 0) +
      COALESCE(SAFE_CAST(spending_deviation_score AS FLOAT64), 0)
    ) AS transaction_risk_score,

    CASE
      WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 0 AND 5 THEN 'Madrugada'
      WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 6 AND 11 THEN 'Mañana'
      WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 12 AND 14 THEN 'Mediodía'
      WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 15 AND 18 THEN 'Tarde'
      WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 19 AND 21 THEN 'Noche'
      ELSE 'Medianoche'
    END AS hour_bin,

    CASE
      WHEN EXTRACT(DAYOFWEEK FROM TIMESTAMP(timestamp)) IN (1, 7) THEN 'Fin de Semana'
      ELSE 'Entre Semana'
    END AS week_part,  

    CASE WHEN payment_channel = 'card' THEN 1 ELSE 0 END AS is_card,
    CASE WHEN payment_channel = 'ach' THEN 1 ELSE 0 END AS is_ach,
    CASE WHEN payment_channel = 'upi' THEN 1 ELSE 0 END AS is_upi,
    CASE WHEN payment_channel = 'wire_transfer' THEN 1 ELSE 0 END AS is_wire_transfer,
    CASE WHEN device_used = 'pos' THEN 1 ELSE 0 END AS is_pos,
    CASE WHEN device_used = 'web' THEN 1 ELSE 0 END AS is_web,
    CASE WHEN device_used = 'mobile' THEN 1 ELSE 0 END AS is_mobile,

    EXTRACT(QUARTER FROM TIMESTAMP(timestamp)) AS quarter,
    CEIL(EXTRACT(DAY FROM TIMESTAMP(timestamp)) / 7) AS week_of_month,
    CASE WHEN EXTRACT(DAY FROM TIMESTAMP(timestamp)) >= 28 THEN 1 ELSE 0 END AS is_end_of_month,

    (
      (CASE WHEN amount > 538.40 THEN 1 ELSE 0 END) +
      (CASE WHEN device_used = 'web' THEN 1 ELSE 0 END) +
      (CASE WHEN EXTRACT(HOUR FROM TIMESTAMP(timestamp)) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) +
      (CASE WHEN SAFE_CAST(geo_anomaly_score AS FLOAT64) > 0.7 THEN 1 ELSE 0 END)
    ) AS risk_signals_count,

    ((amount - 500) / 600) AS amount_zscore,

    SAFE_DIVIDE(amount, SAFE_CAST(time_since_last_transaction AS FLOAT64)) AS amount_per_time,

    CASE
      WHEN LOWER(location) IN ('new york', 'singapore', 'tokyo') THEN 'Alta'
      WHEN LOWER(location) IN ('dubai', 'berlin', 'toronto') THEN 'Media'
      ELSE 'Baja'
    END AS location_risk_level,

    (
      CASE WHEN payment_channel = 'wire_transfer' THEN 2
          WHEN payment_channel = 'upi' THEN 1
          ELSE 0
      END +
      CASE WHEN device_used = 'web' THEN 2
          WHEN device_used = 'mobile' THEN 1
          ELSE 0
      END
    ) AS channel_device_risk,

    DATE_DIFF(
      DATE(TIMESTAMP(timestamp)),
      DATE(MIN(TIMESTAMP(timestamp)) OVER (PARTITION BY sender_account)),
      DAY
    ) AS account_age_days,

    COUNT(*) OVER (
      PARTITION BY device_used, DATE(TIMESTAMP(timestamp))
    ) AS daily_device_volume,

    COUNT(*) OVER (
      PARTITION BY sender_account
      ORDER BY TIMESTAMP(timestamp)
      ROWS BETWEEN 100 PRECEDING AND CURRENT ROW
    ) AS sender_tx_last_hour,

    RANK() OVER (
      PARTITION BY DATE(TIMESTAMP(timestamp))
      ORDER BY amount DESC
    ) AS daily_amount_rank,

    SAFE_DIVIDE(
      SAFE_CAST(velocity_score AS FLOAT64),
      LOG(amount + 1)
    ) AS velocity_amount_ratio
    FROM `fraude-tfm-2025.fraude_dataset.financial_transactions_raw`
    WHERE amount IS NOT NULL
    """

    ejecutar_transformacion = BigQueryInsertJobOperator(
        task_id='transformar_datos',
        configuration={
            "query": {
                "query": transformacion_query,
                "useLegacySql": False
            }
        }
    )

    fin = DummyOperator(task_id='fin')

    inicio >> carga_gcs_a_bq >> ejecutar_transformacion >> fin