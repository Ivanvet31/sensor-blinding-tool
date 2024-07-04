for port in $(seq 1 65535); do
    nc -l -p $port &
done
