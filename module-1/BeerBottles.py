# BeerBottles.py

bottles = int(input("Enter number of bottles: "))

while bottles > 0:
    print(f"{bottles} bottle{'s' if bottles != 1 else ''} of beer on the wall, {bottles} bottle{'s' if bottles != 1 else ''} of beer.")
    bottles -= 1
    print(f"Take one down and pass it around, {bottles} bottle{'s' if bottles != 1 else ''} of beer on the wall.\n")

print("Time to buy more bottles of beer.")
