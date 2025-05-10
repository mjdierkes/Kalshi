# `` 200

object

exchange\_active

boolean

required

False if the core Kalshi exchange is no longer taking any state changes at all. This includes but is not limited to trading, new users, and transfers. True unless we are under maintenance.

exchange\_estimated\_resume\_time

date-time

Date and time in the ISO 8601 spec. Example: 2022-11-30T15:00:00Z

trading\_active

boolean

required

True if we are currently permitting trading on the exchange. This is true during trading hours and false outside exchange hours. Kalshi reserves the right to pause at any time in case issues are detected.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/exchange/status

```

Choose an example:

application/json

`` 200

Updated 3 months ago

* * *

Did this page help you?

Yes

No