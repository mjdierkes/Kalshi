cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

So this optional parameter, when filled, should be filled with the cursor string returned in a previous request to this end-point.

Filling this would basically tell the api to get the next page containing the number of records passed on the limit parameter.

On the other side not filling it tells the api you want to get the first page for another query.

The cursor does not store any filters, so if any filter parameters like settlement\_status, ticker, or event\_ticker were passed in the original query they must be passed again.

limit

int32

1 to 1000

Parameter to specify the number of results per page. Defaults to 100.

count\_filter

string

Restricts the positions to those with any of following fields with non-zero values, as a comma separated list.

The following values are accepted: position, total\_traded, resting\_order\_count

settlement\_status

string

Settlement status of the markets to return. Defaults to unsettled.

all SettlementStatusAll

settled SettlementStatusSettled

unsettled SettlementStatusUnsettled

allsettledunsettled

ticker

string

Ticker of desired positions.

event\_ticker

string

Event ticker of desired positions.

# `` 200

object

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records.

An empty value of this field indicates there is no next page.

event\_positions

array of objects

required

List of event positions.

event\_positions\*

object

event\_exposure

int64

required

Cost of the aggregate event position in cents.

event\_ticker

string

required

Unique identifier for events.

fees\_paid

int64

required

Fees paid on fill orders, in cents.

realized\_pnl

int64

required

Locked in profit and loss, in cents.

resting\_order\_count

int32

required

Aggregate size of resting orders in contract units.

total\_cost

int64

required

Total spent on this event in cents.

market\_positions

array of objects

required

List of market positions.

market\_positions\*

object

fees\_paid

int64

required

Fees paid on fill orders, in cents.

last\_updated\_ts

date-time

required

last time the position is updated.

market\_exposure

int64

required

Cost of the aggregate market position in cents.

position

int32

required

Number of contracts bought in this market. Negative means NO contracts and positive means YES contracts.

realized\_pnl

int64

required

Locked in profit and loss, in cents.

resting\_orders\_count

int32

required

Aggregate size of resting orders in contract units.

ticker

string

required

Unique identifier for the market.

total\_traded

int64

required

Total spent on this market in cents.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/positions \

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