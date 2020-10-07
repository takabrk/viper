#!/bin/sh
# Define the clock
Clock() {
        DATETIME=$(date "+%a %b %d, %T")

        echo -n "$DATETIME"
}

# Print the clock

while true; do
        echo "%{O500px}%{l}%{F#ffffff}%{B#cdcdcd} $(Clock) %{F-}%{B-}"
        sleep 1
done