import os
import datetime

def read_cron_log(log_file_path):
    if not os.path.exists(log_file_path):
        print(f"Log file {log_file_path} does not exist.")
        return []

    with open(log_file_path, 'r') as file:
        return file.readlines()

def parse_cron_entries(log_lines, time_threshold):
    recent_entries = []
    for line in log_lines:
        # Check if the line contains a cron job entry
        if "CRON" in line:
            # Assuming the log format is: "Month Day Time Host CRON[PID]: (user) CMD"
            parts = line.split()
            if len(parts) < 6:
                continue  # Skip lines that don't have enough parts

            # Extract the timestamp
            log_time_str = ' '.join(parts[:3])  # Month Day Time
            log_time = datetime.datetime.strptime(log_time_str, '%b %d %H:%M:%S')

            # Get the current time and calculate the time difference
            now = datetime.datetime.now()
            log_time = log_time.replace(year=now.year)  # Assume the same year for simplicity
            time_diff = now - log_time

            # Check if the entry is recent
            if time_diff <= time_threshold:
                recent_entries.append(line.strip())

    return recent_entries

def main():
    log_file_path = '/var/log/syslog'
    time_threshold = datetime.timedelta(hours=1)  # Define "recent" as within the last hour

    log_lines = read_cron_log(log_file_path)
    recent_cron_jobs = parse_cron_entries(log_lines, time_threshold)

    if recent_cron_jobs:
        print("Recent cron jobs:")
        for entry in recent_cron_jobs:
            print(entry)
    else:
        print("No recent cron jobs found.")

if __name__ == "__main__":
    main()
