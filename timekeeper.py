#!/usr/bin/env python3

import argparse
import os
import json
from datetime import datetime, timedelta
import time

DATA_DIR = '/home/is4s/.timekeeper'
LOG_DIR = os.path.join(DATA_DIR, "logs")
HISTORY_DIR = os.path.join(DATA_DIR, "history")


def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)


def get_log_file():
    return os.path.join(LOG_DIR, f"{datetime.now().date()}.json")


def load_log():
    log_file = get_log_file()
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            return json.load(file)
    return {"clock_ins": [], "clock_outs": [], "target_duration": None}


def save_log(log):
    with open(get_log_file(), "w") as file:
        json.dump(log, file)


def clock_in():
    log = load_log()
    now = datetime.now()
    log["clock_ins"].append(now.isoformat())

    if log["target_duration"] is None:
        target_duration = input(
            "Enter the duration you want to work today (in hours): "
        )
        log["target_duration"] = float(target_duration)

    save_log(log)
    print(f"⏰ Clocked in at {now.strftime('%H:%M:%S')}")
    calculate_remaining_time(log)


def clock_out():
    log = load_log()
    now = datetime.now()
    log["clock_outs"].append(now.isoformat())
    save_log(log)
    print(f"⏰ Clocked out at {now.strftime('%H:%M:%S')}")
    calculate_remaining_time(log, clock_out=True)


def calculate_remaining_time(log, clock_out=False):
    i = min(len(log["clock_ins"]), len(log["clock_outs"]))
    total_worked = (
        sum(
            (
                datetime.fromisoformat(out) - datetime.fromisoformat(inn)
            ).total_seconds()
            for inn, out in zip(log["clock_ins"][:i], log["clock_outs"][:i])
        )
        / 3600
    )  # convert seconds to hours

    if not clock_out:
        total_worked += (
            datetime.now() - datetime.fromisoformat(log["clock_ins"][-1])
        ).total_seconds() / 3600

    remaining_time = log["target_duration"] - total_worked
    if remaining_time <= 0:
        print(
            "🎉 Congratulations! You've completed your target duration for the day."
        )
        save_to_history(log)
    else:
        end_time = datetime.now() + timedelta(hours=remaining_time)
        print(f"⏳ Remaining time to work today: {remaining_time:.2f} hours")
        print(f"🕒 You need to work until: {end_time.strftime('%H:%M:%S')}")


def save_to_history(log):
    history_file = os.path.join(HISTORY_DIR, f"{datetime.now().date()}.json")
    with open(history_file, "w") as file:
        json.dump(log, file)
    os.remove(get_log_file())


def status():
    log = load_log()
    i = min(len(log["clock_ins"]), len(log["clock_outs"]))
    total_worked = (
        sum(
            (
                datetime.fromisoformat(out) - datetime.fromisoformat(inn)
            ).total_seconds()
            for inn, out in zip(log["clock_ins"][:i], log["clock_outs"][:i])
        )
        / 3600
    )  # convert seconds to hours

    if len(log["clock_ins"]) > 0 and len(log["clock_outs"]) < len(
        log["clock_ins"]
    ):
        total_worked += (
            datetime.now() - datetime.fromisoformat(log["clock_ins"][-1])
        ).total_seconds() / 3600

    remaining_time = (
        log["target_duration"] - total_worked if log["target_duration"] else 0
    )
    end_time = (
        datetime.now() + timedelta(hours=remaining_time)
        if remaining_time > 0
        else None
    )

    print("📊 Status Report:")
    print(f"🕰 Clock-ins:")
    for i in log['clock_ins']:
        print(f"\t{i}")
    print(f"🕰 Clock-outs:")
    for i in log['clock_outs']:
        print(f"\t{i}")
    print(f"🌞 Duration worked: {total_worked:.2f} hours")
    print(f"🏹 Target time: {log["target_duration"]} hours")
    print(f"⏳ Duration left to work: {remaining_time:.2f} hours")
    if end_time:
        for j in range(2):
            c = '\U0001F550'
            for i in range(12):
                print(
                    "\r"
                    + c
                    + f" Time to get off: {end_time.strftime('%H:%M:%S')}",
                    end="",
                )
                c = chr(ord(c) + 1)
                time.sleep(0.1)
        print("")


def main():
    ensure_dirs()
    parser = argparse.ArgumentParser(
        description="Timekeeper CLI - Track your work hours easily"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    parser_clock_in = subparsers.add_parser(
        "clock_in", help="Clock in and start tracking time"
    )
    parser_clock_out = subparsers.add_parser(
        "clock_out", help="Clock out and stop tracking time"
    )
    parser_status = subparsers.add_parser(
        "status", help="Show the current status of your work hours"
    )

    args = parser.parse_args()

    if args.command == "clock_in":
        clock_in()
    elif args.command == "clock_out":
        clock_out()
    elif args.command == "status":
        status()


if __name__ == "__main__":
    main()
