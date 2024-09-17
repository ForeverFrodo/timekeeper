# timekeeper
This is a simple timekeeping cli for improved personal timekeeping accountability and tracking.

NOTE: This project currently assumes a linux filesystem.

# Setup

Navigate to the project directory and run `install.sh`:
```sh
source install.sh
```
Follow the prompts to set the relevant paths, or just enter through to go with the default options.

# Use

TODO: expand this section
- `timekeeper clock_in` to clock in. If it's the first clock-in of the day, it will prompt you for a target amount of hours.
- `timekeeper clock_out` clocks out. If you haven't completed your hours, it will update you on how much time you have left. Otherwise, if you've completed your time, it will move the current log file to history and congradulate you.
- `timekeeper status` shows the current state of your hours for the day (clock-ins/outs, hours left, duration worked, time you get off, etc...)
