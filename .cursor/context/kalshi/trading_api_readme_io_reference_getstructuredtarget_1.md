structured\_target\_id

string

required

The ID of the structured target to get.

# `` 200

object

structured\_target

object

required

details

object

required

Has additional fields

id

string

required

Unique identifier for the structured target

name

string

required

Name of the structured target

source\_id

string

Source id of structured target if available

type

string

required

Type of the structured target

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/structured_targets/structured_target_id \

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