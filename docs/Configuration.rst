Configuration
=============

Using Coralogix Python SDK requires these mandatory parameters:

* **PRIVATE KEY** - A unique ID which represents your company. This ID will be sent to your mail once you register to `Coralogix`.

* **APPLICATION NAME** - The name of your main application. For example, a company named *"SuperData"* could insert the *"SuperData Production"* string parameter; or if they want to debug their test environment, they might insert the *"SuperData – Test"*.

* **SUBSYSTEM NAME** - Your application probably has multiple subsystems. For example: Backend servers, Middleware, Frontend servers etc. In order to help you examine and filter the data you need, inserting the subsystem parameter is vital.

Region Configuration
--------------------

* **REGION** - The Coralogix region to use for log ingestion. This parameter is **mandatory**. Supported regions are:

  * **AP1** - Mumbai (AWS: ap-south-1)
  * **AP2** - Singapore (AWS: ap-southeast-1)
  * **AP3** - Jakarta (AWS: ap-southeast-3)
  * **EU1** - Ireland (AWS: eu-west-1)
  * **EU2** - Stockholm (AWS: eu-north-1)
  * **US1** - Ohio (AWS: us-east-2)
  * **US2** - N. Virginia (AWS: us-east-1)

  You can specify the region either by:

  * Passing the ``region`` parameter when initializing the logger
  * Setting the ``CORALOGIX_REGION`` environment variable

  **Note**: If no region is specified (neither as a parameter nor via environment variable), the SDK will raise a ``ValueError``. The SDK uses modern regional endpoints (``ingress.{region}.coralogix.com``) as per the Coralogix endpoint modernization effective March 31, 2026.