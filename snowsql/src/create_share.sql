use role &act_role;
create or replace share &provider_share;
grant usage on database &provider_db to share &provider_share;
grant usage on schema &provider_db.&provider_schema to share &provider_share;
grant select on all tables in schema &provider_db.&provider_schema to share &provider_share;