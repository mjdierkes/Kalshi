Batch orders cancel input data.

ids

array of uuids

required

An array of order IDs to cancel.

ids\*
ADD uuid

# `` 200

object

orders

array of objects

required

An array of responses corresponding to the orders in the request.

orders\*

object

error

object

Generic structure for API error responses. object

order

object

Represents member orders in the API.

When an order is matched multiple trades can be created this can be tracked by looking into the trade.orderId field.

Order object

order\_id

uuid

Optional order\_id to identify the orders that errored.

reduced\_by

int32

required

ReducedBy is how much the count of the order was reduced by because of this operation.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request DELETE \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/orders/batched \

3     --header 'accept: application/json' \

4     --header 'content-type: application/json'

```

Choose an example:

application/json

`` 200

Updated 3 months ago

* * *

Did this page help you?

Yes

No