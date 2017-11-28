mkdir $HOME/Workspace
mkdir $HOME/Softwares
# Add zsh
sudo apt-get install -y git zsh curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
cp ./keys.sh $HOME/Softwares/