limit

int64

1 to 200

Parameter to specify the number of results per page. Defaults to 100.

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

So this optional parameter, when filled, should be filled with the cursor string returned in a previous request to this end-point.

Filling this would basically tell the api to get the next page containing the number of records passed on the limit parameter.

On the other side not filling it tells the api you want to get the first page for another query.

The cursor does not store any filters, so if any filter parameters like series\_ticker was passed in the original query they must be passed again.

status

string

Restricts the events to those with certain statuses, as a comma separated list.

The following values are accepted: unopened, open, closed, settled.

series\_ticker

string

Series ticker to retrieve contracts for.

with\_nested\_markets

boolean

If the markets belonging to the events should be added in the response as a nested field in this event.

truefalse

# `` 200

object

cursor

string

The Cursor represents a pointer to the next page of records in the pagination.

Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records.

An empty value of this field indicates there is no next page.

events

array of objects

required

events\*

object

category

string

required

Deprecated: Event category. Use the series level property instead.

collateral\_return\_type

string

required

event\_ticker

string

required

Unique identifier for events.

markets

array of objects

The markets that are linked to this event. Will be filled only if the query parameter "with\_nested\_markets" is equal "true".

markets

object

can\_close\_early

boolean

required

If true then this market can close earlier then the time provided on close\_time.

cap\_strike

number

category

string

required

Deprecated: Category for this market.

close\_time

date-time

required

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

custom\_strike

object

Expiration value for each target that leads to a YES settlement.

Filled only if "strike\_type" is "custom" or "structured".

Has additional fields

event\_ticker

string

required

Unique identifier for events.

expected\_expiration\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

expiration\_time

date-time

required

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

expiration\_value

string

required

The value that was considered for the settlement.

fee\_waiver\_expiration\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

floor\_strike

number

functional\_strike

string

Mapping from expiration values to settlement values of the YES/LONG side, in centi-cents.

Filled only if "market\_type" is "scalar" and "strike\_type" is "functional".

Ex. f(x) = max(0, min(10000, 500 \* x))

A scalar market with this functional strike and an expiration value of 10 would have a settlement value on the YES/LONG side of 5000 centi cents.

last\_price

int64

required

Price for the last traded yes contract on this market.

latest\_expiration\_time

date-time

required

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

liquidity

int64

required

Value for current offers in this market in cents.

market\_type

string

required

Identifies the type of market, which affects its payout and structure.

binary: Every binary market has two sides, YES and NO. If the market's "payout criterion" is satisfied, it pays out the notional value to holders of YES. Otherwise, it pays out the notional value to holders of NO.

scalar: Every scalar market has two sides, LONG and SHORT (although these might be referred to as YES/NO in some API endpoints). At settlement, each contract's notional value is split between LONG and SHORT as described in the market rules.

no\_ask

int64

required

Price for the lowest NO sell offer on this market.

no\_bid

int64

required

Price for the highest NO buy offer on this market.

no\_sub\_title

string

required

Shortened title for the no side of this market.

notional\_value

int64

required

The total value of a single contract at settlement.

open\_interest

int64

required

Number of contracts bought on this market disconsidering netting.

open\_time

date-time

required

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

previous\_price

int64

required

Price for the last traded yes contract on this market a day ago.

previous\_yes\_ask

int64

required

Price for the lowest YES sell offer on this market a day ago.

previous\_yes\_bid

int64

required

Price for the highest YES buy offer on this market a day ago.

response\_price\_units

string

required

The units used to express all price related fields in this response, including: prices, bids/asks, liquidity, notional and settlement values.

usd\_cent MONEY\_UNIT\_USD\_CENT

usd\_centi\_cent MONEY\_UNIT\_USD\_CENTI\_CENT

`usd_cent` `usd_centi_cent`

result

string

required

Settlement result for this market. Filled only after determination. Omitted for scalar markets.

MARKET\_RESULT\_NO\_RESULT

yes MARKET\_RESULT\_YES

no MARKET\_RESULT\_NO

void MARKET\_RESULT\_VOID

scalar MARKET\_RESULT\_SCALAR

all\_no RANGED\_MARKET\_RESULT\_ALL\_NO

all\_yes RANGED\_MARKET\_RESULT\_ALL\_YES

`yes` `no` `void` `scalar` `all_no` `all_yes`

risk\_limit\_cents

int64

required

Deprecated: Risk limit for this market in cents.

rules\_primary

string

required

A plain language description of the most important market terms.

rules\_secondary

string

required

A plain language description of secondary market terms.

settlement\_timer\_seconds

int32

required

The amount of time after determination that the market settles (pays out).

settlement\_value

int64

The settlement value of the YES/LONG side of the contract. Only filled after determination.

status

string

required

Represents the current status of a market.

strike\_type

string

Strike type defines how the market strike (expiration value) is defined and evaluated.

greater: It will be a single number. For YES outcome the expiration value should be greater than "floor\_strike".

greater\_or\_equal: It will be a single number. For YES outcome the expiration value should be greater OR EQUAL than "floor\_strike".

less: It will be a single number. For YES outcome the expiration value should be less than "cap\_strike".

less\_or\_equal: It will be a single number. For YES outcome the expiration value should be less OR EQUAL than "cap\_strike".

between: It will be two numbers. For YES outcome the expiration value should be between inclusive "floor\_strike" and "cap\_strike", that means expiration value needs to be greater or equal "floor\_strike" and less or equal "cap\_strike".

functional: For scalar markets only. A mapping from expiration values to settlement values of the YES/LONG side will be in "functional\_strike".

custom: It will be one or more non-numerical values. For YES outcome the expiration values should be equal to the values in "custom\_strike".

structured: A key value map from relationship -> structured target IDs. Metadata for these structured targets can be fetched via the /structured\_targets endpoints.

unknown MarketStrikeTypeUnknown

greater MarketStrikeTypeGreater

less MarketStrikeTypeLess

greater\_or\_equal MarketStrikeTypeGreaterOrEqual

less\_or\_equal MarketStrikeTypeLessOrEqual

between MarketStrikeTypeBetween

functional MarketStrikeTypeFunctional

custom MarketStrikeTypeCustom

structured MarketStrikeTypeStructured

`unknown` `greater` `less` `greater_or_equal` `less_or_equal` `between` `functional` `custom` `structured`

subtitle

string

required

Deprecated: Shortened title for this market. Use "yes\_sub\_title" or "no\_sub\_title" instead.

tick\_size

int64

required

The minimum price movement in the market. All limit order prices must be in denominations of the tick size.

ticker

string

required

Unique identifier for markets.

title

string

required

Full title describing this market.

volume

int64

required

Number of contracts bought on this market.

volume\_24h

int64

required

Number of contracts bought on this market in the past day.

yes\_ask

int64

required

Price for the lowest YES sell offer on this market.

yes\_bid

int64

required

Price for the highest YES buy offer on this market.

yes\_sub\_title

string

required

Shortened title for the yes side of this market.

mutually\_exclusive

boolean

required

If true then the event is mutually exclusive.

series\_ticker

string

required

Unique identifier for series.

strike\_date

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

strike\_period

string

The strike period for this event. This will be filled when the event strike is not a date.

If it is a date then the 'strike\_date' field should be filled instead.

sub\_title

string

required

Shortened title.

title

string

required

Event title.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/events \

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