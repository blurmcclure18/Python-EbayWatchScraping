url_count = 1
url = "https://pocketwatchdatabase.com/guide/company/elgin/grade/{}/value"

while url_count <= 50:
    print(url.format(url_count))
    url_count += 1

print("Done!")
