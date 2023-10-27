# Open a file in write mode ('w')
with open('user_input.txt', 'w') as file:
    # Keep taking user input until they enter an empty line
    while True:
        user_input = input("Enter something (or press Enter to stop): ")
        
        # If user enters an empty line, stop taking input
        if user_input == "":
            break
        
        # Write the user input to the file
        file.write(user_input + "\n")

print("User input has been saved to 'user_input.txt'")
