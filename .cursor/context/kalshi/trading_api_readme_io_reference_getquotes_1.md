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

quote\_creator\_user\_id

string

rfq\_creator\_user\_id

string

rfq\_id

string

# `` 200

object

cursor

string

quotes

array of objects

quotes

object

accepted\_side

string

accepted\_ts

date-time

cancellation\_reason

string

cancelled\_ts

date-time

confirmed\_ts

date-time

contracts

int64

created\_ts

date-time

creator\_id

string

creator\_order\_id

uuid

creator\_user\_id

string

executed\_ts

date-time

id

string

market\_ticker

string

no\_bid

int64

rest\_remainder

boolean

Private Fields - included only when creator is the quoter

rfq\_creator\_id

string

rfq\_creator\_order\_id

uuid

Private Fields - included only when creator is the RFQ creator

rfq\_creator\_user\_id

string

rfq\_id

string

status

string

updated\_ts

date-time

yes\_bid

int64

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

2     --url https://api.elections.kalshi.com/trade-api/v2/communications/quotes \

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