#!/bin/bash
# THIS SCRIPT STILL NEEDS TESTING AND FIXING
# Likely doesn't work, but the steps are there.

MOEDIR="/home/${USER}/moe"

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

cd "$(dirname "$0")"
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
sudo su - postgres -c "sed -i -E 's/^shared_buffers = .+/shared_buffers = 2048MB/' /etc/postgresql/15/main/postgresql.conf"
sudo su - postgres -c "sed -i -E 's/^(local\s+all\s+all\s+)peer/\1scram-sha-256/' /etc/postgresql/15/main/pg_hba.conf"

# Update pg_ident.conf
sudo su - postgres -c "echo 'local\t${USER}\t${PGSQL_MAIN_USER}' >> /etc/postgresql/15/main/pg_ident.conf"
sudo su - postgres -c "echo 'local\t${USER}\t${PGSQL_TEST_USER}' >> /etc/postgresql/15/main/pg_ident.conf"

# Create .pgpass if not exist and append users
PGPASS_FILE="/home/${USER}/.pgpass"
touch ${PGPASS_FILE}
chmod 600 ${PGPASS_FILE}
chown ${USER}:${USER} ${PGPASS_FILE}
echo "localhost:5432:${PGSQL_MAIN_DB}:${PGSQL_MAIN_USER}:${PGSQL_MAIN_PWD}" >> ${PGPASS_FILE}
echo "localhost:5432:${PGSQL_TEST_DB}:${PGSQL_TEST_USER}:${PGSQL_TEST_PWD}" >> ${PGPASS_FILE}

# Create a database for bot and test
sudo su - postgres -c "createuser ${PGSQL_MAIN_USER}"
sudo su - postgres -c "psql -c \"ALTER USER ${PGSQL_MAIN_USER} WITH PASSWORD '${PGSQL_MAIN_PWD}';\""
sudo su - postgres -c "createdb -O ${PGSQL_MAIN_USER} ${PGSQL_MAIN_DB}"
sudo su - postgres -c "createuser ${PGSQL_TEST_USER}"
sudo su - postgres -c "psql -c \"ALTER USER ${PGSQL_TEST_USER} WITH PASSWORD '${PGSQL_TEST_PWD}';\""
sudo su - postgres -c "createdb -O ${PGSQL_TEST_USER} ${PGSQL_TEST_DB}"

# May as well create the .env file while we're at it
ENV_FILE="$MOEDIR/.env"
echo "# PGSQL_DB=postgresql://${PGSQL_MAIN_USER}@localhost/${PGSQL_MAIN_DB}" >> ${ENV_FILE}
echo "PGSQL_DB=postgresql://${PGSQL_TEST_USER}@localhost/${PGSQL_TEST_DB}" >> ${ENV_FILE}

# Clear the environment variables now we're done with them
unset PGSQL_TEST_USER
unset PGSQL_MAIN_USER
unset PGSQL_MAIN_PWD
unset PGSQL_TEST_PWD

# Restart the daemon to apply changes
sudo /etc/init.d/postgresql restart
echo "PostgreSQL Setup Complete!"

# Install and update python, pip, and create virtual environment
echo "Installing python and pip modules"
sudo apt install -y python3 python3-venv python3-pip

python3 -m venv ../pvenv
source ../pvenv/bin/activate
pip3 install -U pip

# Install minimum version 2.5.0 from discord.py repository
# Reaction emoji support requires v2.5.0 or greater
cd ${MOEDIR}/pyven/lib/python3.11/site-packages/
git clone https://github.com/Rapptz/discord.py
cd discord.py
python3 -m pip install -U .

for MODULE in $(cat requirements.txt); do
  pip3 --no-cache-dir install $MODULE
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