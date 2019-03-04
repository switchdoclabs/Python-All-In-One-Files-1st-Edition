import pandas as pd
from google.cloud import bigquery





# sample query from:
# https://cloud.google.com/bigquery/public-data/openaq#which_10_locations_have_had_the_worst_air_quality_this_month_as_measured_by_high_pm10
QUERY = """
        SELECT provider_city, provider_state, drg_definition, average_total_payments, average_medicare_payments
        FROM `bigquery-public-data.cms_medicare.inpatient_charges_2015`
        WHERE provider_city = "GREAT FALLS" AND provider_state = "MT"
        ORDER BY provider_city ASC
        LIMIT 1000
        """
#WHERE pollutant = "pm10" AND timestamp > "2017-04-01"

client = bigquery.Client.from_service_account_json(
            'MedicareProject2-1223283ef413.json')
query_job = client.query(QUERY)
df = query_job.to_dataframe()
print (df)

print (df.head(3))
