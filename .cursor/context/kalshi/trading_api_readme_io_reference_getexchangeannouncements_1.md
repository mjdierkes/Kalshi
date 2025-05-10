# `` 200

object

announcements

array of objects

required

A list of exchange-wide announcements.

announcements\*

object

delivery\_time

date-time

required

The time the announcement was delivered.

message

string

required

The message contained within the announcement.

status

string

required

The current status of this announcement.

info AnnouncementTypeInfo

warning AnnouncementTypeWarning

error AnnouncementTypeError

AnnouncementTypeUnknown

`info` `warning` `error`

type

string

required

The type of the announcement.

info AnnouncementTypeInfo

warning AnnouncementTypeWarning

error AnnouncementTypeError

AnnouncementTypeUnknown

`info` `warning` `error`

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/exchange/announcements

```

Choose an example:

application/json

`` 200

Updated 3 months ago

* * *

Did this page help you?

Yes

No