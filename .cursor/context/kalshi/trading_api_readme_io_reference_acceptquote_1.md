quote\_id

string

required

The quote being accepted.

accepted\_side

string

`` 204

No fields are returned on the response.

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

# `` 404      Generic structure for API error responses.

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

1curl --request PUT \

2     --url https://api.elections.kalshi.com/trade-api/v2/communications/quotes/quote_id/accept \

3     --header 'content-type: application/json'

```

Choose an example:

\*/\*

`` 500

Updated 3 months ago

* * *

Did this page help you?

Yes

No