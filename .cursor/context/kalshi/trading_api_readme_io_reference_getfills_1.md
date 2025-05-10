ticker

string

Restricts the response to trades in a specific market.

order\_id

uuid

Restricts the response to trades related to a specific order.

min\_ts

int64

Restricts the response to trades after a timestamp.

max\_ts

int64

Restricts the response to trades before a timestamp.

limit

int32

1 to 1000

Parameter to specify the number of results per page. Defaults to 100.

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

So this optional parameter, when filled, should be filled with the cursor string returned in a previous request to this end-point.

Filling this would basically tell the api to get the next page containing the number of records passed on the limit parameter.

On the other side not filling it tells the api you want to get the first page for another query.

The cursor does not store any filters, so if any filter parameters like ticker, max\_ts or min\_ts were passed in the original query they must be passed again.

# `` 200

object

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records.

An empty value of this field indicates there is no next page.

fills

array of objects

required

fills\*

object

action

string

required

Specifies if this is a buy or sell order.

buy OrderActionBuy

sell OrderActionSell

OrderActionUnknown

`buy` `sell`

count

int32

required

Number of contracts to be bought or sold.

created\_time

date-time

required

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

is\_taker

boolean

required

If true then this fill was a taker.

no\_price

int64

required

Fill price for the no side in cents.

order\_id

uuid

required

Unique identifier for orders.

side

string

required

Specifies if this is a 'yes' or 'no' fill.

yes SIDE\_YES

no SIDE\_NO

SIDE\_UNSET

`yes` `no`

ticker

string

required

Unique identifier for markets.

trade\_id

uuid

required

Unique identifier for fills.

yes\_price

int64

required

Fill price for the yes side in cents.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/fills \

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