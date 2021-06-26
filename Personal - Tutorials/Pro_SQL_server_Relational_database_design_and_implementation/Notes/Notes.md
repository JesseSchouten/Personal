# Pro SQL Server Relational Database Design and Implementation
Start: 2021-6-26
End:
Description

### Davidson, L., & Moss, J. (2021). Pro SQL Server Relational Database Design and Implementation (sixth edition). Apress.

## Reminders:
- SELECT * FROM INFORMATION_SCHEMA.COLUMNS;

## Chapter 1:
### Codd's rules:
- All information in the relational database is represented in exactly one and only way.
- Each and every datum (atomic value) is guaranteed to be logically accesible by resorting to a combination of a table name, primary key value, and column name.
- NULL values are supported in the fully relational DBMS for respresenting missing information in a systematic way, independent of data type.
- The database description is represented at the same logical level as ordinary data, so authorized users can apply the same relational language to its interrogation as they apply to regular data.
- A relational system may support several languages and various models of terminal use. But there must be at least one language whose statements are expressible, per some well-defined synthax, as character strings and whose ability to support comprehensibility of the database system (: data definition, view definition, data manipulation, integrity constraints, authorization, transaction boundaries).
- All views that are theoretically updateable are also updateable by the system.
- The capability of handling a base relation or a derived relation as a single operand applied not only to data retrieval, but also inserted, updating and data deleting.
- Application programs and terminal activities remain logically unimpaired whenever any changed are made in either storage representation or access methods.
- Application programs and terminal activities remain logically unimpaired when information-preserving changed of any kind that theoretically permit unimpairment are made to the base tables.
- Integrity constraints specific to a particular relational database must be definable in the relational data sublanguage and storable in the catalog, not in the application process.
- The data manipulation sublanguage of a relational DBMS must enable application programs and terminal activities to remain logically unimpaired whether and whenever data are physically centralized/redistributed.
- If a relational system supports a low-level language, the low-level language can not be used to subvert or bypass the integrity rules or constraints expressed in the higher-level relational language. 

### Databases and schema's
- Use as few databases as possible for your needs (but not fewer).
- A goal in database development is to keep your code isolated in a single database if possible. Accessing a database on a different server is a practice disfavored by almost anyone who does db encoding: the performance can be really bad, and it is hard to track dependencies and it can be hard to test.

### Tables, rows and columns
- atomic values are values that cannot be broken up without losing it's original characteristics. 

### Working with NULL values
- Threat NULL values as UNKNOWN.
- All datatypes can represent a NULL. 
- Logical values can get tricky with logical expressions NULL <> NULL, because we don't know whether NULL is equal to NULL or not.

### Defining domains:
- The set of values that can be stored:
- Take EmployeeDateOfBirth: the domain refers to several aspects, the column must only store a date, it should be before the current date (else he/she was not born), the age should be between 16 and approx 70 (else he/she wouldn't be working). Values that do not correspond to this are clearly an error. We could set this to NULL. In chapter 7, they cover how to define this domain in code.
- Try to share domains amongst different variables: e.g. cardinalNumber: integer values 0 and greater, date: any valid date value, emailAddress: a string formatted as an actual email address, and 30CharacterString: A string that can be no longer then 30 characters (can be used for uuid's).


### Uniqueness constraints:
- Every table should typically at least have 1 uniqueness constraint, to fullfill the criteria that every table should be accessible by knowing the value of the key.
- Else, unless each row is unique from all other rows, there would be no way to effectively retrieve a single row.
- Failure to identify the keys is one of the biggest blunders a designer will make.
- A candidate key defines uniqueness of rows over a column or set of columns. 
- It can be best to limit the number of columns in a key as much as possible. 
- Natural key: connected to the database context.
- Surrogate key: usually a database-generated value that has no connection to the row data but is simply used as a stand-in for natural key for complexity and performance reasons (GUID).

### Chapter 11:
- Nonclustered and clustered indices.
- If you add a clustered index which is not the primary key, an additional 4-byte value will be added (known as the uniqueifier) to each value. Try to pick columns where the values are unique, with as less columns as possible.
- Clustered indices: max 1 per table. The chosen column will become part of every index of your table. A very common practice is to choose a surrogate key value, often the columns of the primary key constraint for a table, since the surrogate can be kept very small. This is a good decision because: it is typically a small key (often an integer: only 4 bytes or less with compression), but also because its a unique value.
- Caution: using a GUID for a surrogate key is common, but be carefull. It's 16 bytes which is quite wide. But also it has no logical value when generated, and new values are therefore placed randomly in a list of GUID's and end up causing page splits. To make this acceptable you can use NEWSEQUENTIALID() (or make your own). In SQL server 2021 and later, the SEQUENCE object can be used to generate unique values instead of GUID's.
- Typical reasons you use clustered indices for something other then surrogate key, include: data for which you need specific ranges typically, queries that needs to be accessed in order, queries returning large results, and queries identifying a relationship key.

### Quotes
- Generally speaking it is always a good idea to declare exactly the data you need for any operation that you expect to reuse (hence avoid select *, which might change when columns are added, etc).
- Both Primary key and Unique Key are used to uniquely define of a row in a table. Primary Key creates a clustered index of the column whereas a Unique creates an unclustered index of the column. 