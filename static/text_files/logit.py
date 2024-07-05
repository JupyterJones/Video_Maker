def logit(message):
    try:
        # Get the current timestamp
        timestr = datetime.datetime.now().strftime('%A_%b-%d-%Y_%H-%M-%S')

        # Get the caller's frame information
        caller_frame = inspect.stack()[1]
        filename = caller_frame.filename
        lineno = caller_frame.lineno

        # Convert message to string if it's a list
        if isinstance(message, list):
            message_str = ' '.join(map(str, message))
        else:
            message_str = str(message)

        # Construct the log message with filename and line number
        log_message = f"{timestr} - File: {filename}, Line: {lineno}: {message_str}\n"

        # Open the log file in append mode
        with open("log.txt", "a") as file:
            # Get the current position in the file
            file.seek(0, 2)
            pos = file.tell()

            # Write the log message to the file
            file.write(log_message)

            # Print the log message to the console
            print(log_message)

            # Return the position as the ID
            return pos
    except Exception as e:
        message_str = str(message)
        # If an exception occurs during logging, print an error message
        print(f"Error occurred while logging: {e}")