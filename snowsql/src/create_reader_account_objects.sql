use role &act_role;
create or replace database &consumer_db from share &provider_account.&provider_share;
grant imported privileges on database &consumer_db to role &pub_role;

use role &sys_role;
create or replace warehouse query_wh
warehouse_size = xsmall
warehouse_type = standard
auto_suspend = 60
auto_resume = true
initially_suspended = true;

grant usage on warehouse query_wh to role &pub_role;