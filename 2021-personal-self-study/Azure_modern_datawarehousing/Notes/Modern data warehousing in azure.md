---
title: Modern data warehousing in azure
created: '2021-06-16T09:40:10.767Z'
modified: '2021-06-23T06:49:29.457Z'
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
* A variable is scoped to a single pipeline and can only be assigned to, and read
from, using activities within that pipeline. There are specific activities available to set a
variables’ value and to append elements to it if it were an array.
* A parameter is defined within the pipeline but can accept values when the pipeline
is invoked whether that be from an “Execute Pipeline” activity or via a totally separate
calling service such as a trigger, PowerShell, or an Azure Function.
* Methods and configuration used for loading data in certain scenarios are referred to as **patterns**. They consist of: Linear, Parent-child, Iterative parent child, 

# Chapter 4:
* Raw layer: raw data layer (e.g. blob), should be the rawest format. clean layer: takes data from the raw data layer and cleans based on (potentially very complex) business logic. Transformed layer: takes data from the cleaning layer, and performs aggregations and other operations. Can get very complex, but due to the fact that the cleaning layer took away some work already, the sole focus can lie on the logic itself.
* Many services within azure can generate events when things happen, which can be used for event ingestion. An example is Blob Storage, which can fire events when new files are added or existing files are deleted, from which Azure Data Factory can listen for those events and then trigger a pipeline, utilizing the metadata send with the event (e.g. file name and location).
* Event-based ingestion advantages: quicker processing of files, a sooner updated warehouse. Will not become very complex due to several processes/schedules potentially running in the same window (like at batch processing/scheduling).
* Event-based ingestion risks: it's not the engine itself that decides the pace, but rather the supplier of data itself. You MUST make sure that you are always able to receive the events and process the data. Finally, a mechanism is needed to determine when all files have arrived in clean format, and the warehouse is ready to be refreshed. The can quickly become a complex mesh of intertwined dependencies. This brings a risk where the data warehouse will never be processed because the necassary files were never all ready at the right time. These processes should be monitored closely to ensure the warehouse will not be starved.
* A dependency resolution engine handles the way files are handled further in the pipeline, whilst being dependent on the succesfull execution of previous steps.
* E.g. a dependency resolution query would be triggered each time a dataset is succesfully cleaned, and would comprise of several steps. Often stored procedures are used in this process.
* We can let the policy of the dependency resolution engine determine whether we always have to await the datasets in step 1 (before starting step 2), rather then just using an old version for some of the datasets in step 1 (:a low priority dataset). The dataset can be marked as 'low priority' when the data in the dataset does not change often for example.
* Event queueing can be used when to handle incoming events for example in cases when the system is down. The stored events can be picked up when the system resumes.
* Azure SQL DB is a good fit for event based ingestion compared to azure synapse. Primarily because it is specifically well suited for smaller/easily digestible batches. ADF can be used to push the data to the database.
* The lambda architecture approach is defined as a blend of streaming and batch-based ingestion.

# Chapter 5: The role of the data lake
* Working with databricks to clean data is beyond the scope of this book, however: all required cleaning activities can be easily undertaken using either: Spark SQL, Python, R or Scala. Benefits of cleaning data this way, is that the data does not have to move as far. Databricks connects to the data lake by impersonating a service principal, and then exploits its deep integration with the HDFS ecosystem. Additionally,a truly immense file that would be difficult or too time consuming to load into SQL can easily be processed by Databricks as its partitions will be exploited and the workload parallelized.
* Databricks can rack up costs: be cautious with features such as auto-scaling and terminate clusters when not needed!

# Chapter 6: The role of the data contract
* Schema evolution: changing datasets over time (column names, datatypes or degree of quality).
* To handle changes, rule definitions should be stored centrally so you leverage the advantage of only having to adjust the rule for (potentially a large number of) datasets in a single spot.
* Data contract: overarching set of metadata describing how incoming data should look.
* data contract are typically considered to be sql related, and they show an example of a stored procedure type of action in which some regards get updated of they exists, or inserted if they dont.
* One of the questions they ask if whether to define all metadata (i.e. datatypes or columns in the table) manually, or to automate it. Because it can be annoying to define a large number of columns yourself. They mention it is case dependent.
* validation of contracts: in SQL this is enforced by the data schema, e.g. essential values that shouldn't be null as well as data types itself. Any contracts that are rejected should be send back to the author, which could be done using some kind of alerting mechanism.
* Assuming you host the data in SQL warehouse 2, you should store the contracts on a different sql server, in order to protect your SQL engine on which your data warehouse is hosted.
* When modifiying data contracts, rely upon versioning software such as git. This enables you to roll back if stuff goes southways.

# Remaining noteworthy items (not from book per se):
* Service principals help avoid having to create fake users to authenticate between resources.
* A managed identity manages the service principals for you and is kind of a layer on top of the service principals. 
* There are two types of managed identities: system-assigned (;tied to resource directly) & user-assigned (; created independent of resource, can be used between different resources).
* The problem with managed identities can be that not all resources support them.




