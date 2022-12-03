#!/usr/bin/env bash

# Set the following variables to their correct values:
BLENDER_URL=https://mirror.clarkson.edu/blender/release/Blender3.3/blender-3.3.1-linux-x64.tar.xz
BLENDER_INSTALL=$HOME/bin/blender/

mkdir -p "$BLENDER_INSTALL"
cd "$BLENDER_INSTALL" || return

BLENDER_ARCHIVE=$(basename "$BLENDER_URL")
BLENDER_DIR=${BLENDER_ARCHIVE::-7}

BLENDER_VERSION=$(echo "$BLENDER_DIR" | awk 'BEGIN {  FPAT = "(-|\\.)([0-9]+)" } ; {
    major = substr($1, 2)
    minor = $2
    print major minor
}')

curl -o "$BLENDER_ARCHIVE" "$BLENDER_URL"
tar -xf "$BLENDER_ARCHIVE"

BLENDER_FOLDER=$BLENDER_INSTALL$BLENDER_DIR

cd "$BLENDER_FOLDER/$BLENDER_VERSION/python/bin" || return
for i in python*; do
    BPY_EXECUTABLE="$i"
    break
done
BPY=$BLENDER_FOLDER/$BLENDER_VERSION/python/bin/$BPY_EXECUTABLE

cd "$BLENDER_FOLDER" || return

awk '{sub(/Exec=blender %f/,"Exec='"${BLENDER_FOLDER}"'/blender %f"); print}' blender.desktop >blender.desktop.tmp
rm blender.desktop
mv blender.desktop.tmp blender.desktop

desktop-file-install --dir="$HOME"/.local/share/applications blender.desktop
update-desktop-database ~/.local/share/applications
#   for more about installing .desktop files see:
#   https://www.cyberciti.biz/howto/how-to-install-and-edit-desktop-files-on-linux-desktop-entries/

"$BPY" -m ensurepip

printf "\n\n\n"
echo "Add the following to $HOME/.bashrc"
printf "\n"
echo "export BPY=\"$BPY\""
echo "export BLENDER_PATH=\"$BLENDER_FOLDER\""
