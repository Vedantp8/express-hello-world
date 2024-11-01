import requests
from bs4 import BeautifulSoup
import json

main_url = 'https://unsobered.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def scrape_data():
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract links for different sections
    city_section = soup.find('a', class_="elementor-item", string="In Your City")
    city_links = city_section.find_next('ul').find_all('a', class_="elementor-sub-item")

    type_section = soup.find('a', class_="elementor-item", string="Know Your Booze")
    type_links = type_section.find_next('ul').find_all('a', class_="elementor-sub-item")

    event_section = soup.find('a', class_='elementor-item', string='Events')
    event_href = event_section.get('href')
    print("Event Href:", event_href)

    all_data = []  # Initialize all_data list here

    # Loop through type links
    for link in type_links:
        href = link.get('href')
        drink_name = link.text.strip()
        print("Drink:", drink_name, href)

        # Get all data for this drink type
        drink_data = get_href_data(href)
        all_data.extend(drink_data)  # Collect data from the current drink type

    # Loop through city links
    for link in city_links:
        href = link.get('href')
        city_name = link.text.strip()
        print("City:", city_name, href)

        # Get all data for this city
        city_data = get_href_data(href)
        all_data.extend(city_data)  # Collect data from the current city

    # Get data for events
    event_data = get_href_data(event_href)
    all_data.extend(event_data)  # Collect data from events

    # Remove duplicates from all_data based on title or link
    unique_data = {item['link']: item for item in all_data if item['link']}  # Use link as a unique key
    all_data = list(unique_data.values())  # Convert back to list

    # Save all collected data to a JSON file after deduplication
    with open('./jsonData/scraped_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)
        print("Doc saved successfully")

def get_href_data(url):
    all_data = get_card_data(url)  # Get data from the initial page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination_nav = soup.find('nav', class_='elementor-pagination')

    if pagination_nav:
        pagination_links = pagination_nav.find_all('a')
        
        for link in pagination_links:
            href = link['href']
            # Extend all_data with the data collected from pagination links
            all_data.extend(get_card_data(href))  # Collect data from each pagination link

    return all_data  # Return the collected data for this section

def get_card_data(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts_container = soup.find('div', class_='elementor-posts-container')

    data_list = []  # List to store all articles' data

    if posts_container:
        articles = posts_container.find_all('article', class_='elementor-post')
        
        # Iterate over each article and extract the desired data
        for article in articles:
            classes = article.get('class', [])
            tag_classes = [cls.replace('tag-', '') for cls in classes if cls.startswith('tag')]
            category_classes = [cls.replace('category-', '') for cls in classes if cls.startswith('category')]
            
            # Extract title link and text
            title_link = article.find('h3', class_='elementor-post__title').find('a')
            if title_link:
                title_href = title_link['href']
                title_text = title_link.text.strip()
            else:
                title_href = None
                title_text = None
            
            # Extract the date
            date_span = article.find('span', class_='elementor-post-date')
            post_date = date_span.text.strip() if date_span else None
            
            # Create a dictionary for the article data
            article_data = {
                'title': title_text,
                'tags': tag_classes,
                'category': category_classes,
                'date': post_date,
                'link': title_href
            }
            data_list.append(article_data)  # Append the article data to the list

    return data_list  # Return the list of article data

scrape_data()
