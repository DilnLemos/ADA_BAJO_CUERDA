import os
import random as r

def generatefiles(size):
    file_path = f'test_{size}.txt'
    
    content = [f"{r.randint(1, 10)},{r.randint(1, 10)},{r.randint(1, 4)}" for _ in range(size)]


    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{size}\n")
        
        for i in content:
            file.write(f"{i}\n")

    print(f"File successfully saved at: {file_path}")

if __name__ == "__main__":
    sizes = [10, 16, 18, 20,25]
    for size in sizes:
        generatefiles(size)