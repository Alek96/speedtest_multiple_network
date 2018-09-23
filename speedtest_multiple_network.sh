#/bin/bash

#SSIDNames=("ZAMO-HOME" "Orange-51FE" "HUAWEI-B315-E665")
SSIDNames=("ZAMO-HOME" "HUAWEI-B315-E665")

for SSIDName in "${SSIDNames[@]}"
do
    echo "`date \"+%F %T\"` Try connecto to $SSIDName"
    echo "`date \"+%F %T\"` `nmcli connection up $SSIDName`"

    sleep 10

    echo "`date \"+%F %T\"` Check internet connection"
    nm-online -q
    if [ $? -ne 0 ]; then
    #if [[ "$(ping -c 1 google.com | grep '100% packet loss' )" != "" ]]; then
        echo "`date \"+%F %T\"` No internet connection wia $SSIDName"
        continue
    fi
    echo "`date \"+%F %T\"` Internet connection is working"

    echo "`date \"+%F %T\"` Run speed test"
    "$(dirname "$0")/speedtest.sh"
    echo "`date \"+%F %T\"` Speed test finished"
done


