brand = str("Grand Arman").lower()
input_brand = str("GRAND ARMAN").lower()
for i in range(0, 15):
    iqa = brand[i]==input_brand[i]
    print(f"{brand[i]} {input_brand[i]} {iqa}")
