import time

def do_something(loop_num):
    result = f'Doing something... {loop_num}'
    time.sleep(0.1)
    return result
    
# NO PROGRESS BAR
for i in range(10):
    print(do_something(i))
print("Process Completed")

# USING TRACK PROGRESS BAR
from rich.progress import track

for n in track(range(10), description="Doing Something"):
    do_something(n)

# USING PROGRESS TO CREATE A BAR
from rich.progress import Progress
with Progress() as progress:

    task1 = progress.add_task("[red]Doing Something", total=10)
    for i in range(10):
        progress.update(task1, advance=1, description=f'[yellow]{do_something(i)}')
    progress.update(task1, description='[green]Process Completed!')
    
# USING PROGRESS TO CREATE MULTIPLE BARS
from rich.progress import Progress
with Progress() as progress:

    task1 = progress.add_task("[red]Doing Something", total=10)
    task2 = progress.add_task("[blue]Doing Something Else", total=10)
    for i in range(10):
        progress.update(task1, advance=1, description=f'[yellow]{do_something(i)}')
        progress.update(task2, advance=1, description=f'[magenta]{do_something(i)}')
    progress.update(task1, description='[green]Process 1 Completed!')
    progress.update(task2, description='[green]Process 2 Completed!')