ticker

string

required

Unique identifier for the market.

series\_ticker

string

required

Unique identifier for the series.

start\_ts

int64

required

Restricts the candlesticks to those covering time periods that end on or after this timestamp.

end\_ts

int64

required

Restricts the candlesticks to those covering time periods that end on or before this timestamp.

Must be within 5000 period\_intervals after start\_ts.

period\_interval

int32

required

Specifies the length of each candlestick period, in minutes. Must be one minute, one hour, or one day.

# `` 200

object

candlesticks

array of objects

required

Unique identifier for the market.

candlesticks\*

object

end\_period\_ts

int64

required

Unix timestamp for the inclusive end of the candlestick period.

open\_interest

int64

required

Number of contracts bought on the market by end of the candlestick period (end\_period\_ts).

price

object

required

price object

volume

int64

required

Number of contracts bought on the market during the candlestick period.

yes\_ask

object

required

yes\_ask object

yes\_bid

object

required

yes\_bid object

ticker

string

required

Unique identifier for the market.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/series/series_ticker/markets/ticker/candlesticks \

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