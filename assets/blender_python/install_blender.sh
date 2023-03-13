#!/usr/bin/env bash

# USAGE
#   1. In terminal, cd into directory with `install_blender.sh`, for example:
#       cd ~/Downloads
#   2. Optionally modify any default variables, most importantly BLENDER_URL
#       export BLENDER_URL=https://mirror.clarkson.edu/blender/release/Blender3.3/blender-3.3.1-linux-x64.tar.xz
#       export BLENDER_INSTALL=$HOME/bin/blender/
#       export DESKTOP_INSTALL_PATH=$HOME/.local/share/applications
#   3. Run the script
#       ./install_blender.sh

# ------------------------------------------------------------------------------
# Config
# ------------------------------------------------------------------------------

# If the following variables were not already set use the following defaults:

# URL of the Blender archive to download (must be .tar.xz)
: "${BLENDER_URL:=https://mirror.clarkson.edu/blender/release/Blender3.3/blender-3.3.1-linux-x64.tar.xz}"

# Where to extract the archive to
# this path does not have to exist yet
: "${BLENDER_INSTALL:=$HOME/bin/blender/}"

# Where to install the .desktop file
: "${DESKTOP_INSTALL_PATH:=$HOME/.local/share/applications}"

# ------------------------------------------------------------------------------
# No need to edit anything below this point
# ------------------------------------------------------------------------------

add_trailing_slash() {
    str=$1
    length=${#str}
    last_char=${str:length-1:1}
    [[ $last_char != "/" ]] && str="$str/"
    echo "$str"
}

remove_trailing_slash() {
    str=$1
    length=${#str}
    last_char=${str:length-1:1}

    [[ $last_char == "/" ]] && str=${str:0:length-1}
    echo "$str"
}

BLENDER_INSTALL=$(add_trailing_slash "$BLENDER_INSTALL")
DESKTOP_INSTALL_PATH=$(remove_trailing_slash "$DESKTOP_INSTALL_PATH")

# Ensure BLENDER_URL has a filename in the format of "blender-3.3.1-linux-x64.tar.xz"
ARCHIVE_FILENAME="${BLENDER_URL##*/}"
if ! echo "$ARCHIVE_FILENAME" | grep -qE "^blender-[0-9]+\.[0-9]+\.[0-9]+-.*\.tar.xz$"; then
    echo "Invalid archive filename.  Please check BLENDER_URL" 1>&2
    return
fi

mkdir -p "$BLENDER_INSTALL"
cd "$BLENDER_INSTALL" || return

BLENDER_ARCHIVE=$(basename "$BLENDER_URL")
BLENDER_DIR=${BLENDER_ARCHIVE::-7}

# Find Blender version
BLENDER_VERSION=$(echo "$BLENDER_DIR" | awk 'BEGIN {  FPAT = "(-|\\.)([0-9]+)" } ; {
    major = substr($1, 2)
    minor = $2
    print major minor
}')

# Download and extract the archive
curl -o "$BLENDER_ARCHIVE" "$BLENDER_URL" || return
tar -xf "$BLENDER_ARCHIVE" || return

BLENDER_FOLDER=$BLENDER_INSTALL$BLENDER_DIR

# Find the Python version
cd "$BLENDER_FOLDER/$BLENDER_VERSION/python/bin" || return
for i in python*; do
    BPY_EXECUTABLE="$i"
    break
done

BPY=$BLENDER_FOLDER/$BLENDER_VERSION/python/bin/$BPY_EXECUTABLE
cd "$BLENDER_FOLDER" || return

# Modify the .desktop file to include the full Blender path
awk '{sub(/Exec=blender %f/,"Exec='"${BLENDER_FOLDER}"'/blender %f"); print}' blender.desktop >blender.desktop.tmp
rm blender.desktop # Just overwriting the .desktop file didn't work well so workaround that
mv blender.desktop.tmp blender.desktop

# Install the .desktop file
desktop-file-install --dir="$DESKTOP_INSTALL_PATH" blender.desktop && echo "Successfully installed blender.desktop to $DESKTOP_INSTALL_PATH" && update-desktop-database "$DESKTOP_INSTALL_PATH"

# Make sure pip is installed
"$BPY" -m ensurepip

# Write BPY to .bashrc
if ! grep -q "export BPY=\"$BPY\"" ~/.bashrc; then
    echo "export BPY=\"$BPY\"" >>~/.bashrc
fi

# Write BLENDER_PATH to .bashrc
if ! grep -q "export BLENDER_PATH=\"$BLENDER_FOLDER\"" ~/.bashrc; then
    echo "export BLENDER_PATH=\"$BLENDER_FOLDER\"" >>~/.bashrc
fi

# Write BLENDER_VERSION to .bashrc
if ! grep -q "export BLENDER_VERSION=\"$BLENDER_VERSION\"" ~/.bashrc; then
    echo "export BLENDER_VERSION=\"$BLENDER_VERSION\"" >>~/.bashrc
fi
