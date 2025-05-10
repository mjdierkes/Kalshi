status

string

Only return collections of a certain status. Can be unopened, open, or closed

associated\_event\_ticker

string

Only return collections associated with a particular event ticker.

series\_ticker

string

Only return collections with a particular series ticker.

limit

int64

1 to 200

Specify the maximum number of results.

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

This optional parameter, when filled, should be filled with the cursor string returned in a previous request to

this end-point.

# `` 200

object

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records.

An empty value of this field indicates there is no next page.

multivariate\_contracts

array of objects

required

multivariate\_contracts\*

object

associated\_event\_tickers

array of strings

required

A list of events associated with the collection. Markets in these events can be

passed as inputs to the Lookup and Create endpoints.

associated\_event\_tickers\*

close\_date

date-time

required

The close date of the collection. After this time, the collection cannot be

interacted with.

collection\_ticker

string

required

Unique identifier for the collection.

description

string

required

Short description of the collection.

functional\_description

string

required

A functional description of the collection describing how inputs affect the output.

is\_all\_yes

boolean

required

Whether the collection requires that only the market side of 'yes' may be used.

is\_ordered

boolean

required

Whether the collection is ordered. If true, the order of markets passed into Lookup/Create

affects the output. If false, the order does not matter.

is\_single\_market\_per\_event

boolean

required

Whether the collection accepts multiple markets from the same event passed into Lookup/Create.

open\_date

date-time

required

The open date of the collection. Before this time, the collection cannot be

interacted with.

series\_ticker

string

required

Series associated with the collection. Events produced in the collection

will be associated with this series.

size\_max

int64

required

The maximum number of markets that must be passed into Lookup/Create (inclusive).

size\_min

int64

required

The minimum number of markets that must be passed into Lookup/Create (inclusive).

title

string

required

Title of the collection.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/multivariate_event_collections/ \

3     --header 'accept: application/json'

```

Choose an example:

application/json

`` 200

Updated 3 months ago

* * *

Did this page help you?

Yes

No