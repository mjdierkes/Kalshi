```
<?xml version="1.0" encoding="UTF-8"?><rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
    <channel>
        <title><![CDATA[Kalshi Developer Suite]]></title>
        <description><![CDATA[Kalshi Exchange Trading APIs]]></description>
        <link>https://trading-api.readme.io/</link>
        <generator>RSS for Node</generator>
        <lastBuildDate>Sat, 10 May 2025 20:30:41 GMT</lastBuildDate>
        <atom:link href="https://trading-api.readme.io/changelog.rss" rel="self" type="application/rss+xml"/>
        <item>
            <title><![CDATA[Websocket Upgrades]]></title>
            <description><![CDATA[new channels are added - ticker_v2 and market_lifecycle_v2 that are slightly different from their previous iterations and preparing the older versions to be retired soon (~1-2 weeks) with a new version release API Version 2.0.4 (note that 2.0.5 has been announced but this is simply being added to th...]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/websocket-upgrades-20250506</link>
            <guid isPermaLink="false">d9bb9396-47ce-30cc-8f12-a1fd00dd1454</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Tue, 06 May 2025 21:36:10 GMT</pubDate>
            <type>added</type>
        </item>
        <item>
            <title><![CDATA[Breaking Changes to Order Struct]]></title>
            <description><![CDATA[This is a breaking change to the Order struct that is returned several places in the API. The following fields are being deprecated: taker_fill_count , place_count , amend_count , amend_taker_fill_count , decrease_count , maker_fill_count , fcc_cancel_count , close_cancel_count , taker_self_trade_ca...]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/breaking-order-struct</link>
            <guid isPermaLink="false">16426a68-2c5a-3bfe-9adf-9544c4689e4a</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Fri, 02 May 2025 19:09:45 GMT</pubDate>
            <type>removed</type>
        </item>
        <item>
            <title><![CDATA[Websocket Upgrades]]></title>
            <description><![CDATA[delta messages in orderbook_delta will now "updated_ts" and, when the update is caused by your order, a "client_order_id" field be populated as well. no_price is being removed from fills channel as it can be calculated from 1 - yes_price . API Version 2.0.4]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/websocket-upgrades</link>
            <guid isPermaLink="false">9808445c-da76-3f29-9c9f-5722c0b4041e</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Tue, 01 Apr 2025 21:09:18 GMT</pubDate>
            <type>added</type>
        </item>
        <item>
            <title><![CDATA[Adding GetUserDataTimestamp]]></title>
            <description><![CDATA[Adding GetUserDataTimestamp endpoint. There is typically a short delay before exchange events are reflected in the API endpoints. Whenever possible, combine API responses to PUT/POST/DELETE requests with websocket data to obtain the most accurate view of the exchange state. This endpoint provides an...]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/add-api-user-clock</link>
            <guid isPermaLink="false">3b369a1c-9b3b-3be9-8941-0adfe40326e1</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Tue, 18 Mar 2025 20:43:30 GMT</pubDate>
            <type>added</type>
        </item>
        <item>
            <title><![CDATA[Undo Certain 2.0.1 Changes]]></title>
            <description><![CDATA[Due to the api log being new, some users were not able to prepare for the upcoming changes. We are releasing API version 2.0.2 on Friday March 7th 2025 to undo the changes in api field removals All removed fields will be re-added. ws fills precision granularity . GetFills will continue to returning ...]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/undo-version-201-changes</link>
            <guid isPermaLink="false">0815855c-5c13-37aa-9c57-7786a7d97b4e</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Thu, 06 Mar 2025 18:32:10 GMT</pubDate>
            <type>improved</type>
        </item>
        <item>
            <title><![CDATA[GetMilestone PageSize -> Limit]]></title>
            <description><![CDATA[Consistent with our API conventions, GetMilestone now returns limit instead of page_size API Version 2.0.1]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/get-milestone-limit</link>
            <guid isPermaLink="false">219dbea9-746c-3e8f-b841-36ac4786806a</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Sun, 02 Mar 2025 17:58:24 GMT</pubDate>
            <type>improved</type>
        </item>
        <item>
            <title><![CDATA[Removed Fields From GetMarket(s)]]></title>
            <description><![CDATA[GetMarket(s) will no longer return fields Title , Subtitle , NoSubTitle , FeeWaiverExpirationTime , RiskLimitCents Orders will no longer contain QueuePosition OrderConfirmations, returned on create endpoints, will no longer contain SelfTradePreventionType API Version 2.0.1]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/removed-fields</link>
            <guid isPermaLink="false">2300c4fd-e41d-3932-90da-bd7e8dc2292f</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Fri, 21 Feb 2025 16:14:39 GMT</pubDate>
            <type>removed</type>
        </item>
        <item>
            <title><![CDATA[GetApiVersion]]></title>
            <description><![CDATA[Added an endpoint that will give the current API version. This can be used to synchronize with changelog updates. API Version 2.0.1]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/version-endpoint</link>
            <guid isPermaLink="false">3360e99e-647a-35bd-8501-3e5afec07a41</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Wed, 19 Feb 2025 18:24:44 GMT</pubDate>
            <type>added</type>
        </item>
        <item>
            <title><![CDATA[GetRFQ Cursor Response]]></title>
            <description><![CDATA[In order to be consistent with pagination conventions, GetRFQs response will now be cursor instead of next_cursor API Version 2.0.1]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/rfq-cursor-response</link>
            <guid isPermaLink="false">e51931c1-742a-3f7e-91ee-a65eb46748fd</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Tue, 18 Feb 2025 20:32:07 GMT</pubDate>
            <type>fixed</type>
        </item>
        <item>
            <title><![CDATA[GetFills Millisecond Precision]]></title>
            <description><![CDATA[GetFills created_time will now be returned in second precision to be consistent with websockets API Version 2.0.1]]></description>
            <link>https://trading-api.readme.io/v2.0.4/changelog/millisecond-precision</link>
            <guid isPermaLink="false">7d0c24a2-94cf-32e4-980e-ae36f31bf29e</guid>
            <dc:creator><![CDATA[ReadMe API]]></dc:creator>
            <pubDate>Tue, 18 Feb 2025 20:31:38 GMT</pubDate>
            <type>fixed</type>
        </item>
    </channel>
</rss>
```