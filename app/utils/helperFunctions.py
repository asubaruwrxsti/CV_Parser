import os

def loadEnv(file=".env"):
    if not os.path.isfile(file):
        print(f"Error: {file} not found.")
        exit()

    # Load environment variables as a dictionary
    env = {}
    with open(f"{file}", "r") as f:
        for line in f:
            if line[0] != '#':
                key, value = line.strip().split('=')
                env[key] = value
    return env
