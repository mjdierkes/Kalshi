collection\_ticker

string

required

The collection to get the lookup history for.

lookback\_seconds

int64

required

# `` 200

object

lookup\_points

array of objects

lookup\_points

object

event\_ticker

string

required

last\_queried\_ts

date-time

required

market\_ticker

string

required

selected\_markets

array of objects

required

selected\_markets\*

object

event\_ticker

string

required

market\_ticker

string

required

side

string

required

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/multivariate_event_collections/collection_ticker/lookup \

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