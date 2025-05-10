ticker

string

Restricts the response to orders in a single market.

event\_ticker

string

Restricts the response to orders in a single event.

min\_ts

int64

Restricts the response to orders after a timestamp, formatted as a Unix Timestamp.

max\_ts

int64

Restricts the response to orders before a timestamp, formatted as a Unix Timestamp.

status

string

Restricts the response to orders that have a certain status: resting, canceled, or executed.

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

So this optional parameter, when filled, should be filled with the cursor string returned in a previous request to this end-point.

Filling this would basically tell the api to get the next page containing the number of records passed on the limit parameter.

On the other side not filling it tells the api you want to get the first page for another query.

The cursor does not store any filters, so if any filter parameters like ticker, max\_ts or min\_ts were passed in the original query they must be passed again.

limit

int32

1 to 1000

Parameter to specify the number of results per page. Defaults to 100.

# `` 200

object

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records.

An empty value of this field indicates there is no next page.

orders

array of objects

required

orders\*

object

action

string

required

Representing trade action; currently supports buy and sell.

buy OrderActionBuy

sell OrderActionSell

OrderActionUnknown

`buy` `sell`

amend\_count

int32

The amendment delta throughout the lifecycle of the order (contract units).

amend\_taker\_fill\_count

int32

The size of filled taker orders (contract units) as a result of an amendment

client\_order\_id

string

required

close\_cancel\_count

int32

The size of resting orders canceled because of market close (contract units).

created\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

decrease\_count

int32

The reduction in the size of resting for orders (contract units).

expiration\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

fcc\_cancel\_count

int32

The size of resting contracts canceled because of exchange operations (contract units).

last\_update\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

maker\_fees

int64

Fees paid on filled maker contracts, in cents.

maker\_fill\_cost

int64

The cost of filled maker orders in cents.

maker\_fill\_count

int32

The size of filled maker orders (contract units).

no\_price

int64

required

Submitting price of the No side of the trade, in cents.

Exactly one of yes\_price and no\_price must be passed. If both prices are passed, return 400.

order\_id

string

required

Unique identifier for orders.

place\_count

int32

the size of placed maker orders (contract units).

queue\_position

int32

Position in the priority queue at a given price level

remaining\_count

int32

The size of the remaining resting orders (contract units).

side

string

required

Representing direction of the order; currently supports yes and no.

yes SIDE\_YES

no SIDE\_NO

SIDE\_UNSET

`yes` `no`

status

string

required

The current status of this order.

resting OrderStatusResting

canceled OrderStatusCanceled

executed OrderStatusExecuted

pending OrderStatusPending Will be used for order queue to represent orders that haven't been matched yet.

`resting` `canceled` `executed` `pending`

taker\_fees

int64

Fees paid on filled taker contracts, in cents.

taker\_fill\_cost

int64

The cost of filled taker orders in cents.

taker\_fill\_count

int32

The size of filled taker orders (contract units)

taker\_self\_trade\_cancel\_count

int32

The reduction in the size of a taker order due to self-trade prevention cancellation (contract units).

Will be zero for orders placed before the introduction of this field.

ticker

string

required

Unique identifier for markets.

type

string

required

Representing order type; currently supports "market" and "limit".

OrderTypeUnknown

market OrderTypeMarket

limit OrderTypeLimit

`market` `limit`

user\_id

string

yes\_price

int64

required

The yes price for this order in cents.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/orders \

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