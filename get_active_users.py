def get_active_users():
    active_users = []
    try:
        with open('/etc/passwd', 'r') as file:
            # Using list comprehension to filter active users
            active_users = [
                line.split(':')[0]  # Get the username
                for line in file
                if int(line.split(':')[2]) >= 1000 and line.split(':')[0] != 'nobody'  # Check UID and exclude 'nobody'
            ]
    except FileNotFoundError:
        print("The /etc/passwd file does not exist.")
    except ValueError:
        print("Error converting UID to integer.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return active_users

if __name__ == "__main__":
    users = get_active_users()
    print("Active users:")
    for user in users:
        print(user)
