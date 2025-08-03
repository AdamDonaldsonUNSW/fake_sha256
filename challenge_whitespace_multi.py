import hashlib
import itertools
import multiprocessing

whitespace_chars = [' ', '\t', '\n']

def hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def compareHash(real_hash, fake_hash, num_digits):
    return real_hash[-num_digits:] == fake_hash[-num_digits:]

def worker(args):
    real_hash, base_data, combo, num_digits = args
    attempt = base_data + ''.join(combo)
    fake_hash = hash(attempt)
    if compareHash(real_hash, fake_hash, num_digits):
        return (True, attempt, fake_hash)
    return (False, None, None)

def findHash(real_hash, fake_file, num_digits):
    with open(fake_file, "r") as fake:
        fake_data = fake.read()

    max_length = 1
    count = 0
    while True:
        combos = list(itertools.product(whitespace_chars, repeat=max_length))
        args = [(real_hash, fake_data, combo, num_digits) for combo in combos]

        found = False
        result_data = None

        with multiprocessing.Pool() as pool:
            for result in pool.imap_unordered(worker, args, chunksize=100):
                count += 1
                matched, attempt, fake_hash = result
                if matched:
                    found = True
                    result_data = (count, fake_hash, attempt)
                    break

        if found:
            return result_data

        max_length += 1

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

if __name__ == "__main__":
    main()