import shutil
import sys

# Get the disk usage statistics
total, used, free = shutil.disk_usage("/")

# Calculate the percentage of disk used
percent_used = (used / total) * 100

# Check if the available space is less than or equal to 10%
if percent_used >= 90:
    print("full")
    sys.exit(1)  # Exit with a status code of 1 to indicate failure
else:
    print(f"Disk is {percent_used:.2f}% full")
    sys.exit(0)  # Exit with a status code of 0 to indicate success
