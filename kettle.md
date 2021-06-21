

## 组件清单

### Input  

| Name                                | Description                                                  |
| ----------------------------------- | ------------------------------------------------------------ |
| CSV file input                      |                                                              |
| Data Grid                           |                                                              |
| De-serialize from file              |                                                              |
| Email messages input                |                                                              |
| ESRI Shapefile Reader               |                                                              |
| Fixed file input                    |                                                              |
| Generate random credit card numbers |                                                              |
| Generate random value               |                                                              |
| Generate Rows                       | 生成行（Generate Rows ）：这个步骤输出一定数量的行，缺省为空。可选包括一定数量的静态字段。 |
| Get data from XML                   |                                                              |
| Get File Names                      |                                                              |
| Get Files Rows Count                |                                                              |
| Get repository names                |                                                              |
| Get SubFolder names                 |                                                              |
| Get System Info                     | 获取系统信息(get system info):这个步骤从 Kettle 环境中获取信息。 |
| Get table names                     |                                                              |
| Google Analytics                    |                                                              |
| GZIP CSV Input                      |                                                              |
| JSON Input                          |                                                              |
| LDAP Input                          |                                                              |
| LDIF Input                          |                                                              |
| Load file content in memory         |                                                              |
| Microsoft Access Input              |                                                              |
| Microsoft Excel Input               |                                                              |
| Mondrian Input                      |                                                              |
| OLAP Input                          |                                                              |
| Parquet Input                       |                                                              |
| Property Input                      |                                                              |
| RSS Input                           |                                                              |
| S3 CSV Input                        |                                                              |
| Salesforce Input                    |                                                              |
| SAS Input                           |                                                              |
| Table Input                         | 表输入(table Input)：常用来利用连接和SQL，从数据中读取信息，自动生成基本的SQL语句。 |
| Text file input                     | 文本文件输入(text input)：读取大量不同的文本文件。大多是通过工具生成的CSV文件。 |
| XBase input                         |                                                              |
| XML Input Stream (StAX)             |                                                              |
| Yaml Input                          |                                                              |
| HL7 Input                           |                                                              |



Cube输入(文件反序列化)(De-serialize from file):从二进制 Kettle Cube 文件中读取数据行。 备注：这个步骤仅仅用来存储短期数据。不同版本之间不保证文件的格式一样。

XBase输入： 使用这一步可以读取大多数被称为 XBase family派生的 DBF文件。

Excel输入：利用这个步骤可以从 Kettle 支持的系统的 Excel文件里面读取数据。

XML输入：这个步骤允许你读取存储在 XML 文件中的数据。它也提供一个接口，你可以定义你想读取的文件名、XML 文件的数据重复部分、获取的字段等。你可以指定元素或属性字段。

获取文件名(Get File Names)：这个步骤可以获取系统的文件名信息。

文本文件输出(Text File Output)：

表输出(Table output)：这个步骤可以存储信息到数据库表中。

插入/更新(Insert/Update):这个步骤利用查询关键字在表中搜索行。如果行没有找到，就插入行。如果能被找 到，并且要被更新的字段没有任何改变，就什么也不做。如果有不同，行就会被更新。

更新（Update ）：这个步骤类似于插入/更新步骤，除了对数据表不作插入操作之外。它仅仅执行更新操作。

删除(Delete)：这个步骤类似于上一步，除了不更新操作。所有的行均被删除。

Cube output(序列化到文件)(Serialize to file):这一步骤存储数据到一个二进制文件。这个步骤有个优势就是回读的时候，文本文件的内容不需要解析。这是因为元数据也同时存储在 CUBE 文件里面。

XML输出：这个步骤允许你从源中写入行到一个或者多个 XML 文件。

EXCEL输出：利用这个步骤，在 Kettle 支持的系统中，你可以写入数据到一个或者多个Excel 文件中。

Access 输出（Microsoft Access Output）: 允许你在转换中创建一个新的 Access 数据库文件作为输出。

数据库查询（Database lookup）:这个步骤类型允许你在数据库表中查找值。

流查询（Stream lookup）:这个步骤类型允许你从其它步骤中查询信息。首先，“源步骤”的数据被读到内存中，然后被用来从主要的流中查询数据。

调用数据库存储过程(Call DB Procedure):这个步骤允许你运行一个数据库存储过程，获取返回结果。

HTTP 客户端(HTTP Cient):HTTP 客户端根据一个附带条件的基准 URL，来调用一个简单的调用。

字段选择 (Select values) :这个步骤常常用来 选择字段 重命名字段 指定字段的长度或者精度 

下面是三个不同标签的功能： 

​      选择和修改：指定需要流到输出流中的字段的精确顺序和名称 

​      删除：指定必须从输出流中删除的字段 

​      元数据：修改元数据字段的名称、类型、长度和精度 

过滤记录(Filter rows):这个步骤允许你根据条件和比较符来过滤记录。 一旦这个步骤连接到先前的步骤中，你可以简单的单击“<field>”，“=”和“<value>” 区域来构建条件。 

排序记录（Sort rows）:这个步骤利用你指定的字段排序行，无论他们是按照升序还是降序。

备注：当行数超过 5000 行的时候，Kettle 使用临时文件来排序行。

添加序列(Add sequence):这个步骤在流中增加一个序列。一个序列是在某个起始值和增量的基础上，经常改变的整数值。你可以使用数据库的序列，也可以使用 Kettle 决定的序列。

备注：Kettle 序列在同一个转换中是唯一使用的。每一次转换运行的时候，序列的值又会重新循环一次（从开始值开始）

空操作-什么都不做(Dummy-do nothing):这个操作什么都不做。它的主要作用是，在你想测试什么的时候，充当一个占位符。例如有一个转换，你至少需要两个彼此连接的步骤。如果你想测试文本文件输入步骤，你可以将它连接到一个 Dummy 步骤。

行转列(Row Normaliser):这个步骤转动表，标准化数据。

拆分字段（Split Fields）:这个步骤允许你根据分隔符来拆分字段。

去除重复记录(Unique rows)：这个步骤从输入流中称移除重复的记录。

分组(Group By)：这个步骤允许你通过定义分组的字段来计算值。

例如：计算产品的平均销售额，获取库存的黄色衬衫的数量等等。

设置为空值(Null if):如果某个字符串的值等于指定的值，设置那个值为空。

计算器（Calculator ）:这个步骤提供一个功能列表，可以在字段值上运行。

计算器的一个重要优势是，它有着几倍于常用的 JavaScript 脚本的速度。

增加 XML （XML Add ）:这个步骤允许你将在 XML 中的行字段内容编码，XML 以字符串字段的形式添加到行中。

增加常量（Add constants ）:这个步骤很简单，主要是添加常量到流中。

它的使用也很容易：用字符串形式指定名称，类型和值。利用选择的数据类型指定转换格式。

行转列（Row Denormaliser ）:这个步骤允许你通过查询键值对来反向规格化数据。也可以立即转换数据类型。

行扁平化（Flattener ）:这个步骤允许你扁平化预备的数据。

值映射（Value Mapper ）:这个步骤简单的映射字符串，从一个值映射到另一个值。通常你想解中转换表的问题,不管怎么说，这是一种可选的方案：简单的将转换表作一部分。

例如：如果你想替换 Language codes，你可以：

使用的字段名：LanuguageCode 目标字段名：LanguageDesc

源值/目标值：EN/English,FR/French,NL/Dutch,ES/Spanish,DE/German,…

被冻结的步骤（Blocking step ）:它冻结所有的输出，直到从上一步骤来的最后一行数据到达,最后一行数据将发送到下一步。你可以使用这个步骤触发常用插件、存储过程和 Java Script等等。

记录关联（笛卡尔输出）（Join Rows-Cartesian Product ）:这个步骤允许你组合输入流中的所有行（笛卡尔输出）。

数据库连接（Database Join ）:这个步骤允许你使用先前步骤的数据，运行一个数据库查询。

能够指定查询参数：在 SQL 查询中使用“？” ; 在 SQL 查询中使用数据网格中的字段

合并记录（Merge rows ）:这个步骤允许你比较两个行流。如果你想在两个不同的时间比较比较数据，这是非常有用的。它常被用于数据仓库源系统没有包含最后更新日期的情况。

两个行流被合并，一个是引用流（旧数据），一个比较流（新数据）。每次都是行的最后版本通过进入下一步骤。行有以下标记：

“identical”:关键字在两个流中都存在，并且值相同

“changed”: 关键字在两个流中都存在，但是一个或者更多的值不同

“new”:引用流中没有找到关键字

“deleted”: 比较流中没有找到关键字

比较流中的数据进入下一步骤，除非在“删除“的情况。

存储合并（Stored Merge ）:这个步骤合并来自多个输入步骤的数据行，并且这些行用指定的关键字排序。

合并连接(Merge Join) :这个步骤将来自两个不同的步骤输入的数据执行一个高效的合并。合并选项包括INNER、LEFT OUTER、RIGHT OUTER、FULL OUTER。

备注：这个步骤将输入的行按指定的字段存储

Java Script 值（Java Script Value ）:这个步骤允许你用 JavaScript 语言做复杂的运算。使用的 JavaScript 引擎是 Rhino 1.5R5。

改进的 Java Script 值（Modified Java Script Value ）:这个步骤是“Javascript Values”的进改版本，它可以提供更好的效率，也更容

易使用。

执行 SQL 语句（Execute SQL script ）:在这个步骤中你可以执行 SQL 脚本，或者在转换初始化的时候执行，或者在步骤的每一个输入行执行。

维度更新/查询（Dimension lookup/update ）:

联合更新/查询（Combination lookup/update ）:这个步骤允许你在一个 junk-dimesion 表里存储信息。

映射（Mapping ）:如果你希望某个转换多次运行，你可以将重复的部分添加到一个映射中。映射是一个这样的转换：指定输入如何从映射输入中到达 ;指定输入字段如何转换：字段被添加或者删除

从结果获取记录（Get rows from result ）:这个步骤返回在一个任务中先前步骤生成的行。你可以进入选择先前步骤生成的元数据字段。

复制记录到结果（Copy rows to result ）:这个步骤允许你在一个任务中将行数据（内存中的）传递到下一个步骤

设置变量（Set Variable）:这个步骤允许你在一个任务中或者虚拟机中设置变量。它仅仅可以用一行数据来设置变量值。

获取变量（Get Variable ）:这个步骤允许你获取一个变量，它可以返回行或者附加值到输入行。

备注：你需要指定完整的变量格式${variable}或者%%variable%%。

从以前的结果获取文件（Get files from result ）:每次在转换、任务、文件细节、任务条目、步骤等处理、使用或者创建一个文件时，文件被捕获并且附加到结果中。你可以使用这个步骤访问那些信息。

复制文件名到结果（Set files in result）:在某种情况下，我们可以操纵输出结果中的文件列表。例如 mail 任务条目可以使用文件列表来关联邮件，可能你不需要发送所有的文件，你可以在此步骤中指定你想要发送的邮件。

记录注射器（Injector ）:注射器主要是针对以下人使用：想利用 Kettle API 和 JAVA 来注射记录到转换中。

套接字读入器（Socket Reader）:套接字读入器是通过 TCP/IP 协议将数据从一个服务器向另一个服务器传输。

套接字输写器（Socket Writer）:套接字输写器是通过 TCP/IP 协议将数据从一个服务器向另一个服务器传输。

聚合行（Aggregate Rows ）:这个步骤允许你在所有行的基础上快速的聚集行。

流 XML 输入（Streaming XML Input）:这个步骤主要提供值的解析，它信赖于 SAX 解析器，在大文件解析上能提供更好的性能。

它与 XML 输入非常相似，仅仅在内容和字段制表符上略有不同。

中止（Abort ）:这个步骤允许你在观察输入的时候中止步骤。它的主要用途是错误处理，在一定数量的行流过错误的连接时中止转换。

Oracle 批量装载（Oracle bulk loader ）:这个步骤允许你大批量加载数据到 Oracle 数据库，它将用一个正确的装载格式，然后调用 Oracle 的 SQL*Loader 数据加载工具加载到指定的表中。

## 官方文档组件清单

| Category       | Name                                   | Description                                                  |
| -------------- | -------------------------------------- | ------------------------------------------------------------ |
| Agile          | MonetDB Agile Mart                     |                                                              |
| Agile          | Table Agile Mart                       |                                                              |
| Big Data       | Avro input                             | Decode binary or JSON Avro data and extracts fields from the structure it defines, either from flat files or incoming fields. |
| Big Data       | Avro output                            | Serialize data into Avro binary or JSON format from the PDI data stream, then writes it to file. |
| Big Data       | Cassandra Input                        | Read from a Cassandra column family.                         |
| Big Data       | Cassandra Output                       | Write to a Cassandra column family.                          |
| Big Data       | CouchDB Input                          | Retrieve all documents from a given view in a given design document from a given database. |
| Big Data       | Hadoop File Input                      | Read data from a variety of different text-file types stored on a Hadoop cluster. |
| Big Data       | Hadoop File Output                     | Write data to a variety of different text-file types stored on a Hadoop cluster. |
| Big Data       | HBase Input                            | Read from an HBase column family.                            |
| Big Data       | HBase Output                           | Write to an HBase column family.                             |
| Big Data       | HBase Row Decoder                      | Decode an incoming key and HBase result object according to a mapping. |
| Big Data       | MapReduce Input                        | Enter Key Value pairs from Hadoop MapReduce.                 |
| Big Data       | MapReduce Output                       | Exit Key Value pairs, then push into Hadoop MapReduce.       |
| Big Data       | MongoDB Input                          | Read all entries from a MongoDB collection in the specified database. |
| Big Data       | MongoDB Output                         | Write to a MongoDB collection.                               |
| Big Data       | ORC Input                              | Read fields data from ORC files into a PDI data stream.      |
| Big Data       | ORC Output                             | Serialize data from the PDI data stream into an ORC file format and writes it to a file. |
| Big Data       | SSTable Output                         | Write to a filesystem directory as a Cassandra SSTable.      |
| Bulk loading   | ElasticSearch Bulk Insert              | Perform bulk inserts into ElasticSearch.                     |
| Bulk loading   | Infobright Loader                      | Load data to an Infobright database table.                   |
| Bulk loading   | Ingres VectorWise Bulk Loader          | Interface with the Ingres VectorWise Bulk Loader "COPY TABLE" command. |
| Bulk loading   | MonetDB Bulk Loader                    | Load data into MonetDB by using their bulk load command in streaming mode. |
| Bulk loading   | MySQL Bulk Loader                      | Load data over a named pipe (not available on MS Windows).   |
| Bulk loading   | Oracle Bulk Loader                     | Use Oracle Bulk Loader to load data.                         |
| Bulk loading   | PostgreSQL Bulk Loader                 | Bulk load PostgreSQL data.                                   |
| Bulk loading   | Teradata Fastload Bulk Loader          | Bulk load Teradata Fastload data.                            |
| Bulk loading   | Teradata TPT Insert Upsert Bulk Loader | Bulk load via TPT using the tbuild command.                  |
| Bulk loading   | Vertica Bulk Loader                    | Bulk load data into a Vertica table using their high performance COPY feature. |
| Bulk loading   | Greenplum Load                         | Bulk load Greenplum data.                                    |
| Data Mining    | ARFF output                            | Write data in ARFF format to a file.                         |
| Data Mining    | Knowledge Flow                         | Executes a Knowledge Flow data mining process.               |
| Data Warehouse | Combination lookup/update              | Update a junk dimension in a data warehouse. Alternatively, look up information in this dimension. The primary key of a junk dimension are all the fields. |
| Data Warehouse | Dimension lookup/update                | Update a slowly changing dimension in a data warehouse. Alternatively, look up information in this dimension. |
| Deprecated     | Avro input (deprecated)                | Replaced by Avro input.                                      |
| Deprecated     | Example step (deprecated)              | Is an example of a plugin test step.                         |
| Deprecated     | Greenplum Bulk Loader (deprecated)     | Bulk load Greenplum data. Replacement step is Greenplum Load. |
| Deprecated     | IBM Websphere MQ Consumer (deprecated) | Receive messages from any IBM Websphere MQ Server.           |
| Deprecated     | IBM Websphere MQ Producer (deprecated) | Send messages to any IBM Websphere MQ Server.                |
| Deprecated     | JMS consumer (deprecated)              | Replaced by JMS consumer.                                    |
| Deprecated     | JMS producer (deprecated)              | Replaced by JMS producer.                                    |
| Deprecated     | LucidDB streaming loader (deprecated)  | Load data into LucidDB by using Remote Rows UDX.             |
| Deprecated     | OpenERP object input (deprecated)      | Retrieve data from the OpenERP server using the XMLRPC interface with the 'read' function. |
| Deprecated     | OpenERP object output (deprecated)     | Update data on the OpenERP server using the XMLRPC interface and the 'import' function |
| Deprecated     | Palo cell input (deprecated)           | Retrieve all cell data from a Palo cube.                     |
| Deprecated     | Palo cell output (deprecated)          | Update cell data in a Palo cube.                             |
| Deprecated     | Palo dim input (deprecated)            | Return elements from a dimension in a Palo database.         |
| Deprecated     | Palo dim output (deprecated)           | Create/update dimension elements and element consolidations in a Palo database. |
| Deprecated     | SAP input (deprecated)                 | Read data from SAP ERP, optionally with parameters.          |
| Deprecated     | Text file input (deprecated)           | Replaced by Text file input.                                 |
| Deprecated     | Text file output (deprecated)          | Replaced by Text file output.                                |
| Deprecated     | OpenERP object delete (deprecated)     | Delete data from the OpenERP server using the XMLRPC interface with the 'unlink' function. |
| Experimental   | Script                                 | Calculate values by scripting in Ruby, Python, Groovy, Javascript, and other scripting languages. |
| Experimental   | SFTP Put                               | Upload a file or a stream file to a remote host via SFTP.    |
| Flow           | Abort                                  | Abort a transformation.                                      |
| Flow           | Append streams                         | Append two streams in an ordered way.                        |
| Flow           | Block this step until steps finish     | Block this step until selected steps finish.                 |
| Flow           | Blocking step                          | Block flow until all incoming rows have been processed. Subsequent steps only recieve the last input row to this step. |
| Flow           | Detect empty stream                    | Output one empty row if input stream is empty (ie when input stream does not contain any row). |
| Flow           | Dummy (do nothing)                     | Does not do anything. It is useful however when testing things or in certain situations where you want to split streams. |
| Flow           | ETL Metadata Injection                 | Inject metadata into an existing transformation prior to execution. This allows for the creation of dynamic and highly flexible data integration solutions. |
| Flow           | Filter Rows                            | Filter rows using simple equations.                          |
| Flow           | Identify last row in a stream          | Mark the last row.                                           |
| Flow           | Java Filter                            | Filter rows using java code.                                 |
| Flow           | Prioritize streams                     | Prioritize streams in an order way.                          |
| Flow           | Single Threader                        | Execute a sequence of steps in a single thread.              |
| Flow           | Switch / Case                          | Switch a row to a certain target step based on the case value in a field. |
| Flow           | Job Executor                           | Run a PDI job, and passes parameters and rows.               |
| Flow           | Transformation Executor                | Run a Pentaho Data Integration transformation, sets parameters, and passes rows. |
| Inline         | Injector                               | Inject rows into the transformation through the java API.    |
| Inline         | Socket reader                          | Read a socket. A socket client that connects to a server (Socket Writer step). |
| Inline         | Socket writer                          | Write a socket. A socket server that can send rows of data to a socket reader. |
| Input          | CSV file input                         | Read from a simple CSV file input.                           |
| Input          | Data Grid                              | Enter rows of static data in a grid, usually for testing, reference or demo purpose. |
| Input          | De-serialize from file                 | Read rows of data from a data cube.                          |
| Input          | Email messages input                   | Read POP3/IMAP server and retrieve messages.                 |
| Input          | ESRI Shapefile Reader                  | Read shape file data from an ESRI shape file and linked DBF file. |
| Input          | Fixed file input                       | Read from a fixed file input.                                |
| Input          | Generate random credit card numbers    | Generate random valide (luhn check) credit card numbers.     |
| Input          | Generate random value                  | Generate random value.                                       |
| Input          | Generate Rows                          | Generate a number of empty or equal rows.                    |
| Input          | Get data from XML                      | Get data from XML file by using XPath. This step also allows you to parse XML defined in a previous field. |
| Input          | Get File Names                         | Get file names from the operating system and send them to the next step. |
| Input          | Get Files Rows Count                   | Get files rows count.                                        |
| Input          | Get repository names                   | List detailed information about transformations and/or jobs in a repository. |
| Input          | Get SubFolder names                    | Read a parent folder and return all subfolders.              |
| Input          | Get System Info                        | Get information from the system like system date, arguments, etc. |
| Input          | Get table names                        | Get table names from database connection and send them to the next step. |
| Input          | Google Analytics                       | Fetch data from google analytics account.                    |
| Input          | GZIP CSV Input                         | Read in parallel from a GZIP CSV file.                       |
| Input          | JSON Input                             | Extract relevant portions out of JSON structures (file or incoming field) and output rows. |
| Input          | LDAP Input                             | Read data from LDAP host.                                    |
| Input          | LDIF Input                             | Read data from LDIF files.                                   |
| Input          | Load file content in memory            | Load file content in memory.                                 |
| Input          | Microsoft Access Input                 | Read data from a Microsoft Access file                       |
| Input          | Microsoft Excel Input                  | Read data from Excel and OpenOffice Workbooks (XLS, XLSX, ODS). |
| Input          | Mondrian Input                         | Execute and retrieve data using an MDX query against a Pentaho Analyses OLAP server (Mondrian). |
| Input          | OLAP Input                             | Execute and retrieve data using an MDX query against any XML/A OLAP datasource using olap4j. |
| Input          | Parquet Input                          | Decode Parquet data formats and extracts fields from the structure it defines. |
| Input          | Property Input                         | Read data (key, value) from properties files.                |
| Input          | RSS Input                              | Read RSS feeds.                                              |
| Input          | S3 CSV Input                           | Read from an S3 CSV file.                                    |
| Input          | Salesforce Input                       | Read information from SalesForce.                            |
| Input          | SAS Input                              | Reads file in sas7bdat (SAS) native format.                  |
| Input          | Table Input                            | Read information from a database table.                      |
| Input          | Text file input                        | Read data from a text file in several formats. This data can then be passed to your next step(s). |
| Input          | XBase input                            | Read records from an XBase type of database file (DBF).      |
| Input          | XML Input Stream (StAX)                | Process very large and complex XML files very fast.          |
| Input          | Yaml Input                             | Read YAML source (file or stream) parse them and convert them to rows and writes these to one or more output. |
| Input          | HL7 Input                              | Read data from HL7 data streams.                             |
| Job            | Copy rows to result                    | Write rows to the executing job. The information will then be passed to the next entry in this job. |
| Job            | Get files from result                  | Read filenames used or generated in a previous entry in a job. |
| Job            | Get rows from result                   | Read rows from a previous entry in a job.                    |
| Job            | Get Variables                          | Determine the values of certain (environment or Kettle) variables and put them in field values. |
| Job            | Set files in result                    | Set filenames in the result of this transformation. Subsequent job entries can then use this information. |
| Job            | Set Variables                          | Set environment variables based on a single input row.       |
| Joins          | Join Rows (cartesian product)          | Output the cartesian product of the input streams. The number of rows is the multiplication of the number of rows in the input streams. |
| Joins          | Merge Join                             | Join two streams on a given key and outputs a joined set. The input streams must be sorted on the join key. |
| Joins          | Merge Rows (diff)                      | Merge two streams of rows, sorted on a certain key. The two streams are compared and the equals, changed, deleted and new rows are flagged. |
| Joins          | Multiway Merge Join                    | Join multiple streams. This step supports INNER and FULL OUTER joins. |
| Joins          | Sorted Merge                           | Merge rows coming from multiple input steps providing these rows are sorted themselves on the given key fields. |
| Joins          | XML Join                               | Join a stream of XML-Tags into a target XML string.          |
| Lookup         | Call DB Procedure                      | Get back information by calling a database procedure.        |
| Lookup         | Check if a column exists               | Check if a column exists in a table on a specified connection. |
| Lookup         | Check if file is locked                | Check if a file is locked by another process.                |
| Lookup         | Check if webservice is available       | Check if a webservice is available.                          |
| Lookup         | Database join                          | Execute a database query using stream values as parameters.  |
| Lookup         | Database lookup                        | Look up values in a database using field values.             |
| Lookup         | Dynamic SQL row                        | Execute dynamic SQL statement build in a previous field.     |
| Lookup         | File exists                            | Check if a file exists.                                      |
| Lookup         | Fuzzy match                            | Find the approximate matches to a string using matching algorithms. Read a field from a main stream and output approximative value from lookup stream. |
| Lookup         | HTTP client                            | Call a web service over HTTP by supplying a base URL by allowing parameters to be set dynamically. |
| Lookup         | HTTP Post                              | Call a web service request over HTTP by supplying a base URL by allowing parameters to be set dynamically. |
| Lookup         | MaxMind GeoIP Lookup                   | Lookup an IPv4 address in a MaxMind database and add fields such as geography, ISP, or organization. |
| Lookup         | REST Client                            | Consume RESTful services. REpresentational State Transfer (REST) is a key design idiom that embraces a stateless client-server architecture in which the web services are viewed as resources and can be identified by their URLs |
| Lookup         | Stream lookup                          | Look up values coming from another stream in the transformation. |
| Lookup         | Table exists                           | Check if a table exists on a specified connection.           |
| Lookup         | Web services lookup                    | Look up information using web services (WSDL).               |
| Mapping        | Mapping (sub-transformation)           | Run a mapping (sub-transformation), use MappingInput and MappingOutput to specify the fields interface. |
| Mapping        | Mapping input specification            | Specify the input interface of a mapping.                    |
| Mapping        | Mapping output specification           | Specify the output interface of a mapping.                   |
| Mapping        | Simple Mapping                         | Turn a repetitive, re-usable part of a transformation (a sequence of steps) into a mapping (sub-transformation). |
| Output         | Automatic Documentation Output         | Generate documentation automatically based on input in the form of a list of transformations and jobs. |
| Output         | Delete                                 | Delete data in a database table based upon keys.             |
| Output         | Insert / Update                        | Update or insert rows in a database based upon keys.         |
| Output         | JSON output                            | Create JSON block and output it in a field to a file.        |
| Output         | LDAP Output                            | Perform Insert, upsert, update, add or delete operations on records based on their DN (Distinguished Name). |
| Output         | Microsoft Access Output                | Store records into an MS-Access database table.              |
| Output         | Microsoft Excel Output                 | Store records into an Excel (XLS) document with formatting information. |
| Output         | Microsoft Excel Writer                 | Write or appends data to an Excel file.                      |
| Output         | Parquet Output                         | Map fields within data files and choose where you want to process those files. |
| Output         | Pentaho Reporting Output               | Execute an existing report file (.prpt).                     |
| Output         | Properties Output                      | Write data to properties file.                               |
| Output         | RSS Output                             | Read RSS stream.                                             |
| Output         | S3 File Output                         | Export data to a text file on an Amazon Simple Storage Service (S3). |
| Output         | Salesforce Delete                      | Delete records in a Salesforce module.                       |
| Output         | Salesforce Insert                      | Insert records in a Salesforce module.                       |
| Output         | Salesforce Update                      | Update records in a Salesforce module.                       |
| Output         | Salesforce Upsert                      | Insert or update records in a Salesforce module.             |
| Output         | Serialize to file                      | Write rows of data to a data cube.                           |
| Output         | SQL File Output                        | Output SQL INSERT statements to a file.                      |
| Output         | Synchronize after merge                | Perform insert/update/delete in one go based on the value of a field. |
| Output         | Table Output                           | Write information to a database table.                       |
| Output         | Text file output                       | Write rows to a text file.                                   |
| Output         | Update                                 | Update data in a database table based upon keys.             |
| Output         | XML Output                             | Write data to an XML file.                                   |
| Pentaho Server | Set Session Variables                  | Set the value of session variable.                           |
| Pentaho Server | Call Endpoint                          | Call API endpoints from the Pentaho Server within a PDI transformation. |
| Pentaho Server | Get Session Variables                  | Retrieve the value of a session variable.                    |
| Scripting      | Execute Row SQL Script                 | Execute an SQL statement or file for every input row.        |
| Scripting      | Execute SQL script                     | Execute an SQL script, optionally parameterized using input rows. |
| Scripting      | Formula                                | Calculate a formula using Pentaho's libformula.              |
| Scripting      | Modified Java Script Value             | Run JavaScript programs (and much more).                     |
| Scripting      | Python Executor                        | Map upstream data from a PDI input step or execute a Python script to generate data. When you send all rows, Python stores the dataset in a variable that kicks off your Python script. |
| Scripting      | Regex Evaluation                       | Evaluate regular expressions. This step uses a regular expression to evaluate a field. It can also extract new fields out of an existing field with capturing groups. |
| Scripting      | Rule Executor                          | Execute a rule against each row (using Drools).              |
| Scripting      | Rule Accumulator                       | Execute a rule against a set of rows (using Drools).         |
| Scripting      | User Defined Java Class                | Program a step using Java code.                              |
| Scripting      | User Defined Java Expression           | Calculate the result of a Java Expression using Janino.      |
| Statistics     | Analytic query                         | Execute analytic queries over a sorted dataset (LEAD/LAG/FIRST/LAST). |
| Statistics     | Group by                               | Build aggregates in a group by fashion. This works only on a sorted input. If the input is not sorted, only double consecutive rows are handled correctly. |
| Statistics     | Memory Group by                        | Build aggregates in a group by fashion. This step doesn't require sorted input. |
| Statistics     | Output steps metrics                   | Return metrics for one or several steps.                     |
| Statistics     | R script executor                      | Execute an R script within a PDI transformation.             |
| Statistics     | Reservoir Sampling                     | Transform Samples a fixed number of rows from the incoming stream. |
| Statistics     | Sample rows                            | Filter rows based on the line number.                        |
| Statistics     | Univariate Statistics                  | Compute some simple stats based on a single input field.     |
| Streaming      | AMQP Consumer                          | Pull streaming data from an AMQP broker or clients through an AMQP transformation. |
| Streaming      | AMQP Producer                          | Publish messages in near-real-time to an AMQP broker.        |
| Streaming      | Get records from stream                | Return records that were previously generated by another transformation in a job. |
| Streaming      | JMS Consumer                           | Receive messages from a JMS server.                          |
| Streaming      | JMS Producer                           | Send messages to a JMS server.                               |
| Streaming      | Kafka Consumer                         | Run a sub-transformation that executes according to message batch size or duration, letting you process a continuous stream of records in near-real-time. |
| Streaming      | Kafka Producer                         | Publish messages in near-real-time across worker nodes where multiple, subscribed members have access. |
| Streaming      | MQTT Consumer                          | Pull streaming data from an MQTT broker or clients through an MQTT transformation. |
| Streaming      | MQTT Producer                          | Publish messages in near-real-time to an MQTT broker.        |
| Transform      | Add a checksum                         | Add a checksum column for each input row.                    |
| Transform      | Add constants                          | Add one or more constants to the input rows.                 |
| Transform      | Add sequence                           | Get the next value from an sequence.                         |
| Transform      | Add value fields changing sequence     | Add sequence depending of fields value change. Each time value of at least one field change, PDI will reset sequence. |
| Transform      | Add XML                                | Encode several fields into an XML fragment.                  |
| Transform      | Calculator                             | Create new fields by performing simple calculations.         |
| Transform      | Closure Generator                      | Generate a closure table using parent-child relationships.   |
| Transform      | Concat Fields                          | Concatenate multiple fields into one target field. The fields can be separated by a separator and the enclosure logic is completely compatible with the Text File Output step. |
| Transform      | Get ID from slave server               | Retrieve unique IDs in blocks from a slave server. The referenced sequence needs to be configured on the slave server in the XML configuration file. |
| Transform      | Number range                           | Create ranges based on numeric field.                        |
| Transform      | Replace in string                      | Replace all occurrences a word in a string with another word. |
| Transform      | Row Denormaliser                       | Denormalise rows by looking up key-value pairs and by assigning them to new fields in the output rows. This method aggregates and needs the input rows to be sorted on the grouping fields. |
| Transform      | Row Flattener                          | Flatten consecutive rows based on the order in which they appear in the input stream. |
| Transform      | Row Normaliser                         | Normalise de-normalised information.                         |
| Transform      | Select values                          | Select or remove fields in a row. Optionally, set the field meta-data: type, length and precision. |
| Transform      | Set Field Value                        | Replace value of a field with another value field.           |
| Transform      | Set Field Value to a Constant          | Replace value of a field to a constant.                      |
| Transform      | Sort rows                              | Sort rows based upon field values (ascending or descending). |
| Transform      | Split field to rows                    | Split a single string field by delimiter and creates a new row for each split term. |
| Transform      | Split Fields                           | Split a single field into more then one.                     |
| Transform      | Splunk Input                           | Read data from Splunk.                                       |
| Transform      | Splunk Output                          | Write data to Splunk.                                        |
| Transform      | String operations                      | Apply certain operations like trimming, padding and others to string value. |
| Transform      | Strings cut                            | Cut a portion of a substring.                                |
| Transform      | Unique rows                            | Remove double rows and leave only unique occurrences. This works only on a sorted input. If the input is not sorted, only double consecutive rows are handled correctly. |
| Transform      | Unique rows (HashSet)                  | Remove double rows and leave only unique occurrences by using a HashSet. |
| Transform      | Value Mapper                           | Map values of a certain field from one value to another.     |
| Transform      | XSL Transformation                     | Transform XML stream using XSL (eXtensible Stylesheet Language). |
| Utility        | Change file encoding                   | Change file encoding and create a new file.                  |
| Utility        | Clone row                              | Clone a row as many times as needed.                         |
| Utility        | Delay row                              | Output each input row after a delay.                         |
| Utility        | Edi to XML                             | Convert an Edifact message to XML to simplify data extraction (Available in PDI 4.4, already present in CI trunk builds). |
| Utility        | Execute a process                      | Execute a process and return the result.                     |
| Utility        | If field value is null                 | Set a field value to a constant if it is null.               |
| Utility        | Mail                                   | Send e-mail.                                                 |
| Utility        | Metadata structure of stream           | Read the metadata of the incoming stream.                    |
| Utility        | Null if...                             | Set a field value to null if it is equal to a constant value. |
| Utility        | Process files                          | Process one file per row (copy or move or delete). This step only accept filename in input. |
| Utility        | Run SSH commands                       | Run SSH commands and returns result.                         |
| Utility        | Send message to Syslog                 | Send message to Syslog server.                               |
| Utility        | Write to log                           | Write data to log.                                           |
| Utility        | Table Compare                          | Compare the data from two tables (provided they have the same lay-out). It'll find differences between the data in the two tables and log it. |
| Utility        | Zip File                               | Create a standard ZIP archive from the data stream fields.   |
| Validation     | Credit card validator                  | Determines: (1) if a credit card number is valid (uses LUHN10 (MOD-10) algorithm) (2) which credit card vendor handles that number (VISA, MasterCard, Diners Club, EnRoute, American Express (AMEX),...). |
| Validation     | Data Validator                         | Validates passing data based on a set of rules.              |
| Validation     | Mail Validator                         | Check if an email address is valid.                          |
| Validation     | XSD Validator                          | Validate XML source (files or streams) against XML Schema Definition. |



## 待解决问题

### merge join