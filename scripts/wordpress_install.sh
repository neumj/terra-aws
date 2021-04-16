/updates and installs
/https://greggborodaty.com/upgrading-to-https-with-wordpress-amazon-ec2-lets-encrypt-and-cloudflare/
/https://awswithatiq.com/create-a-virtual-host-in-apache-2-4
/https://awswithatiq.com/how-to-setup-ssl-certificate-into-your-aws-ec2-instance-2020/

/sudo su -
sudo yum update -y
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y httpd
sudo yum install -y mysql
sudo yum install -y php-xml
sudo yum install -y php-gd
sudo yum install -y php72-mysqlnd 
sudo yum install -y php72-mbstring
sudo yum install -y php72-mcrypt
sudo yum install -y php72-zip
sudo yum install -y mod24_ssl
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

/groups and permissions
sudo groupadd www
sudo usermod -a -G www ec2-user
sudo usermod -a -G www apache

/env setup
export MYSQL_HOST=<DB-ENDPOINT>

/mysql setup
mysql --user=<USER> --password=<PASSWORD> <DBNAME>

CREATE USER <DB-USER> IDENTIFIED BY '<PASSWORD>';
GRANT ALL PRIVILEGES ON <DBNAME>.* TO <DB-USER>;
FLUSH PRIVILEGES;
Exit

/wordpress config
sudo chgrp -R www /home/ec2-user
sudo chmod 2775 /home/ec2-user
find /home/ec2-user -type d -exec sudo chmod 2775 {} +
find /home/ec2-user/wordpress -type f -exec sudo chmod 0664 {} +
cd wordpress
cp wp-config-sample.php wp-config.php
sudo vim wp-config.php

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', '<DBNAME>' );

/** MySQL database username */
define( 'DB_USER', '<USER>' );

/** MySQL database password */
define( 'DB_PASSWORD', '<PASSWORD>' );

/** MySQL hostname */
define( 'DB_HOST', '<DB-ENDPOINT>' );

/Authentication Unique Keys and Salts.
/https://api.wordpress.org/secret-key/1.1/salt/

/deploy wordpress
cd /home/ec2-user
sudo cp -r wordpress/* /var/www/html/
sudo chown -R apache /var/www
sudo chgrp -R www /var/www
sudo chmod 2775 /var/www
find /var/www -type d -exec sudo chmod 2775 {} +
find /var/www -type f -exec sudo chmod 0664 {} +
sudo service httpd start
sudo systemctl enable httpd

/sudo service httpd restart
