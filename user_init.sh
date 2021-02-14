echo "Do you want to (S)earch a specific mail or check (M)ultiple mail? (S/M) "
read app_choice

if [ ${app_choice,,}  == 'm' ]; then
    isImage=$(docker images)
    if ! [[ $isImage == *"email_checker"* ]]; then
        docker build -t email_checker .
    else
        echo "[+] Docker images is already build"
    fi

    echo "Do you want to save your report as a file? Y/N "
    read report_choice
    if [ $report_choice == 'y' ]; then
        docker run -e PYTHONUNBUFFERED=1 email_checker -m -r
        docker_id=$(docker ps -aqf ancestor=email_checker:latest)
        docker cp $docker_id:/Email_checker/app/reports /tmp
    else
        docker run -e PYTHONUNBUFFERED=1 email_checker -m
    fi

elif [ ${app_choice,,} == 's' ]; then
    echo "Script will check for a specific mail. What's the subject of your mail? "
    read subject

    isImage=$(docker images)
        if ! [[ $isImage == *"email_checker"* ]]; then
            docker build -t email_checker .
        else
            echo "[+] Docker images is already build"
        fi
    docker run -e PYTHONUNBUFFERED=1 email_checker -s $subject
else
    echo "Unkwown parameter"
fi
