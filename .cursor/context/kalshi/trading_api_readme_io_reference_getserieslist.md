category

string

Should be filled with the category of the series to filter on.

Required: yes

include\_product\_metadata

boolean

Indicate if you want to include product metadata in response.

truefalse

# `` 200

object

series

array of objects

Data for the series.

Required: yes

series

object

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

Updated about 1 month ago

* * *

Did this page help you?

Yes

No

ShellNodeRubyPHPPython

```

xxxxxxxxxx

1curl --request GET \

2     --url https://api.elections.kalshi.com/trade-api/v2/series/ \

3     --header 'accept: application/json'

```

Choose an example:

application/json

`` 200

Updated about 1 month ago

* * *

Did this page help you?

Yes

No