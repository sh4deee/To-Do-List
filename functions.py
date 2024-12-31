import os
import json
from datetime import datetime
from help_functions import HelpFunctions


class Functions:
    def __init__(self):
        self.help_functions = HelpFunctions()
        self.tasks = []
        self.load_from_json()  # Load tasks from the JSON file upon initialization

#                                                       NOTE: ADD A WAY TO MAKE DIFFRENT FILES OF TASKS OR OPEN DIFFRENT ONES

    # THE MAIN FUNCTIONS FOR THE TO DO LIST
    def add_task(self):
        while True: 
            task = self.help_functions.get_user_input("Enter task: ")
            if not task:
                self.help_functions.clear_screen()
                print("Task description cannot be empty.")
                continue
            if len(task) > 150:
                self.help_functions.clear_screen()
                print("Task is too long. Please enter a task with 150 characters or less.")
                continue
            break

        while True:  # Input for the date
            try:
                date_input = input("Enter the date (YYYY-MM-DD) or leave it blank: ").strip()
                self.help_functions.clear_screen()

                if not date_input:  # Allow blank input
                    date = None
                    print("No date provided, proceeding without a date.")
                    self.help_functions.pause()
                    self.help_functions.clear_screen()
                    break

                # Parse and validate the date
                date = datetime.strptime(date_input, "%Y-%m-%d")
                break

            except ValueError:
                self.help_functions.clear_screen()
                print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")


        priority_text ="""
Task priority
    1. high
    2. Medium
    3. low
Enter your choice: """

        input_priority = self.help_functions.get_user_input(priority_text, clear=True, input_type='int', start_invalid_input=1, end_invalid_input=3, convert_str=True)
        if input_priority == '1':
            priority = 'high'
        elif input_priority == '2':
            priority = 'medium'
        else:
            priority = 'low'

        # Add task to the list
        task_info = {
            "task": task,
            "date": date.strftime("%Y-%m-%d") if date else None,
            "completed": False,
            "priority": priority
        }        

        self.tasks.append(task_info)
        self.save_to_json()

    def remove_task(self):
        while True:
            # Check if there are any tasks to remove
            if not self.tasks:
                print("No tasks to remove.")
                break

            # Display tasks before removing
            print("\nCurrent tasks:")
            self.view_tasks(False)

            # Get the task number from the user and ensure it's an integer
            task_input = input("Enter the task number: ").strip()
            self.help_functions.clear_screen()

            # Handle empty input or non-numeric input
            if not task_input:
                print("Input cannot be empty. Please try again.")
                continue

            try:
                task_choice = int(task_input)

                # Check if the task number is valid
                if task_choice < 1 or task_choice > len(self.tasks):
                    print("Invalid task number. Please choose a valid task number.")
                    continue

                # Remove the task by index
                removed_task = self.tasks.pop(task_choice - 1)

                # Save the updated list of tasks to JSON
                self.remove_task_from_json(removed_task)
                break

            except ValueError:
                # Handle case where input is not a valid number
                print("Invalid input. Please enter a valid task number.")

    def delete_all(self):
        if not self.tasks:
            print("There is no tasks to delete")
            return
        
        text ="""
You sure you wanna delete all tasks?
    1. yes
    2. no
Enter your choise: """
        user_choice = self.help_functions.get_user_input(text, clear=True, input_type='int', start_invalid_input=1, end_invalid_input=2, convert_str=True)

        if user_choice == '1':
            self.tasks = []
            self.save_to_json()
        else:
            return

    def mark_task_complete(self):
        # Get the list of incomplete tasks
        incompleted_tasks = [task for task in self.tasks if not task["completed"]]

        if not incompleted_tasks:
            self.help_functions.clear_screen()
            print("No tasks to mark as complete.")
            return

        while True:
            # Display the tasks
            self.help_functions.clear_screen()
            for i, task in enumerate(incompleted_tasks):
                formatted_date = task["date"] if task["date"] else "N/A"
                print(f"{i + 1}- {task['task']} | DATE: {formatted_date}")
                print("-" * 30)

            # Get the task number from the user
            task_input = input("Choose the task to complete: ").strip()
            self.help_functions.clear_screen()

            # Handle empty input or non-numeric input
            if not task_input:
                print("Input cannot be empty. Please try again.")
                continue

            try:
                task_number = int(task_input)

                # Check if the task number is valid
                if task_number < 1 or task_number > len(incompleted_tasks):
                    print("Invalid task number. Please choose a valid task number.")
                    continue

                # Mark the task as complete
                self.tasks[self.tasks.index(incompleted_tasks[task_number - 1])]["completed"] = True
                print("Task marked as completed successfully.")
                break

            except ValueError:
                # Handle case where input is not a valid number
                print("Invalid input. Please enter a valid task number.")
    
        # Save to JSON after marking a task as complete
        self.save_to_json()

    def edit_task(self): # make better prints
        if not self.tasks:
            print("No tasks to edit.")
            return

        while True:
            # Display tasks before editing
            print("\nCurrent tasks:")
            self.view_tasks(False)

            # Get the task number from the user
            task_input = input("Enter the task number to edit: ").strip()
            self.help_functions.clear_screen()

            # Validate task input
            if not task_input:
                print("Input cannot be empty. Please try again.")
                continue

            if not task_input.isdigit() or int(task_input) < 1 or int(task_input) > len(self.tasks):
                print("Invalid task number. Please choose a valid task number.")
                continue

            task_choice = int(task_input) - 1
            selected_task = self.tasks[task_choice]

            print(f"Editing Task: {selected_task['task']}")
            print("-" * 40)

            # Edit task fields
            selected_task["task"] = input(
                f"Enter new task name (leave empty to keep '{selected_task['task']}'): "
            ).strip() or selected_task["task"]
            self.help_functions.clear_screen()

            while True:
                new_date = input(
                    f"Enter new date (YYYY-MM-DD) or leave empty to keep '{selected_task['date']}'): "
                ).strip()
                self.help_functions.clear_screen()
                if not new_date:  # Keep the current date
                    break
                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                    selected_task["date"] = new_date
                    break
                except ValueError:
                    print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")

            # Edit completion status
            while True:
                new_status = input(
                    "Mark task as Completed or Not Completed? (completed/not completed, leave empty to keep current): "
                ).strip().lower()
                self.help_functions.clear_screen()
                if not new_status:  # Keep current status if input is empty
                    break
                if new_status in {"completed", "not completed"}:
                    selected_task["completed"] = (new_status == "completed")
                    break
                print("Invalid input. Please enter 'completed' or 'not completed'.")

            # Edit priority
            while True:
                new_priority = input(
                    f"Enter new priority (High, Medium, Low) or leave empty to keep '{selected_task['priority']}'): "
                ).strip().lower()
                self.help_functions.clear_screen()
                if not new_priority:  # Keep current priority
                    break
                if new_priority in {"high", "medium", "low"}:
                    selected_task["priority"] = new_priority
                    break
                print("Invalid priority. Please enter 'high', 'medium', or 'low'.")
            break

        # Save updated list to JSON, making sure there are no duplicates
        self.save_to_json()

    def view_tasks(self, pause_and_clear=True):
        if not self.tasks:
            print("No tasks to view.")
            return False
        
        # Display tasks
        for i, task in enumerate(self.tasks):
            status = "✔" if task["completed"] else "❌"
            formatted_date = task["date"] if task["date"] else "N/A"
            print(f"[TASK {i + 1}] | Task: {task['task']} | Due Date: {formatted_date or 'No Date'} | Status: {status} | Priority: {task['priority']}")
        # Pause and clear the screen if flag is True
        if pause_and_clear:
            self.help_functions.pause()
            self.help_functions.clear_screen()

    def sort_tasks(self):

        if not self.tasks:
            print("No tasks to sort.")
            return False
        
        text = """
How do you want to sort your tasks:
    1. By letters
    2. By date
    3. By completion
    4. By high priority
    5. by low priority
Enter your choice: """
        

        choice = self.help_functions.get_user_input(text, clear=True, input_type='int', start_invalid_input=1, end_invalid_input=5, convert_str=True)
        
        if choice == '1':
            sort_type = 'letters'
        elif choice == '2':
            sort_type = 'date'
        elif choice == '3':
            sort_type = 'completed'
        elif choice == '4':
            sort_type = 'high priority'
        else:
            sort_type = 'low priority'

        self.sort_tasks_in_json(sort_by=sort_type)

    def filter_tasks(self):
        filter_by_text = """
How do you want to filter your tasks
    1. By date
    2. By priority
Enter your choice: """

        user_choice = self.help_functions.get_user_input(filter_by_text, clear=True, input_type='int', start_invalid_input=1, end_invalid_input=2, convert_str=True)
        
        if user_choice == '1':
            while True:  # Input for the date
                try:
                    date_input = input("Enter the date (YYYY-MM-DD): ").strip()
                    self.help_functions.clear_screen()

                    # Parse and validate the date
                    date = datetime.strptime(date_input, "%Y-%m-%d")
                    date_filtered = [task for task in self.tasks if datetime.strptime(task['date'], "%Y-%m-%d") >= date]
                    for task in date_filtered:
                        print(task)
                    break

                except ValueError:
                    self.help_functions.clear_screen()
                    print("Invalid date format. Please enter a valid date in YYYY-MM-DD format.")

        elif user_choice == '2':
            priority_text = """
Filter by priority
    1. High
    2. Medium
    3. Low
Enter your choice: """
    
            priority_map = {1: 'high', 2: 'medium', 3: 'low'}
            input_priority = self.help_functions.get_user_input(priority_text, clear=True, input_type='int', start_invalid_input=1, end_invalid_input=3)

            # Get the corresponding priority label
            priority_label = priority_map.get(int(input_priority))

            # Filter tasks based on the selected priority
            filtered_tasks = [task for task in self.tasks if task['priority'] == priority_label]

            for task in filtered_tasks:
                print(task)



    # THE MAIN FUNCTIONS FOR SAVING DATA IN JSON FORM
    def save_to_json(self, filename="tasks.json"):
        # Save the current tasks to the JSON file
        with open(filename, "w") as file:  # Open in write mode 'w' to overwrite the file
            json.dump(self.tasks, file, indent=4)

    def load_from_json(self, filename="tasks.json"):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    self.tasks = json.load(file)
                    if not self.tasks:
                        self.tasks = []
        except FileNotFoundError:
            # No print statement, silently handle the case when the file doesn't exist
            self.tasks = []

    def remove_task_from_json(self, task_to_remove, filename="tasks.json"):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    current_data = json.load(file)

                # Remove the task from current_data if it exists
                current_data = [task for task in current_data if not (task["task"] == task_to_remove["task"] and task["date"] == task_to_remove["date"])]
                
                # Write the updated data back to the file
                with open(filename, "w") as file:
                    json.dump(current_data, file, indent=4)

                # Update the local task list
                self.tasks = current_data  # Load the new data into self.tasks

        except FileNotFoundError:
            # Handle file not found silently (just ensure tasks are empty)
            self.tasks = []

    def sort_tasks_in_json(self, sort_by=None, filename="tasks.json"):
        """
Sort tasks in the JSON file based on the provided criteria.

Args:
    sort_by (str): The criterion by which to sort tasks. Can be 'letters', 'date', 'completed', 
                'high priority', or 'low priority'.
    filename (str): The name of the JSON file containing tasks (default is 'tasks.json').

Returns:
    None: Modifies the task list in the provided JSON file.
        """
        # List of valid sorting criteria
        valid_criteria = ['letters', 'date', 'completed', 'high priority', 'low priority']

        # Mapping of priority levels for sorting: high < medium < low
        priority_map = {'high': 1, 'medium': 2, 'low': 3}

        # Check if the sort_by argument is valid
        if sort_by not in valid_criteria:
            print("Invalid sorting criteria. Use 'letters', 'date', 'completed', 'high priority', or 'low priority'.")
            return

        try:
            # Check if the file exists before trying to read
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    current_data = json.load(file)  # Load current tasks from JSON file

                # Sort the tasks based on the provided criterion
                if sort_by == 'letters':
                    # Sort tasks by task name (case-insensitive)
                    current_data.sort(key=lambda task: task['task'].lower())  
                    # Convert task names to lowercase for case-insensitive sorting

                elif sort_by == 'date':
                    # Sort tasks by date (None/empty dates come last)
                    current_data.sort(key=lambda task: (task['date'] is None, task['date']))
                    # The key (task['date'] is None, task['date']) ensures that None values (empty dates) come last.

                elif sort_by == 'completed':
                    # Sort tasks by completion status (incomplete tasks first, then completed tasks)
                    current_data.sort(key=lambda task: task['completed'])  
                    # task['completed'] will sort False (incomplete tasks) before True (completed tasks).

                elif sort_by == 'high priority':
                    # Sort tasks by priority (high priority tasks come first)
                    current_data.sort(key=lambda task: priority_map.get(task['priority']))
                    # priority_map.get() retrieves the numeric value for priority with high priority comes first.

                elif sort_by == 'low priority':
                    # Sort tasks by priority (low priority tasks come first)
                    current_data.sort(key=lambda task: priority_map.get(task['priority']), reverse=True)
                    # priority_map.get() retrieves the numeric value for priority and  reverse=True ensures low priority comes first.

                # Save the sorted tasks back into the JSON file
                with open(filename, "w") as file:
                    json.dump(current_data, file, indent=4)  # Write the sorted data back to the file

                # Update the local task list
                self.tasks = current_data  # Load the sorted data into self.tasks

            else:
                print(f"Error: The file '{filename}' does not exist.")  # Error if file doesn't exist

        except Exception as e:
            print(f"An error occurred: {e}")  # Handle any unexpected errors