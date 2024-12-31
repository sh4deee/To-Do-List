import os

class HelpFunctions:

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause(self):
        input("Press Enter to continue...")

    def text_helper(self, text, clear_pause=False):
        print(text)
        if clear_pause:
            self.pause()
            self.clear_screen()

    def get_user_input(self, prompt, clear=False, input_type=None, start_invalid_input=None, end_invalid_input=None, convert_str=False):
        """
Gets user input and validates it based on the expected type, converting numeric inputs to strings after validation.

Args:
    prompt (str): The message to display to the user.
    input_type (str): The expected type of input ('int', 'float', None).
    start_invalid_input (int, optional): The start of the valid input range.
    end_invalid_input (int, optional): The end of the valid input range.
    clear (bool, optional): Whether to clear the screen after input.
    convert_str (bool, optional): Whether to convert the input to string before returning.
    
Returns:
    str: The validated user input as a string.
        """
        while True:
            # Get user input
            user_input = input(prompt)

            # Check if input is empty
            if not user_input.strip():
                if clear:
                    self.clear_screen()
                print("You did not enter anything. Please try again.")
                continue

            try:
                # Handle numeric inputs (int or float)
                if input_type in ['int', 'float']:
                    user_input = float(user_input) if input_type == 'float' else int(user_input)

                    # Validate range if both start and end are provided
                    if start_invalid_input is not None and end_invalid_input is not None:
                        if not (start_invalid_input <= user_input <= end_invalid_input):
                            if clear:
                                self.clear_screen()

                            between_sign = 'or' if start_invalid_input == 1 and end_invalid_input == 2 else 'and'
                            print(f"Invalid choice. Please enter a number between {start_invalid_input} {between_sign} {end_invalid_input}.")
                            continue

                if convert_str:
                    # Convert input to string before returning
                    user_input = str(user_input)

                # Clear screen if specified
                if clear:
                    self.clear_screen()

                return user_input

            except ValueError:
                # Display appropriate error message for invalid numeric inputs
                if clear:
                    self.clear_screen()
                else:
                    error_message = "integer" if input_type == "int" else "float" if input_type == "float" else "input"
                    print(f"Invalid {error_message}. Please try again.")