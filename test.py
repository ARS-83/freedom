import requests

url = "http://149.104.79.176:2053/zAogYERqaVfe5qfCai/panel/inbound/addClient"

payload = "id=2&settings=%7B%22clients%22%3A%20%5B%7B%0A%20%20%22id%22%3A%20%22459e6636-5b5a-4112-890c-92705e1bb67d%22%2C%0A%20%20%22flow%22%3A%20%22%22%2C%0A%20%20%22email%22%3A%20%226v4zljdd%22%2C%0A%20%20%22limitIp%22%3A%200%2C%0A%20%20%22totalGB%22%3A%2026843545600%2C%0A%20%20%22expiryTime%22%3A%201769878433196%2C%0A%20%20%22enable%22%3A%20true%2C%0A%20%20%22tgId%22%3A%20%22%22%2C%0A%20%20%22subId%22%3A%20%228s1mmn9x9dzaf9v0%22%2C%0A%20%20%22comment%22%3A%20%22%22%2C%0A%20%20%22reset%22%3A%200%0A%7D%5D%7D"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'Origin': 'http://149.104.79.176:2053',
  'Connection': 'keep-alive',
  'Referer': 'http://149.104.79.176:2053/zAogYERqaVfe5qfCai/panel/inbounds',
  'Cookie': 'PHPSESSID=iv473ktmtgvaq6jtf52g6f9orh; lang=en-US; 3x-ui=MTc2OTYxNjc0NHxEWDhFQVFMX2dBQUJFQUVRQUFCbF80QUFBUVp6ZEhKcGJtY01EQUFLVEU5SFNVNWZWVk5GVWhoNExYVnBMMlJoZEdGaVlYTmxMMjF2WkdWc0xsVnpaWExfZ1FNQkFRUlZjMlZ5QWYtQ0FBRURBUUpKWkFFRUFBRUlWWE5sY201aGJXVUJEQUFCQ0ZCaGMzTjNiM0prQVF3QUFBQkpfNEpHQVFJQkEyRnljd0U4SkRKaEpERXdKRlV5YmpNd1VEbEpUemRvY1hZNWQzTlVlR2x2WkdWalJVVk5PRWsyVWs5dGRXdE5hRGxwZUZaeVVFUm5NSFI2ZHpOSFZWUjVBQT09fOzjezoFY9vDb1a62dVQ35dcokrZmbNKnAhkC_z9h7gb',
  'Priority': 'u=0',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
