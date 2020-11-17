import requests


def main():
    target_timezone = "Europe/Moscow"
    req = requests.get(f"http://localhost:8080/{target_timezone}")
    print(f'Requesting info for {target_timezone}')
    print(req.text)
    start = {"date": "12:30pm 2020-12-01", "tz": target_timezone}
    end = {"date": "12.20.2021 22:21:05", "tz": "EST"}
    req = requests.post(f"http://localhost:8080/api/v1/time?tz=EST")
    print(req.text)
    req = requests.post(f"http://localhost:8080/api/v1/date?tz=EST")
    print(req.text)
    req = requests.post(f"http://localhost:8080/api/v1/datediff?start={start}&end={end}")
    print(req.text)


if __name__ == '__main__':
    main()
