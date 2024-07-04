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
# untested
apt-get install gnupg2
wget http://deb.debian.org/debian/pool/main/p/postgresql-common/postgresql-common_225+deb11u1.tar.xz
tar -xf postgresql-common_225\+deb11u1.tar.xz
rm postgresql-common_225\+deb11u1.tar.xz
mkdir -p /usr/share/postgresql-common/pgdg
mv ./postgresql-common/pgdg/apt.postgresql.org.sh /usr/share/postgresql-common/pgdg/
rm -r ./postgresql-common
/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
apt-get install postgresql-15 postgresql-server-dev-15
sed -i -E "s/^shared_buffers = .+/shared_buffers = 2048MB/" /etc/postgresql/15/main/postgresql.conf
sed -i -E "s/^(local\s+all\s+all\s+)peer/\1scram-sha-256/" /etc/postgresql/15/main/pg_hba.conf
read -s -p "Set password for Unix user postgres: " pg_unix_pwd
echo
echo "$pg_unix_pwd" | su -c 'passwd postgres' postgres
read -s -p "Enter New PostgreSQL DB User: " pg_usr
echo
read -s -p "Enter New PostgreSQL Password: " pgusr_pwd
echo
echo "local		${USER}		$pg_usr" >> /etc/postgresql/15/main/pg_ident.conf
pgdb_pwd=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 48)
touch /home/${USER}/.pgpass
chmod 600 /home/${USER}/.pgpass
chown ${USER}:${USER} /home/${USER}/.pgpass
echo "localhost:5432:bot_db:$pg_usr:$pgusr_pwd
localhost:5432:test_db:$pg_usr:$pgusr_pwd" > /home/${USER}/.pgpass
su - postgres -c "psql -c \"CREATE USER $pg_usr WITH PASSWORD '$pgusr_pwd';\""
su - postgres -c "psql -c \"CREATE DATABASE bot_db OWNER $pg_usr;\""
su - postgres -c "psql -c \"CREATE DATABASE test_db OWNER $pg_usr;\""
su - postgres -c "/etc/init.d/postgresql restart"
echo "PostgreSQL Setup Complete!"
echo "Installing python and pip modules"
apt install python3 python3-pip
python3 -m venv ~/moebot/pvenv
source /home/${USER}/moebot/pvenv/bin/activate
pip -U install pip3
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
      - Integer to define the top tokens considered within the sample operation to create new text. Limits the sampling pool to the top k logits, adding more diversity to the responses.
    - top_p (Default: None).
      - Float to define the tokens that are within the sample operation of text generation. Add tokens in the sample for more probable to least probable until the sum of the probabilities is greater than top_p. Uses nucleus sampling to choose from the smallest possible set of logits whose cumulative probability is at least p.
    - temperature (Default: 1.0).
      - Float (0.0-100.0). The temperature of the sampling operation. 1 means regular sampling, 0 means always take the highest score, 100.0 is getting closer to uniform probability. Controls the randomness of predictions by scaling the logits before applying softmax. Lower values make the model more confident and deterministic, while higher values increase randomness.
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

0.0.2 - Added PostgreSQL support with separate channel contexts
0.0.1 - Initial Public Release

## To do

 -[ ] Auto-delete channel data when bot is removed from a guild
 -[ ] Reply to replies to bot messages:
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