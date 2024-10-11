import os

class FileManager:

    def level_one_directory_search(dir_1: str, target: str): 
        cur_path = os.path.join(os.path.dirname(__file__),'..', '..')  # Get the user's home directory
        script_dir = os.path.abspath(cur_path)
        data_dir = os.path.join(script_dir, dir_1)
        os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists# Create a temporary file path
        return os.path.join(data_dir, target)

    def level_two_directory_search(dir_1: str, dir_2: str, target: str): # Stupid method name I know
        cur_path = os.path.join(os.path.dirname(__file__),'..', '..')  # Get the user's home directory
        home_dir = os.path.abspath(cur_path)
        data_dir = os.path.join(home_dir, dir_1)
        os.makedirs(data_dir, exist_ok=True)  # Ensure the directory exists# Create a temporary file path
        data_dir_2 = os.path.join(data_dir, dir_2)
        os.makedirs(data_dir_2, exist_ok=True)  # Ensure the directory exists# Create a temporary file path
        return os.path.join(data_dir_2, target)
    
    def read_conversation(filename):
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return []
        with open(filename, 'r') as f:
            lines = f.readlines()
        return [{'role': line.split(': ')[0], 'content': line.split(': ')[1].strip()} for line in lines]
    
    def save_conversation(messages, filename):
        with open(filename, 'w') as f:
            for message in messages:
                f.write(f"{message['role']}: {message['content']}\n")