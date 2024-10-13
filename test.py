with open("school_times.txt", "r+") as file:
    all_times = []
    data = [line.replace("\n", "").split("Stunde")[1].split("-") for line in file.readlines()]
    for each in data:
        for every_time in each:
            all_times.append(every_time.strip())

    print(all_times)

print(list(set(["10", "10", "2"])))
