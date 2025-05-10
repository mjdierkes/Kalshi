series\_ticker

string

required

Should be filled with the ticker of the series.

# `` 200

object

series

object

Represents a group of events that have the same underlying source.

For example: Fed interest rate hikes is a series with multiple events, one for each FOMC meeting.

category

string

required

Category specifies the category which this series belongs to.

contract\_url

string

required

ContractUrl provides a direct link to contract terms which govern the series.

frequency

string

required

Description of the frequency of the series. There is no fixed value set here, but will be something human-readable like: weekly, daily, one-off.

product\_metadata

object

required

Has additional fields

settlement\_sources

array of objects

required

SettlementSources specifies the official sources used for the determination of markets within the series. Methodology is defined in the rulebook.

settlement\_sources\*

object

name

string

The official name of the settlement source

url

string

The URL of the settlement source

tags

array of strings

required

Tags specifies the subjects that this series relates to, multiple series from different categories can have the same tags.

tags\*

ticker

string

required

Ticker that identifies this series.

title

string

required

Title describing the series. For full context use you should use this field with the title field of the events belonging to this series.

Updated 3 months ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/series/series_ticker \

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