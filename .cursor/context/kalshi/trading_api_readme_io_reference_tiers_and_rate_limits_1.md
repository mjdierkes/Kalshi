### Access tiers:   [Skip link to Access tiers:](https://trading-api.readme.io/reference/tiers-and-rate-limits-1\#access-tiers)

| Tier | Read | Write |
| --- | --- | --- |
| Basic | 10 per second | 5 per second |
| Advanced | 30 per second | 30 per second |
| Premier | 100 per second | 100 per second |
| Prime | 100 per second | 400 per second |

- Qualification for tiers
  - Basic: Completing signup
  - Advanced: Completing [https://forms.gle/iMhGvPZ1yU173jk2A](https://forms.gle/iMhGvPZ1yU173jk2A)
  - Premier: 3.75% of exchange traded volume in a given month
  - Prime: 7.5% of exchange traded volume in a given month
- In addition to the volume targets, technical competency is a requirement for Premier/Prime access. Before providing access to the Premier/Prime tiers, the Exchange will establish that the trader/trading entity has the following requirements met:
  - Knowledge of common security practices for API usage.
  - Proficiency in setting up monitoring for API usage, and ability to monitor API usage in near real-time.
  - Understanding and implementation of rate limiting and throttling mechanisms imposed by the API, and the ability to self-limit load.
  - Awareness of legal and compliance aspects related to API usage.
- Only the following APIs fall under the write limit, for the batch APIs, each item in the batch is considered 1 transaction with the sole exception of BatchCancelOrders, where each cancel counts as 0.2 transactions.
  - [BatchCreateOrders](https://trading-api.readme.io/reference/batchcreateorders)
  - [BatchCancelOrders](https://trading-api.readme.io/reference/batchcancelorders)
  - [CreateOrder](https://trading-api.readme.io/reference/createorder)
  - [CancelOrder](https://trading-api.readme.io/reference/cancelorder)
  - [AmendOrder](https://trading-api.readme.io/reference/amendorder)
  - [DecreaseOrder](https://trading-api.readme.io/reference/decreaseorder)
- We reserve the right to downgrade your API rate limit tier from Prime and Premier when you have shown lack of activity in the previous period

Updated 23 days ago

* * *

- [Best practices and references](https://trading-api.readme.io/reference/best-practices)

Did this page help you?

Yes

No

Updated 23 days ago

* * *

- [Best practices and references](https://trading-api.readme.io/reference/best-practices)

Did this page help you?

Yes

No