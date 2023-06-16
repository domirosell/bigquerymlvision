# bigquerymlvision
Image annotation by using BQML + Object Tables + Cloud AI Vision


First you must create a connection and a model in BigQuery, following these steps:

1. Create storage resource connection in bigquery (BigLake)

BigQuery --> Add --> Connections to external data sources:
Connection type
BigLake and remote functions (Cloud Resource)

Note that a service account will be created for the connection. Please grant it the roles/serviceusage.serviceUsageConsumer role, or a custom role with the serviceusage.services.use permission.


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

The connection service account will also need permissions to read the file from the bucket.


4. You can know check in BQ the scores returned by the Cloud AI Vision in a friendly way

SELECT
JSON_VALUE(label_annotations.description) AS description,
JSON_VALUE(label_annotations.mid) AS mid,
JSON_VALUE(label_annotations.score) AS score,
JSON_VALUE(label_annotations.topicality) AS topicality,
*


FROM `project_id.dataset_id.table_id_ml_vision_api` ,
UNNEST(JSON_QUERY_ARRAY(ml_annotate_image_result.label_annotations)) AS label_annotations

Example:

<img width="880" alt="image" src="https://github.com/domirosell/bigquerymlvision/assets/136735618/d991dbf3-9da8-4ce7-b696-77f443fad282">

Provided links for further information:
https://cloud.google.com/bigquery/docs/working-with-connections - Working with connections
https://cloud.google.com/bigquery/docs/annotate-image - Annotate object table images with BQML
https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image#syntax
https://cloud.google.com/bigquery/docs/remote-function-tutorial?hl=es-419 - Remote functions may also be used



