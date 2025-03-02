#!/bin/bash

# RUNNING THIS SCRIPT HAS NO GUARANTEE OF SUCCESS!

# Do carefully review each line and make adjustments needed for system compatibility

# Assuming the current directory is moe/

# Install and Setup PostgreSQL
sudo apt update
sudo apt install -y gnupg2

wget http://deb.debian.org/debian/pool/main/p/postgresql-common/postgresql-common_225+deb11u1.tar.xz
tar -xf postgresql-common_225+deb11u1.tar.xz
rm postgresql-common_225+deb11u1.tar.xz

sudo mkdir -p /usr/share/postgresql-common/pgdg
sudo mv ./postgresql-common/pgdg/apt.postgresql.org.sh /usr/share/postgresql-common/pgdg/

rm -r ./postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt install -y postgresql-15 postgresql-server-dev-15

sudo /etc/init.d/postgresql start
sudo /etc/init.d/postgresql status

# postgres is installed, do setup
echo "Set new password for Unix user postgres"
sudo passwd postgres

# Configure local socket connection
sudo su - postgres -c "sed -i -E 's/^(local\s+all\s+all\s+)peer/\1scram-sha-256/' /etc/postgresql/15/main/pg_hba.conf"

# Create random password for env
PGSQL_USER='moebot'
PGSQL_PASS=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 48)
PGSQL_MAIN_DB="$PGSQL_USER"_db
PGSQL_TEST_DB=test_"$PGSQL_MAIN_DB"

# Update pg_ident.conf
sudo su - postgres -c "echo 'local\t${USER}\t${PGSQL_USER}' >> /etc/postgresql/15/main/pg_ident.conf"

# Create .pgpass if not exist and append users
PGPASS_FILE="/home/${USER}/.pgpass"
touch ${PGPASS_FILE}
chmod 600 ${PGPASS_FILE}
chown ${USER}:${USER} ${PGPASS_FILE}

echo "localhost:5432:${PGSQL_MAIN_DB}:${PGSQL_USER}:${PGSQL_PASS}\
localhost:5432:${PGSQL_TEST_DB}:${PGSQL_USER}:${PGSQL_PASS}" >> ${PGPASS_FILE}

unset PGPASS_FILE

# Create a database for bot and test
sudo su - postgres -c "createuser ${PGSQL_USER}"
sudo su - postgres -c "psql -c \"ALTER USER ${PGSQL_USER} WITH PASSWORD '${PGSQL_PASS}';\""
sudo su - postgres -c "createdb -O ${PGSQL_USER} ${PGSQL_MAIN_DB}"
sudo su - postgres -c "createdb -O ${PGSQL_USER} ${PGSQL_TEST_DB}"

# Create the .env file
ENV_FILE='.env'
touch ${ENV_FILE}
chmod 600 ${ENV_FILE}

echo "# moe database\
PGSQL_DB=postgresql://${PGSQL_USER}@localhost/${PGSQL_MAIN_DB}\
# moe test database
# PGSQL_DB=postgresql://${PGSQL_USER}@localhost/${PGSQL_TEST_DB}\
# Add your Discord Auth Token
AUTH_TOKEN=\
# moe default command prefix
CMD_PREFIX=m1" >> ${ENV_FILE}
# Bot-specific Emoji variables should also be added

# Clear the environment variables now we're done with them
unset PGSQL_USER
unset PGSQL_PASS
unset PGSQL_MAIN_DB
unset PGSQL_TEST_DB
unset ENV_FILE

# Restart the daemon to apply changes
sudo /etc/init.d/postgresql restart
echo "PostgreSQL Setup Complete!"

# Install python, pip, and create virtual environment
echo "Installing python and pip"
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv pyvenv

echo "Installing modules"
source ./pyvenv/bin/activate
python3 -m pip --no-cache-dir install -U `cat docs/requirements.txt`



######################################################################################
##  MIT License                                                                     ##
##                                                                                  ##
##  Copyright © 2024-2025 monk (Discord ID: 699370563235479624)                     ##
##                                                                                  ##
##  Permission is hereby granted, free of charge, to any person obtaining a copy    ##
##  of this software and associated documentation files (the "Software"), to deal   ##
##  in the Software without restriction, including without limitation the rights    ##
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       ##
##  copies of the Software, and to permit persons to whom the Software is           ##
##  furnished to do so, subject to the following conditions:                        ##
##                                                                                  ##
##  The above copyright notice and this permission notice shall be included in all  ##
##  copies or substantial portions of the Software.                                 ##
##                                                                                  ##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      ##
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        ##
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     ##
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          ##
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   ##
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   ##
##  SOFTWARE.                                                                       ##
######################################################################################