import requests
import json

def pin_to_ipfs(data):
	assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
	#YOUR CODE HERE

	url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
	api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxZDUyM2U5MS1mZjRjLTQyYmItOTc4MC1mNmFkOTNmNjRhOWYiLCJlbWFpbCI6ImRlbm5pc2tmaWdAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6Ijc4MTA1NzAxNjg0OTJjMzVkMjViIiwic2NvcGVkS2V5U2VjcmV0IjoiODBjOWNiMGEyZjI3YWQ1NmJiOTVjZjEyMWU4NTBkNWI4NDQ1NjMwZDI5YThiNWM0ZjYwNzY3YjUzZjJkOTM2NiIsImlhdCI6MTcxOTg4NDg5OX0.r_q5X0rjNmDWH2R8xFl8_zBXNkpw8AFtxxXdlz7794A"
	headers = {
		"Authorization": f"Bearer {api_key}"
		}

	response = requests.posts(url, json=data, headers=headers )
	cid = response.json().get('IpfsHash')

	return cid

def get_from_ipfs(cid,content_type="json"):
	assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
	url = f"https://gateway.pinata.cloud/ipfs/{cid}"

	try:
		response = requests.get(url)
		response.raise_for_status()
		if content_type.lower() == "json":
			data = response.json()
		else:
			raise ValueError("It is required to be of type JSON.")
		assert isinstance(data, dict), f"get_from_ipfs should return a dict"
	except requests.exceptions.RequestException as e:
		print(f"Issue happened while retreiving from IFPS: {e}")
		return None
	return data
