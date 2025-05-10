Batch order create input data.

orders

array of objects

required

An array of individual orders to place.

orders\*
ADD object

# `` 201

object

orders

array of objects

required

An array of responses corresponding to orders in the request.

orders\*

object

client\_order\_id

string

error

object

Generic structure for API error responses. object

order

object

Represents the confirmation for an order that was just created.

OrderConfirmation object

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request POST \

2     --url https://api.elections.kalshi.com/trade-api/v2/portfolio/orders/batched \

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