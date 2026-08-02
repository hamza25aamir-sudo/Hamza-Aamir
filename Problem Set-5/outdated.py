months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

try:
    while True:   #MM/DD/YYY
        Date = input("Date: ").strip()
        if "/" in Date:
            month, day, year = Date.split("/")
            month = int(month)
            day = int(day)
            year = int(year)

        elif "," in Date: 
            month_name, rest = Date.split(" ", 1)
            day, year = rest.split(",")

            month = months.index(month_name) + 1
            day = int(day)
            year = int(year)

        else:
            continue

        # Validate month and day
        if 1 <= month <= 12 and 1 <= day <= 31:
            print(f"{year:04}-{month:02}-{day:02}")
            break
except(ValueError, IndexError):
    pass