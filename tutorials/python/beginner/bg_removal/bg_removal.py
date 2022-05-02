from rembg import remove
import os

for file in os.listdir('./pics'):
    print(f'Processing {file}')
    with open(f'./pics/{file}', 'rb') as i:
        with open(f'./out_pics/{file}', 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)