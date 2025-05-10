ticker

string

required

Market ticker.

depth

int32

Depth specifies the maximum number of orderbook price levels you want to see for either side.

Only the highest (most relevant) price level are kept.

# `` 200

object

orderbook

object

required

Contains the number of pending resting order for each price on a specific market.

no

array of arrays of int32s

required

no\*

array of int32s

yes

array of arrays of int32s

required

yes\*

array of int32s

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/markets/ticker/orderbook \

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