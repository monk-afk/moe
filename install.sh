#!/bin/bash
# moe/install.sh
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
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
REQUIRED_MODULES="pip wheel py-dotenv discord.py transformers==4.51.3 cryptography"
echo "Installing modules: ${REQUIRED_MODULES}"
for MOD in ${REQUIRED_MODULES}; do
  python3 -m pip --no-cache-dir install -U "${MOD}"
done

# Need to do this one separately now
python3 -m pip --no-cache-dir install -U torch==2.7.0 --index-url https://download.pytorch.org/whl/cpu

#  Decryption key
if ! grep -q '^STORAGE_KEY=' "${DOTENV}"; then
  echo -e "\n# Storage Key\nSTORAGE_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> "${DOTENV}"
fi

deactivate

# Create bot launcher script
RUN_SCRIPT="${MOEDIR}/run_moe.sh"
if [ ! -f "${RUN_SCRIPT}" ]; then
  cat <<EOF > "${RUN_SCRIPT}"
#!/bin/bash
source "${PYVENV}/bin/activate"
python3 "${MOEDIR}/bot.py"
deactivate
EOF

  chmod 500 "${RUN_SCRIPT}"
  echo "Created Launcher: ${RUN_SCRIPT}"
else
  echo "Launcher already exists"
fi

echo "Environment Variables: ${DOTENV}"

unset DOTENV PYVENV MOEDIR REQUIRED_MODULES RUN_SCRIPT

echo "Done!"
