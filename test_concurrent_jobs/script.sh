#!/bin/bash

counter=1
while [ $counter -le 500 ]
do
echo $counter
((counter++))
ray job submit -- python long_running.py --no-wait &
done
echo All done
