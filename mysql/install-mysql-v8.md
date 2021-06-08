Install MySQL (v8.0+) in Ubuntu:

```bash
# Download and update the latest MySQL apt repository configuration file:
curl -OL https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb
sudo dpkg –i mysql-apt-config_0.8.13-1_all.deb

# Refresh the apt repository and install MySql:
sudo apt-get update
sudo apt-get install mysql-server

# Setup basic security features:
sudo mysql_secure_installation
```

To verify MySQL is running:

```bash
sudo service mysql status
```

To stop the MySQL service:

```bash
sudo service mysql stop
```

To start the MySQL service:

```bash
sudo service mysql start
```

Run MySQL as root:

```bash
sudo mysql –u root –p
```

Create a new user account and grant privileges:

```sql
CREATE USER '<username>'@'localhost' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON * . * TO '<username>'@'localhost';
FLUSH PRIVILEGES;
```
