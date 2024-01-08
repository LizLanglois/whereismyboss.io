import requests
from bs4 import BeautifulSoup
import folium

def scrape_website(url):
    # Define headers to simulate a request from a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element with the specified div id
        tracker_item_schedule_position = soup.find('div', id='trackerItemSchedulePosition')

        # Check if the element is found
        if tracker_item_schedule_position:
            # Extract and print the text content of the element
            position_text = tracker_item_schedule_position.get_text().strip()
            print(f"Tracker Item Schedule Position: {position_text}")

            # Extract only the coordinates from the text
            coordinates_start = position_text.find('coordinates') + len('coordinates')
            coordinates_end = position_text.find('en route to') if 'en route to' in position_text else None
            coordinates = position_text[coordinates_start:coordinates_end].strip()

            # Generate a map using folium
            generate_map(coordinates)
        else:
            print("Element with id 'trackerItemSchedulePosition' not found.")
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")

def generate_map(coordinates):
    # Format and extract latitude and longitude from the coordinates
    coordinates = coordinates.replace('N', '').replace('S', '').replace('E', '').replace('W', '')
    lat, lon = [float(coord.strip()) for coord in coordinates.split('/')]

    # Create a folium map centered around the provided latitude and longitude
    my_map = folium.Map(location=[lat, lon], zoom_start=10)

    # Add a marker to the map
    folium.Marker([lat, lon], popup='Current Position').add_to(my_map)

    # Save the map to an HTML file
    my_map.save('map.html')
    print("Map generated. Check the map.html file for the result.")

# Replace 'your_url_here' with the actual URL you want to scrape
url_to_scrape = 'https://www.cruisemapper.com/?imo=9156515'
scrape_website(url_to_scrape)
