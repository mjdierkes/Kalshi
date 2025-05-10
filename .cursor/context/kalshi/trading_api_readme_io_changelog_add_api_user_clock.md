[Back to All](https://trading-api.readme.io/changelog)

added

Adding GetUserDataTimestamp endpoint.

There is typically a short delay before exchange events are reflected in the API endpoints. Whenever possible, combine API responses to PUT/POST/DELETE requests with websocket data to obtain the most accurate view of the exchange state. This endpoint provides an approximate indication of when the data from the following endpoints was last validated.

GetBalance, GetOrder(s), GetFills, GetPositions

#### API Version   [Skip link to API Version](https://trading-api.readme.io/changelog/add-api-user-clock\#api-version)

2.0.3