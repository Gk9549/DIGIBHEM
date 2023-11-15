import datetime
import sched
import sys
import time

# Create a scheduler to manage reminders
reminder_scheduler = sched.scheduler(timefunc=time.monotonic, delayfunc=time.sleep)

# Store reminders in a list of dictionaries
reminders = []

def create_reminder():
    event_name = input("Enter event name: ")
    date_str = input("Enter date (YYYY-MM-DD): ")
    time_str = input("Enter time (HH:MM): ")
    notes = input("Optional notes: ")
    
    try:
        event_date = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        reminders.append({
            'event_name': event_name,
            'event_date': event_date,
            'notes': notes
        })
        print("Reminder created successfully!")
    except ValueError:
        print("Invalid date or time format. Use YYYY-MM-DD HH:MM.")

def view_reminders():
    if reminders:
        print("Upcoming Reminders:")
        for idx, reminder in enumerate(reminders, 1):
            print(f"{idx}. Event: {reminder['event_name']}")
            print(f"   Date and Time: {reminder['event_date'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   Notes: {reminder['notes']}")
    else:
        print("No reminders to display.")

def delete_reminder():
    view_reminders()
    if reminders:
        try:
            index = int(input("Enter the reminder number to delete: ")) - 1
            if 0 <= index < len(reminders):
                deleted_event = reminders.pop(index)
                print(f"Reminder for '{deleted_event['event_name']}' deleted.")
            else:
                print("Invalid reminder number.")
        except ValueError:
            print("Invalid input. Enter a valid number.")
    else:
        print("No reminders to delete.")

def schedule_reminders():
    now = datetime.datetime.now()
    for reminder in reminders:
        event_date = reminder['event_date']

        if now < event_date:
            time_difference = (event_date - now).total_seconds()
            reminder_scheduler.enter(time_difference, 1, show_reminder, (reminder,))
    reminder_scheduler.run()

def show_reminder(reminder):
    print("\nReminder:")
    print(f"Event: {reminder['event_name']}")
    print(f"Date and Time: {reminder['event_date'].strftime('%Y-%m-%d %H:%M')}")
    print(f"Notes: {reminder['notes']}")

def main():
    while True:
        print("\nReminder Application Menu:")
        print("1. Create Reminder")
        print("2. View Reminders")
        print("3. Delete Reminder")
        print("4. Schedule Reminders")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            create_reminder()
        elif choice == '2':
            view_reminders()
        elif choice == '3':
            delete_reminder()
        elif choice == '4':
            schedule_reminders()
        elif choice == '5':
            sys.exit("Goodbye!")
        else:
            print("Invalid choice. Please choose 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
