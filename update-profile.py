#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

# Define the schedule with (start_month, start_day, end_month, end_day, theme, filename, folder)
SCHEDULE = [
    (12, 30, 1, 3, "New Years", "newyears.png", "Holidays"),
    (1, 4, 3, 20, "Winter", "winter.png", "Seasons"),
    (3, 21, 5, 31, "Spring", "spring.png", "Seasons"),
    (6, 1, 7, 2, "Summer", "summer.png", "Seasons"),
    (7, 3, 7, 5, "4th of July", "4thofjuly.png", "Holidays"),
    (7, 6, 8, 31, "Summer", "summer.png", "Seasons"),
    (9, 1, 10, 25, "Fall", "fall.png", "Seasons"),
    (10, 26, 11, 1, "Halloween", "halloween.png", "Holidays"),
    (11, 2, 11, 19, "Fall", "fall.png", "Seasons"),
    (11, 20, 11, 30, "Thanksgiving", "thanksgiving.png", "Holidays"),
    (12, 1, 12, 29, "Christmas", "christmas.png", "Holidays"),
]

def date_in_range(current_date, start_month, start_day, end_month, end_day):
    """Check if current date falls within the given range."""
    month = current_date.month
    day = current_date.day
    
    # Handle ranges that cross year boundary
    if start_month > end_month:
        return (month > start_month or (month == start_month and day >= start_day) or
                month < end_month or (month == end_month and day <= end_day))
    else:
        return ((month > start_month or (month == start_month and day >= start_day)) and
                (month < end_month or (month == end_month and day <= end_day)))

def get_current_theme():
    """Determine the current theme based on today's date."""
    today = datetime.now()
    
    for start_m, start_d, end_m, end_d, theme, filename, folder in SCHEDULE:
        if date_in_range(today, start_m, start_d, end_m, end_d):
            return theme, filename, folder, f"{get_month_name(start_m)} {start_d} - {get_month_name(end_m)} {end_d}"
    
    return None, None, None, None

def get_month_name(month):
    """Convert month number to abbreviation."""
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "June", 
              "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[month]

def update_current_png(filename, folder):
    """Copy the appropriate image to current.png."""
    source = os.path.join(folder, filename)
    destination = "current.png"
    
    if os.path.exists(source):
        shutil.copy2(source, destination)
        print(f"Updated current.png to {source}")
        return True
    else:
        print(f"Warning: Source file {source} not found!")
        return False

def update_readme(theme, date_range):
    """Update the README with the current theme."""
    with open("README.md", "r") as f:
        content = f.read()
    
    # Find and replace the Current Profile Picture section
    start_marker = "## Current Profile Picture"
    end_marker = "---"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        new_section = f"""## Current Profile Picture
**{theme}**: *{date_range}*
![Current Profile](current.png)
"""
        updated_content = content[:start_idx] + new_section + content[end_idx:]
        
        with open("README.md", "w") as f:
            f.write(updated_content)
        print(f"Updated README.md with theme: {theme}")
        return True
    else:
        print("Warning: Could not find markers in README.md")
        return False

def main():
    theme, filename, folder, date_range = get_current_theme()
    
    if theme and filename and folder:
        print(f"Current theme: {theme} ({date_range})")
        update_current_png(filename, folder)
        update_readme(theme, date_range)
    else:
        print("Error: Could not determine current theme")

if __name__ == "__main__":
    main()
