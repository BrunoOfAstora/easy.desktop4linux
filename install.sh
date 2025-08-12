#!/usr/bin/bash

set -e

if [ "$1" == un ]; then
    echo "Uninstalling..."

    sed -i 's|export PATH="$HOME/.local/bin/desktop:$PATH"||g' "$HOME/.bashrc"
    rm -rf ~/.local/bin/dsktp

    echo "Done."
    exit 1
fi

mkdir -p ~/.local/bin/dsktp
if grep "desktop" "$HOME/.local/bin/desktop/desktop" > /dev/null 2>&1; then
  echo "'desktop' is already installed"
  exit 1
fi

cp src/desktop ~/.local/bin/dsktp

cp src/run.py ~/.local/bin/dsktp

chmod +x ~/.local/bin/dsktp/desktop

if [ -f "$HOME/.bashrc" ]; then
    if grep 'export PATH="$HOME/.local/bin/dsktp/desktop:$PATH"' "$HOME/.bashrc" > /dev/null 2>&1; then
      echo "'Desktop' is already configured in your system"
      exit 1;
    fi

    echo 'export PATH="$HOME/.local/bin/dsktp:$PATH"' >> ~/.bashrc
    source ~/.bashrc

elif [ -f "$HOME/.zshrc" ]; then
   if grep 'export PATH="$HOME/.local/bin/dsktp/desktop:$PATH"' "$HOME/.zshrc" > /dev/null 2>&1; then
      echo "'Desktop' is already configured in your system"
      exit 1;
    fi

    echo 'export PATH="$HOME/.local/bin/dsktp:$PATH"' >> ~/.zshrc
    source ~/.zshrc

else
  echo "Unknown configuration file."
  exit 1
fi

echo "Done"

