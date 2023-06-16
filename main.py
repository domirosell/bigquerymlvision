
# @author Domingo Rosell drosell@gmail.com
# @date 2023-06-16

from google.cloud import bigquery

# Image annotation by using Cloud Vision API
# Function is triggered after a file is uploded to a bucket
# Result is writen to BigQuery

def vision_api_bqml(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    project_id = 'project_id' # TO_DO_DEVELOPER
    dataset_id = 'dataset_id'       # TO_DO_DEVELOPER
    model_id = '`project_id.dataset_id.model_id`'  # TO_DO_DEVELOPER
    connection_id = '`region.connection_id`'  # TO_DO_DEVELOPER

    file = event
    table_id = file['name'].replace(".", "").replace(" ", "")
    destination = "`{}.{}.{}`".format(project_id, dataset_id ,table_id)
    final_table_vision_api = table_id + "_ml_vision_api"

    query_create_object_table = "CREATE EXTERNAL TABLE " + destination + \
                                ' WITH CONNECTION ' + connection_id + \
                                ' OPTIONS(' \
                                ' object_metadata = \'SIMPLE\',' \
                                ' uris = [\'gs://' + file['bucket'] + "/" + file['name'] + "']," \
                                " max_staleness = INTERVAL 1 DAY," \
                                " metadata_cache_mode = 'AUTOMATIC'" \
                                " );"

    query_cloud_vision_api = 'SELECT * FROM ML.ANNOTATE_IMAGE(' \
                             'MODEL ' + model_id + "," \
                             'TABLE ' + destination + "," \
                             "STRUCT(['label_detection'] AS vision_features));"

    bigquery_client = bigquery.Client(project=project_id)
    job = bigquery_client.query(query_create_object_table)
    job.result()
    print("Object table created!")

    job_config = bigquery.QueryJobConfig()
    job_config.destination = bigquery_client.dataset(dataset_id, project_id).table(final_table_vision_api)
    job_config.write_disposition = "WRITE_TRUNCATE"
    job = bigquery_client.query(query_cloud_vision_api, job_config=job_config)
    job.result()
    print("Image annotated by using Cloud Vision API!")