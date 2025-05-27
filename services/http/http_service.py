import httpx


async def http_get(
  client: httpx.AsyncClient, url: str, params: dict = None, headers: dict = None
) -> dict:
  """
  Perform a GET request to the specified URL with optional parameters.

  Args:
      url (str): The URL to send the GET request to.
      params (dict, optional): Optional parameters to include in the request.
      headers (dict, optional): Optional headers to include in the request.
          Defaults to None.
  Returns:
      dict: The JSON response from the API.

  Raises:
      Exception: If the request fails or if the response is not valid JSON.
  """
  try:
    response = await client.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses

    if response.status_code != 200:
      print(f"[!] HTTP GET request failed with status code: {response.status_code}")
      raise Exception("Invalid response from the server")

    return response.json()
  except Exception as e:
    print(f"[!] HTTP GET request failed: {e}")
    raise
