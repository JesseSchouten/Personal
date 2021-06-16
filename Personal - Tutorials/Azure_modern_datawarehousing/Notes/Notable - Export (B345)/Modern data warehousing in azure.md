---
title: Modern data warehousing in azure
created: '2021-06-16T09:40:10.767Z'
modified: '2021-06-16T22:06:32.492Z'
---

# Modern data warehousing in azure

Start: 
End:
Description: 

### How, M. (2020). Beyond the Modern Data Warehouse. In The Modern Data Warehouse in Azure (pp. 229-274). Apress, Berkeley, CA.

## Chapter 1:
* Resource group means that admins can assign permissions to that single level and control permissions for the entire system.
* As the subscription gets more use, create resource groups per project or application, per environment. So for a single data warehouse, you may have a develop, test and production resource group.
* Tags might be another usefull feature, it allows admins to label so that resources can be found easily.
* Service principals: services accounts that can be assigned acces to many of the resources in a resource groups without any human employees having access to the data.
* Proposed naming conventions for resources: Department (e.g. markt for marketing), application/service (e.g. sqldb for a sql database), environment (e.g. dev, test) and deployment region (e.g. eus for East US). Examples: mdwa-sqldb-dev-eus, mdwa-syndb-dev-eus.

## Chapter 2: The SQL engine
* The four V's: Volume, Variety, Velocity and Value
* Two types of SQL engines, Azure synapse analytics & Azure SQL Database, both only suitable for tabular format, so no unstructured data (documents, JSON data, multimedia files directly). Consider Azure CosmosDB for document data.
* Azure Synapse: Massively Paralell Processing (MPP), underpinned by SQL server engine.
* Azure SQL database: optimized for reads and writes, can scale up to 100 TB. Intelligent query processing and can be highly reactive to changes in runtime conditions (allowing for peak performance to be maintained). 
    * Deployment options: Managed instance (close to on-premise), Elastic pool (utilize a pool of compute resources for a lower cost of ownership).
* If you database is less than 1 TB, not likely to increase -> Azure SQ: DB. 
* As volume increases (e.g. 100 TB), azure synapse is better in terms of performance, though it likely stays more expensive!

# Chapter 3: The integration engine:
* Azure Data Factory (ADF), quote: 'Within Azure, there is really only one option for cloud scale data integration and this is Azure Data Factory (ADF). No other engines exist within the Azure service itself, and while this may seem limiting, it is actually refreshing because there is no real debate to be had; if you want to remain on the Azure platform, you use ADF.'
* First, in ADF v2, you had to write JSON locally and deploy it to ADF using powershell. Now this is all in the UI, though: the underlying JSON is still accesible, and it still is the easiest way to debug.
* Building blocks in ADF: Linked services, Triggers, Datasets, Pipelines, Activities.
* Linked services: any credentials should be stored in azure keyvault. Data store linked services allow connection to over 80 different data stores (Azure SQL DB, Azure data lake, etc); fetch and deposit data. Azure store linked services allow the execution of jobs on azure compute resources (Databricks, azure functions, azure synapse, etc); execute jobs on Azure-based compute resources. Applying a linked service connection means that we can use a service principal to authenticate our Data Factory and then just ensure that the service principal is added to a group that has access to the resource we want to connect to.
* Triggers: method by which pipelines are invoked. Possible to test in debug mode, which runs on a debug cluster, hence not actually running the components. 3 trigger categories: schedule triggers (e.g. time-based schedule), tumbling window triggers (; slice & partitioning, e.g. set to daily 5 years in the past will create 1825 data slices sequentially) & event triggers (; knows whats going on in the source data and invokes script based on this activity, called an event).
* Datasets: Layer on top of a linked service (connection) to implement logic that allows you to access specific tables, files, directories and others. A common usage of a dataset is to specify a specific folder location in a cloud data store to copy data from or to.
* Pipelines and Activities: Pipelines are the heart of the engine, defining the routes of activities that are to be executed. A pipeline contains multiple JSON objects called activities. Activities can be divided in four groups: External compute activities (e.g. databricks, machine learning & SQL stored procedures); no dataset required, Internal compute activities (e.g. Copy data activity, ); linked service & dataset required, Iteration and conditional activities (e.g. set and append, execute pipeline, for each loop, wait, if condition) and web activities (e.g. generic http calls, not for large-scale data processing; no heavy lift work).
* ADF can be integrated directly into a Git repo hosted either on github or azure devops workspace. When specifying the source control option, you can branch the account and project to associate your ADF instance to, and choose any branch in the repo. You then can create pull requests in order to publish code into the main branch.
* Things to consider to create a well organized ADF instance: Use folders, Use a clear naming convention (source system names, source and sink references, pipeline purpose, etc), use templates (; they ensure developers can easily pick from agreed patterns when building a data factory).

# Chapter 5: The role of the data lake
* Working with databricks to clean data is beyond the scope of this book, however: all required cleaning activities can be easily undertaken using either: Spark SQL, Python, R or Scala. Benefits of cleaning data this way, is that the data does not have to move as far. Databricks connects to the data lake by impersonating a service principal, and then exploits its deep integration with the HDFS ecosystem. Additionally,a truly immense file that would be difficult or too time consuming to load into SQL can easily be processed by Databricks as its partitions will be exploited and the workload parallelized.
* Databricks can rack up costs: be cautious with features such as auto-scaling and terminate clusters when not needed!




