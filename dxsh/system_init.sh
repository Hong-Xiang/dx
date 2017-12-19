mkdir $HOME/Workspace
mkdir $HOME/Softwares
mkdir $HOME/Scripts
# Add zsh
sudo apt-get install -y git zsh curl htop 
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
scp -r hongxwing@192.168.1.101:.ssh $HOME/
cp ./keys.sh $HOME/Softwares/
cp ./path.sh $HOME/Softwares/
