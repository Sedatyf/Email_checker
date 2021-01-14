echo "Do you want to (S)earch a specific mail or check (M)ultiple mail? (S/M) "
read app_choice

USERNAME=$(grep USERNAME config.env | cut -d '=' -f2)
PASSWORD=$(grep PASSWORD config.env | cut -d '=' -f2)
IMAP=$(grep IMAP config.env | cut -d '=' -f2)

if [ ${app_choice,,}  == 'm' ]; then
    echo "Script will check N emails starting from the top. How much email do you want to check? "
    read N

    re='^[0-9]{1,2}$'
    correct=0

    if ! [[ $N =~ $re ]]; then
        echo "[!] Error: you have to precise a number between 0 and 99"
    else
        correct=1
    fi

    if [ $correct == 1 ]; then
        # TODO : check if an image exists if not, build it from Dockerfile
        docker run -e PYTHONUNBUFFERED=1 sedatyf/email_checker:latest -m $N
    fi

elif [ ${app_choice,,} == 's' ]; then
    echo "Script will check for a specific mail. What's the subject of your mail? "
    read subject

    # TODO : check if an image exists if not, build it from Dockerfile
    docker run -e PYTHONUNBUFFERED=1 sedatyf/email_checker:latest -s $subject -a r
else
    echo "Unkwown parameter"
fi