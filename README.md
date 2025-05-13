# CeneoWebScraper

## Struktura opiini w serwisie Ceneo.pl
|składowa|zmienna|sektor|
|--------|-------|------|
|opinia|opinion|div.js_product-review:not(.user-post--highlight)|
|identyfikator opinii||opinion_id|["data-entry-id"]|
|autor|author|span.user-post__author-name|
|rekomendacje|recommendation|span.user-post__author-recomendation > em|
|liczba gwiazdek|stars|span.user-post__score-count|
|treść opinii|content|div.user-post__text|
|lista zalet|pros|div.review-feeature__item--positive|
|lista wad|cons|div.review-feeature__item--negative|
|ile osób uznało opinię za przydatną|useful|button.vote-yes["data-total-vote"]|
|ile osób uznało opinię za nieprzydatną|useless|button.vote-no["data-total-vote"]|
|data wystawienia opinii|post_date|span.user-post__published > time:nth-child(1)["datetime"]|
|data zakupu prodkutu|purchase_date|span.user-post__published > time:nth-child(2)["datetime"]|