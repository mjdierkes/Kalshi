# `` 200

object

schedule

object

required

maintenance\_windows

array of objects

required

Scheduled maintenance windows, during which the exchange may be unavailable.

maintenance\_windows\*

object

end\_datetime

date-time

start\_datetime

date-time

standard\_hours

array of objects

required

The standard operating hours of the exchange. All times are expressed in ET.

Outside of these times trading will be unavailable.

standard\_hours\*

object

end\_time

date-time

friday

array of objects

friday

object

close\_time

string

open\_time

string

monday

array of objects

monday

object

close\_time

string

open\_time

string

saturday

array of objects

saturday

object

close\_time

string

open\_time

string

start\_time

date-time

sunday

array of objects

sunday

object

close\_time

string

open\_time

string

thursday

array of objects

thursday

object

close\_time

string

open\_time

string

tuesday

array of objects

tuesday

object

close\_time

string

open\_time

string

wednesday

array of objects

wednesday

object

close\_time

string

open\_time

string

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/exchange/schedule

```

Choose an example:

application/json

`` 200

Updated 3 months ago

* * *

Did this page help you?

Yes

No