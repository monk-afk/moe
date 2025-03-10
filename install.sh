#!/bin/bash
set -e
MOEDIR=$(cd "$(dirname "${0}")" &> /dev/null && pwd)

# Create the .env file if it doesn't exist
DOTENV="${MOEDIR}/.env"
if [ ! -f "${DOTENV}" ]; then
  echo "Creating .env file in ${DOTENV}"
  touch "${DOTENV}"
  chmod 600 "${DOTENV}"

  echo "# moe's variables" >> "${DOTENV}"
  echo "CMD_PREFIX=m1" >> "${DOTENV}"

  read -s -p "Enter Discord Auth Token: " TOKEN
  echo -e "\n# Discord Auth Token\nAUTH_TOKEN=${TOKEN}" >> "${DOTENV}"
  unset TOKEN

  while true; do
    echo
    read -p "Enable Emoji Reactions? (y/n): " yn
    case "$yn" in
      [Yy]* ) cat <<EOF >> "${DOTENV}"
# Reaction Emojis
UPVOTE_EMOJI=
DOWNVOTE_EMOJI=
NOYOU_EMOJI=
MOE_EMOJI=
THINK_EMOJI=
WOW_EMOJI=
EOF
              break ;;
      [Nn]* ) mv "${MOEDIR}/cogs/react.py" "${MOEDIR}/cogs/react_py"
              echo "Disabled react.py!"
              break ;;
      * ) echo "Please type 'y' or 'n'." ;;
    esac
  done
fi

read -p "Should we update Apt sources? (y/n): " yn
case "$yn" in
  [Yy]* ) sudo apt update ;;
  [Nn]* ) echo "Skipped apt update." ;;
  * ) echo "No input, continuing without apt update." ;;
esac

# Install Python components if missing
for package in python3 python3-venv python3-pip; do
  if ! command -v "${package}" &> /dev/null; then
    sudo apt install -y "${package}"
  fi
done

# Create virtual environment
PYVENV="${MOEDIR}/pyven"
echo "Creating Python virtual environment in ${PYVENV}"
if [ ! -d "${PYVENV}" ]; then
  python3 -m venv "${PYVENV}"
fi
source "${PYVENV}/bin/activate"

# Install one at a time; sometimes batch install will cause OOM on low-resource systems
REQUIRED_MODULES="pip wheel py-dotenv discord.py transformers torch"
echo "Installing modules: ${REQUIRED_MODULES}"
for MOD in ${REQUIRED_MODULES}; do
  python3 -m pip --no-cache-dir install -U "${MOD}"
done
deactivate

# Create bot launcher script
RUN_SCRIPT="${MOEDIR}/run_moe.sh"
cat <<EOF > "${RUN_SCRIPT}"
#!/bin/bash
source "${PYVENV}/bin/activate"
python3 "${MOEDIR}/bot.py"
deactivate
EOF
chmod 500 "${RUN_SCRIPT}"

echo "Done!
Bot Launcher: ${RUN_SCRIPT}
Environment Variables: ${DOTENV}
"
unset DOTENV PYVENV MOEDIR REQUIRED_MODULES RUN_SCRIPT

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
