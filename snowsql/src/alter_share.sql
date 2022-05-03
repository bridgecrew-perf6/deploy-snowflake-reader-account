use role &act_role;

show managed accounts like '%&{consumer_account}%';

set reader_account_locator=(select "locator" from table(result_scan(last_query_id())) where "name" = upper('&consumer_account'));

alter share &provider_share add accounts = $reader_account_locator;

set locator = (select lower($reader_account_locator));

select $locator;