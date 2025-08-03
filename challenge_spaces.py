import hashlib

def hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def compareHash(real_hash, fake_hash, num_digits):
    return real_hash[-num_digits:] == fake_hash[-num_digits:]


def findHash(real_hash, fake_file, num_digits):
    with open(fake_file, "r") as fake:
        fake_data = fake.read()

    count = 0
    found = False
    while not found:
        fake_hash = hash(fake_data)
        if compareHash(real_hash, fake_hash, num_digits):
            found = True
        else:
            fake_data += " "
        count += 1

    return count, fake_hash, fake_data

def main():
    real_file = input("Enter Real File: ")
    fake_file = input("Enter Fake File: ")

    with open(real_file, "r") as real:
        real_data = real.read()
    fake_data = ""
    terminate = False

    while not terminate:
        num_digits = int(input("How many identical end digits: "))

        real_hash = hash(real_data)
        count, fake_hash, fake_data = findHash(real_hash, fake_file, num_digits)

        print(f"Matched after {count} additions.")
        print(f"Final Fake Hash: {fake_hash}")
        print(f"Final Real Hash: {real_hash}")

        loop = input("Try again with different number (Y/N)? ")
        loop = loop.lower()
        if loop == "yes" or loop == "y":
            terminate = False
        else:
            terminate = True

    writeToFile = input("Do you want to overwrite fake file (Y/N)? ")
    writeToFile = writeToFile.lower()
    if writeToFile == "yes" or writeToFile == "y":
        with open(fake_file, "w") as fake:
            fake.write(fake_data)

main()