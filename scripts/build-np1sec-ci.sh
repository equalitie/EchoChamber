set -x
set -e
if [ ! -e np1sec/jabberite ]; then
  sudo apt-get install -y cmake libgcrypt20-dev libglib2.0-dev libreadline-dev libpurple-dev
  git clone https://github.com/equalitie/np1sec.git && cd np1sec
  cmake .
  make
fi
