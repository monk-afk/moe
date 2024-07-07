# NOT ENTIRELY FUNCTIONAL
# This is supposed to be an automated install script

# Install and Setup PostgreSQL
sudo apt install gnupg2
wget http://deb.debian.org/debian/pool/main/p/postgresql-common/postgresql-common_225+deb11u1.tar.xz
tar -xf postgresql-common_225\+deb11u1.tar.xz
rm postgresql-common_225\+deb11u1.tar.xz
sudo mkdir -p /usr/share/postgresql-common/pgdg
sudo mv ./postgresql-common/pgdg/apt.postgresql.org.sh /usr/share/postgresql-common/pgdg/
rm -r ./postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt install postgresql-15 postgresql-server-dev-15

# postgres is installed, do setup
echo "Set new password for Unix user postgres"
sudo passwd postgres
PGSQL_MAIN_USER='moebot'
PGSQL_MAIN_PWD=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 48)
PGSQL_MAIN_DB='moebot_db'
PGSQL_TEST_USER=test_"$PGSQL_MAIN_USER"
PGSQL_TEST_PWD=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 48)
PGSQL_TEST_DB=test_"$PGSQL_MAIN_DB"

# Set configs
sudo su - postgres -c 'sed -i -E "s/^shared_buffers = .+/shared_buffers = 2048MB/" /etc/postgresql/15/main/postgresql.conf'
sudo su - postgres -c 'sed -i -E "s/^(local\s+all\s+all\s+)peer/\1scram-sha-256/" /etc/postgresql/15/main/pg_hba.conf'

# These variables are missing, needs fixing
sudo su - postgres -c 'echo "local		${USER}		$PGSQL_MAIN_USER" >> /etc/postgresql/15/main/pg_ident.conf'
sudo su - postgres -c 'echo "local		${USER}		$PGSQL_TEST_USER" >> /etc/postgresql/15/main/pg_ident.conf'

# Create .pgpass if not exist and append users
touch /home/${USER}/.pgpass
chmod 600 /home/${USER}/.pgpass
chown ${USER}:${USER} /home/${USER}/.pgpass
echo "localhost:5432:$PGSQL_MAIN_DB:$PGSQL_MAIN_USER:$PGSQL_MAIN_PWD" >> /home/${USER}/.pgpass
echo "localhost:5432:$PGSQL_TEST_DB:$PGSQL_TEST_USER:$PGSQL_TEST_PWD" >> /home/${USER}/.pgpass

# Create a database for bot and test
sudo su - postgres -c createuser $PGSQL_MAIN_USER -p $PGSQL_MAIN_PWD
sudo su - postgres -c createdb -O $PGSQL_MAIN_USER $PGSQL_MAIN_USER
sudo su - postgres -c createuser $PGSQL_TEST_USER -p $PGSQL_TEST_PWD
sudo su - postgres -c createdb -O $PGSQL_TEST_USER $PGSQL_TEST_USER

# May as well create the .env file while we're at it
echo "# PGSQL_DB=postgresql://$PGSQL_MAIN_USER@localhost/$PGSQL_MAIN_DB" >> /home/${USER}/moe/.env
echo "PGSQL_DB=postgresql://$PGSQL_TEST_USER@localhost/$PGSQL_TEST_DB" >> /home/${USER}/moe/.env

# Clear the environment variables now we're done with them
PGSQL_TEST_USER=
PGSQL_MAIN_USER=
PGSQL_MAIN_PWD=
PGSQL_TEST_PWD=
POSTGRES_UNIX_PWD=

# restart the daemon to apply changes
sudo /etc/init.d/postgresql restart
echo "PostgreSQL Setup Complete!"

# install and update python, pip, and create virtual environment
echo "Installing python and pip modules"
sudo apt install python3 python3-venv python3-pip

python3 -m venv /home/${USER}/moe/pvenv
source /home/${USER}/moe/pvenv/bin/activate

pip3 install -U pip

for MODULE in `cat requirements.txt`
  do pip3 --no-cache-dir install -U $MODULE
done



####################################################################################
# MIT License                                                                      #
#                                                                                  #
# Copyright (c) 2024 monk                                                          #
#                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy     #
# of this software and associated documentation files (the "Software"), to deal    #
# in the Software without restriction, including without limitation the rights     #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
# copies of the Software, and to permit persons to whom the Software is            #
# furnished to do so, subject to the following conditions:                         #
#                                                                                  #
# The above copyright notice and this permission notice shall be included in all   #
# copies or substantial portions of the Software.                                  #
#                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE    #
# SOFTWARE.                                                                        #
####################################################################################