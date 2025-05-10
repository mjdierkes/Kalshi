[Back to All](https://trading-api.readme.io/changelog)

added

delta messages in `orderbook_delta` will now "updated\_ts" and, when the update is caused by your order, a "client\_order\_id" field be populated as well.

`no_price` is being removed from `fills` channel as it can be calculated from 1 - `yes_price`.

#### API Version   [Skip link to API Version](https://trading-api.readme.io/changelog/websocket-upgrades\#api-version)

2.0.4