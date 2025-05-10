cursor

string

limit

int32

market\_ticker

string

event\_ticker

string

status

string

creator\_user\_id

string

# `` 200

object

cursor

string

rfqs

array of objects

rfqs

object

cancellation\_reason

string

cancelled\_ts

date-time

contracts

int64

created\_ts

date-time

creator\_id

string

creator\_user\_id

string

id

string

market\_ticker

string

rest\_remainder

boolean

Private Fields - included only when creator is the requester

status

string

updated\_ts

date-time

# `` 400      Generic structure for API error responses.

object

code

string

details

string

message

string

# `` 403      Generic structure for API error responses.

object

code

string

details

string

message

string

# `` 500      Generic structure for API error responses.

object

code

string

details

string

message

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

2     --url https://api.elections.kalshi.com/trade-api/v2/communications/rfqs \

3     --header 'accept: application/json'

```

Choose an example:

application/json

`` 200

\*/\*

`` 500

Updated 3 months ago

* * *

Did this page help you?

Yes

No