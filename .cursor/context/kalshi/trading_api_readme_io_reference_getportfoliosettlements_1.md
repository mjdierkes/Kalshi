limit

int64

1 to 1000

Parameter to specify the number of results per page. Defaults to 100.

min\_ts

int64

Restricts the response to settlements after a timestamp.

max\_ts

int64

Restricts the response to settlements before a timestamp.

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

So this optional parameter, when filled, should be filled with the cursor string returned in a previous request to this end-point.

Filling this would basically tell the api to get the next page containing the number of records passed on the limit parameter.

On the other side not filling it tells the api you want to get the first page for another query.

# `` 200

object

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records.

An empty value of this field indicates there is no next page.

settlements

array of objects

required

Settlement summaries for all markets the user participated in

settlements\*

object

market\_result

string

required

Settlement result for this market.

no\_count

int64

required

Number of no contracts owned on settlement.

no\_total\_cost

int64

required

Cost of the aggregate no position in this market on settlement in cents.

revenue

int64

required

Value earned in this settlement in cents.

settled\_time

date-time

required

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

ticker

string

required

Unique identifier for markets.

yes\_count

int64

required

Number of yes contracts owned on settlement.

yes\_total\_cost

int64

required

Cost of the aggregate yes position in this market on settlement in cents.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/settlements \

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