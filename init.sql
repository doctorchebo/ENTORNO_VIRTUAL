-- Allow root to connect from any host
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

-- Allow myuser to connect from any host
GRANT ALL PRIVILEGES ON *.* TO 'dms_user'@'%' WITH GRANT OPTION;

-- Apply the changes
FLUSH PRIVILEGES;
