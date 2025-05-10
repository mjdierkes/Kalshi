[Back to All](https://trading-api.readme.io/changelog)

removed

This is a **breaking change** to the Order struct that is returned several places in the API. The following fields are being deprecated:

`taker_fill_count`, `place_count`, `amend_count`, `amend_taker_fill_count`, `decrease_count`, `maker_fill_count`, `fcc_cancel_count`, `close_cancel_count`, `taker_self_trade_cancel_count`, `maker_self_trade_cancel_count`.

Instead, the following three fields will be populated:

- `remaining_count` already exists
- `initial_count` represents the quantity the order was originally submitted with.
- `fill_count` represents the quantity that has been filled.

Users can still determine how much of their fill count was maker or taker by using the GetFills endpoint.

#### API Version   [Skip link to API Version](https://trading-api.readme.io/changelog/breaking-order-struct\#api-version)

2.0.5