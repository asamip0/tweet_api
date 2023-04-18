import json

# Sample JSON data
data = {
    
    "MerchantId": "16",
    "ApiUserName": "KhaltiFT",
    "Signature": "WD7p4tKKDS9AWkRw3HIfXUqAQtqK6NK57iAtul/pMhTIRVTC087KmZhDMVRi5FEBhmfoBBq4c1JYIbk8B1+DY5Stv5MHAFTQzC39XqLz5UH7QZztXcE7C/goXwjePUhA55sNerEpU5gF6miwJxDcBhz6LgnRfrJFk5bgP+d0XG6FQUI/jio6XpW9cvrRm2HWgWx3qboyCJ/EzYcst4AXKZSDP3YFx2ylMNi9hbNP/BjRObQ/vyJEmXmr5nIQ0tPdUkUYhcT8mbDd36b8ft36PZmvJLLI9lZ+phH3Yh6oLC2qEh3q3oiQDwzHjESljPM0aeucjOO+72OwF9095nkm7Q==",
    "TimeStamp": "2023-04-11T15:46:27.574",
    "MerchantTxnId": "test02"

}

# Sort the data in ascending order based on the keys
sorted_data = dict(sorted(data.items()))

# Print the sorted result
print(json.dumps(sorted_data, indent=4))
