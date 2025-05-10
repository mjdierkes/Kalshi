added

# [Websocket Upgrades](https://trading-api.readme.io/changelog/websocket-upgrades-20250506)

4 days agoby ReadMe API

new channels are added - `ticker_v2` and `market_lifecycle_v2` that are slightly different from their previous iterations and preparing

the older versions to be retired soon (~1-2 weeks) with a new version release

removed

# [Breaking Changes to Order Struct](https://trading-api.readme.io/changelog/breaking-order-struct)

8 days agoby ReadMe API

This is a **breaking change** to the Order struct that is returned several places in the API. The following fields are being deprecated:

added

# [Websocket Upgrades](https://trading-api.readme.io/changelog/websocket-upgrades)

about 1 month agoby ReadMe API

delta messages in `orderbook_delta` will now "updated\_ts" and, when the update is caused by your order, a "client\_order\_id" field be populated as well.

added

# [Adding GetUserDataTimestamp](https://trading-api.readme.io/changelog/add-api-user-clock)

about 2 months agoby ReadMe API

Adding GetUserDataTimestamp endpoint.

improved

# [Undo Certain 2.0.1 Changes](https://trading-api.readme.io/changelog/undo-version-201-changes)

2 months agoby ReadMe API

Due to the api log being new, some users were not able to prepare for the upcoming changes. We are releasing API version 2.0.2 on Friday March 7th 2025 to undo the changes in

improved

# [GetMilestone PageSize -> Limit](https://trading-api.readme.io/changelog/get-milestone-limit)

2 months agoby ReadMe API

Consistent with our API conventions, GetMilestone now returns `limit` instead of `page_size`

removed

# [Removed Fields From GetMarket(s)](https://trading-api.readme.io/changelog/removed-fields)

3 months agoby ReadMe API

GetMarket(s) will no longer return fields `Title`, `Subtitle`, `NoSubTitle`, `FeeWaiverExpirationTime`, `RiskLimitCents`

Orders will no longer contain `QueuePosition`

OrderConfirmations, returned on create endpoints, will no longer contain `SelfTradePreventionType`

added

# [GetApiVersion](https://trading-api.readme.io/changelog/version-endpoint)

3 months agoby ReadMe API

Added an endpoint that will give the current API version. This can be used to synchronize with changelog updates.

fixed

# [GetRFQ Cursor Response](https://trading-api.readme.io/changelog/rfq-cursor-response)

3 months agoby ReadMe API

In order to be consistent with pagination conventions, GetRFQs response will now be `cursor` instead of `next_cursor`

fixed

# [GetFills Millisecond Precision](https://trading-api.readme.io/changelog/millisecond-precision)

3 months agoby ReadMe API

GetFills `created_time` will now be returned in second precision to be consistent with websockets