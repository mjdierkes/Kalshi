Order create input data

action

string

required

Specifies if this is a buy or sell order.

buy\_max\_cost

int64

If type = market and action = buy, buy\_max\_cost represents the maximum cents that can be spent to acquire a position.

client\_order\_id

string

required

count

int32

required

Number of contracts to be bought or sold.

expiration\_ts

int64

Expiration time of the order, in unix seconds.

If this is not supplied, the order won't expire until explicitly cancelled.

This is also known as Good 'Till Cancelled (GTC).

If the time is in the past, the order will attempt to partially or completely fill

and the remaining unfilled quantity will be cancelled. This is also known as Immediate-or-Cancel (IOC).

If the time is in the future, the remaining unfilled quantity order will expire

at the specified time.

no\_price

int64

Submitting price of the No side of the trade, in cents.

Exactly one of yes\_price and no\_price must be passed. If both prices are passed, return 400.

post\_only

boolean

If this flag is set to true, an order will be rejected if it crosses the spread and executes.

truefalse

sell\_position\_floor

int32

SellPositionFloor will not let you flip position for a market order if set to 0.

side

string

required

Specifies if this is a 'yes' or 'no' order.

ticker

string

required

The ticker of the market the order will be placed in.

type

string

required

Specifies if this is a "market" or a "limit" order.

Note that either the Yes Price or the No Price must be provided for limit orders.

yes\_price

int64

Submitting price of the Yes side of the trade, in cents.

Exactly one of yes\_price and no\_price must be passed. If both prices are passed, return 400.

# `` 201

object

order

object

required

Represents the confirmation for an order that was just created.

action

string

required

Representing trade action; currently supports buy and sell.

buy OrderActionBuy

sell OrderActionSell

OrderActionUnknown

`buy` `sell`

client\_order\_id

string

required

created\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

expiration\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

no\_price

int64

required

The no price for this order in cents.

order\_id

string

required

Unique identifier for orders.

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

The current status of a given order.

resting OrderStatusResting

canceled OrderStatusCanceled

executed OrderStatusExecuted

pending OrderStatusPending Will be used for order queue to represent orders that haven't been matched yet.

`resting` `canceled` `executed` `pending`

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

1curl --request POST \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/orders \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Choose an example:

application/json

`` 201

Updated 3 months ago

* * *

Did this page help you?

Yes

No