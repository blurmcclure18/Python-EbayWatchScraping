from random import randint

user_agent = "user-agent={}"

headers = {
    "header": [
        "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1;)",
        "Microsoft; (Lumia 640 XL LTE)",
        "AppleWebKit/537.36 (KHTML, like Gecko)",
        "Chrome/42.0.2311.135 (Mobile)",
        "Safari/537.36",
        "Edge/12.10166",
    ]
}

print(user_agent.format(headers["header"][randint(0, 5)]))
