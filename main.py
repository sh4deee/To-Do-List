from help_functions import HelpFunctions
from functions import Functions

class Program:
    def __init__(self):
        self.help_functions = HelpFunctions()
        self.functions = Functions()

    def main_menu(self):
        message = """
Welcome to the To-Do List Program!
Please choose an option from the menu below:

    1. Add tasks to the list
    2. Remove tasks from the list
    3. Delete all tasks
    4. Mark tasks as complete
    5. Edit tasks
    6. View tasks
    7. Sort tasks
    8. Filter tasks
    9. Quit

Enter your choice: """

        choice_map = {
            1: self.functions.add_task,
            2: self.functions.remove_task,
            3: self.functions.delete_all,
            4: self.functions.mark_task_complete,
            5: self.functions.edit_task,
            6: self.functions.view_tasks,
            7: self.functions.sort_tasks,
            8: self.functions.filter_tasks,
            9: exit
        }

        while True:
            choice = self.help_functions.get_user_input(message, clear=True, input_type='int', start_invalid_input=1, end_invalid_input=9)

            if choice in choice_map:
                if choice == 9:
                    print("Thanks for using my to-do list program.")
                    break  
                else:
                    choice_map[choice]()

if __name__ == "__main__":
    main = Program()
    main.main_menu()