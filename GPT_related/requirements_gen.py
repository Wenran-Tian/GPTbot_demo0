import os

def generate_requirements():
    os.system('pip freeze > requirements.txt')

if __name__ == "__main__":
    generate_requirements()
    print("requirements.txt generated.")