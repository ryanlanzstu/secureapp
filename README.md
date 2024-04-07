In app.py amend MySQL config to your devices needs:
# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'
app.config['MYSQL_PORT'] = 3307

Create a MySQL DB called 'flask_users'.
Create 2 tables called 'tbl_users' and 'tbl_xss'. Pictures of tables in Project Report.

In 'tbl_users' add 'id-int(11)' as the Private Key and add Auto Incrementing, 'username-varchar(20)' and 'password-varchar(20)'
In 'tbl_xss' add 'xss_id-int(11)' as the Private Key and add Auto Incrementing, 'username-varchar(20), 'xss_text-text', and 'time-timestamp'.

