# bigquerymlvision
Image annotation by using BQML + Object Tables + Cloud Vision API


First you must create a connection and a model in BigQuery, following these steps:

1. Create storage resource connection in bigquery (BigLake)

BigQuery --> Add --> Connections to external data sources:
Connection type
BigLake and remote functions (Cloud Resource)


2. Create the MODEL. In this example, we'll be using a Remote model provided by GCP (CLOUD_AI_VISION_V1).


CREATE MODEL `project_id.dataset_id.model`
REMOTE WITH CONNECTION `region.my-connection`
OPTIONS(REMOTE_SERVICE_TYPE="CLOUD_AI_VISION_V1")


3. Create the cloud functions and associate a GCS trigger.
Different features may be used as vision features, in this example label_detection has been used.

Just set these variables properly, upload an image to your bucket and let magic happen in GCP :-)

 project_id = 'project_id' # TO_DO_DEVELOPER
 dataset_id = 'dataset_id'       # TO_DO_DEVELOPER
 model_id = '`project_id.dataset_id.model_id`'  # TO_DO_DEVELOPER
 connection_id = '`region_id.connection_id`'  # TO_DO_DEVELOPER

The object table will be created in the specified project & dataset. In the same dataset, the result will be written with suffix _ml_vision_api

Provided links for further information:
https://cloud.google.com/bigquery/docs/working-with-connections - Working with connections
https://cloud.google.com/bigquery/docs/annotate-image - Annotate object table images with BQML
https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image#syntax
https://cloud.google.com/bigquery/docs/remote-function-tutorial?hl=es-419 - Remote functions may also be used



