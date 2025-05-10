milestone\_id

string

required

The ID of the milestone to get.

# `` 200

object

milestone

object

required

category

string

required

Category of the milestone

details

object

required

Has additional fields

end\_date

date-time

End date of the milestone, if any

id

string

required

Unique identifier for the milestone

notification\_message

string

required

Notification message for the milestone

related\_event\_tickers

array of strings

required

List of event tickers related to this milestone

related\_event\_tickers\*

source\_id

string

Source id of milestone if available

start\_date

date-time

required

Start date of the milestone

title

string

required

Title of the milestone

type

string

required

Type of the milestone

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/milestones/milestone_id \

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