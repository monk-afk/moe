# møe

A Discord chatbot equipped with DialoGTP; a pre-trained language model tailored for casual conversation.

<img decoding="async" loading="lazy" alt="moe icon of a red and black checkered diamond" src="https://raw.githubusercontent.com/monk-afk/SquareOne/main/images/moe_bot/rgb_32b_floatpt/squareone_moe_icon_1280px.png" width="64"/>

### &nbsp;&nbsp;&nbsp;[![](https://dcbadge.limes.pink/api/server/pE4Tu3cf23)](https://discord.gg/pE4Tu3cf23)

This Readme needs more attention. I'll get to it eventually
___

- > Keyword Trigger
  - The bot responds to messages containing the keywords "moe" or "bot".
- > Channel Specific
  - It can be configured to respond only in designated channels.
- > AI Language Model
  - Utilizes the DialoGPT model from Microsoft to simulate chat.

___

## Required Software, Modules and Libraries

```bash
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
sudo su - postgres -c createuser $PGSQL_MAIN_USER -p $PGSQL_MAIN_PWD
sudo su - postgres -c createdb -O $PGSQL_MAIN_USER $PGSQL_MAIN_USER

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

pip install -U pip
pip install discord.py transformers py-dotenv torch psycopg2-binary
```
___

### Response Generation Parameters

- > inputs (required)
  - text (required)
    - The last input from the user in the conversation.
  - generated_responses
    - A list of strings corresponding to the earlier replies from the model.
  - past_user_inputs
    - A list of strings corresponding to the earlier replies from the user. Should be of the same length of generated_responses.
  - parameters
    - a dict containing the following keys:
    - min_length (Default: None).
      - Integer to define the minimum length in tokens of the output summary.
    - max_length (Default: None).
      - Integer to define the maximum length in tokens of the output summary.
    - top_k (Default: None).
      - An integer that limits the number of tokens considered when generating the next word. Example: top_k = 50: The model will only consider the 50 most probable next words.
    - top_p (Default: None).
      - Nucleus sampling dynamically adjusts the pool of candidate tokens based on the sum of the probabilities of the next tokens. Example: If top_p is 0.9, the model will consider the smallest set of tokens whose total probability adds up to 0.9 (90%).
    - temperature (Default: 1.0).
      - Float (0.0-100.0). adjusts the randomness of the model's predictions by scaling the probabilities of the next tokens. A high temperature makes all tokens more equally likely, while a low temperature makes the most likely tokens even more likely. Lower temperatures make the output more predictable and repetitive, while higher temperatures make it more varied and creative.
    - repetition_penalty (Default: None).
      - Float (0.0-100.0). The more a token is used within generation the more it is penalized to not be picked in successive generation passes.
    - max_time (Default: None).
      - Float (0-120.0). The amount of time in seconds that the query should take maximum. Network can cause some overhead so it will be a soft limit.
- options
  - a dict containing the following keys:
    - use_cache (Default: true). Boolean. There is a cache layer on the inference API to speedup requests we have already seen. Most models can use those results as is as models are deterministic (meaning the results will be the same anyway). However if you use a non deterministic model, you can set this parameter to prevent the caching mechanism from being used resulting in a real new query.
    - wait_for_model (Default: false) Boolean. If the model is not ready, wait for it instead of receiving 503. It limits the number of requests required to get your inference done. It is advised to only set this flag to true after receiving a 503 error as it will limit hanging in your application to known places.

___

## Changelog

0.0.1 - Initial Public Release

## To do
 - Add PostgreSQL support with separate channel contexts
 - Auto-delete channel data when bot is removed from a guild
 - Ignore direct messages
 - Bug: is_processing queues between servers/channels
 - Reply to replies to bot messages:
> ```py
>   referenced_message = await message.channel.fetch_message(message.reference.message_id)
>   if referenced_message.author == bot.user:
>       is_reply_to_bot = True
> ```
___

```py
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
```