/updates and installs
/https://greggborodaty.com/upgrading-to-https-with-wordpress-amazon-ec2-lets-encrypt-and-cloudflare/
/sudo su -
sudo yum update -y
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y httpd2
sudo yum install -y mysql
sudo yum install php-xml
sudo yum install php-gd
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

/groups and permissions
sudo groupadd www
sudo usermod -a -G www ec2-user
sudo usermod -a -G www apache
sudo chown -R ec2-user /var/www
sudo chgrp -R www /var/www
sudo chmod 2775 /var/www
find /var/www -type d -exec sudo chmod 2775 {} +
find /var/www -type f -exec sudo chmod 0664 {} +

/env setup
export MYSQL_HOST=<your-endpoint>

/mysql setup
mysql --user=<user> --password=<password> <dbname>

CREATE USER 'wordpress' IDENTIFIED BY '<PASSWORD>';
GRANT ALL PRIVILEGES ON wordpress.* TO wordpress;
FLUSH PRIVILEGES;
Exit

/wordpress config
cd wordpress
cp wp-config-sample.php wp-config.php
sudo vim wp-config.php

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'database_name_here' );

/** MySQL database username */
define( 'DB_USER', 'username_here' );

/** MySQL database password */
define( 'DB_PASSWORD', 'password_here' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/Authentication Unique Keys and Salts.
/https://api.wordpress.org/secret-key/1.1/salt/

/deploy wordpress
cd /home/ec2-user
sudo cp -r wordpress/* /var/www/html/
sudo service httpd start
sudo systemctl enable httpd
sudo chown -R apache:apache /var/www/html

/sudo service httpd restart
