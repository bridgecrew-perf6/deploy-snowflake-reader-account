use role &act_role;
create managed account &consumer_account 
admin_name='&consumer_user'
,admin_password='&consumer_pass'
,type=reader;
