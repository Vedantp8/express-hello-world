import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website to scrape
main_url = 'https://unsobered.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

def scrape_data():
    # Send a GET request to the main URL
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract links for different sections: cities, types of drinks, and events
    city_section = soup.find('a', class_="elementor-item", string="In Your City")
    city_links = city_section.find_next('ul').find_all('a', class_="elementor-sub-item")

    type_section = soup.find('a', class_="elementor-item", string="Know Your Booze")
    type_links = type_section.find_next('ul').find_all('a', class_="elementor-sub-item")

    event_section = soup.find('a', class_='elementor-item', string='Events')
    event_href = event_section.get('href')
    print("Event Href:", event_href)

    all_data = []

    # Get drink data for each type
    for link in type_links:
        href = link.get('href')
        drink_name = link.text.strip()
        print("Drink:", drink_name, href)

        drink_data = get_href_data(href)  # Fetch drink-specific data
        all_data.extend(drink_data)  # Add to the overall data list

    # Get city data for each city
    for link in city_links:
        href = link.get('href')
        city_name = link.text.strip()
        print("City:", city_name, href)

        city_data = get_href_data(href)  # Fetch city-specific data
        all_data.extend(city_data)  # Add to the overall data list

    # Get event-specific data
    event_data = get_href_data(event_href)
    all_data.extend(event_data)  # Add to the overall data list

    # Remove duplicates by link
    unique_data = {item['link']: item for item in all_data if item['link']} 
    all_data = list(unique_data.values()) 
    
    # Save the scraped data to a JSON file
    with open('./jsonData/scraped_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)
        print("Doc saved successfully")

def get_href_data(url):
    all_data = get_card_data(url)  # Get initial card data from the URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for pagination links
    pagination_nav = soup.find('nav', class_='elementor-pagination')
    if pagination_nav:
        pagination_links = pagination_nav.find_all('a')  # Get all pagination links
        
        # Fetch data for each pagination link
        for link in pagination_links:
            href = link['href']
            all_data.extend(get_card_data(href))  # Add card data from each pagination link

    return all_data  

def get_card_data(url):
    # Fetch data from a specific card URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts_container = soup.find('div', class_='elementor-posts-container')

    data_list = []  # List to store data from articles

    if posts_container:
        articles = posts_container.find_all('article', class_='elementor-post')  # Find all articles
        
        for article in articles:
            # Extract tags and categories from article classes
            classes = article.get('class', [])
            tag_classes = [cls.replace('tag-', '') for cls in classes if cls.startswith('tag')]
            category_classes = [cls.replace('category-', '') for cls in classes if cls.startswith('category')]
            
            # Extract title and link of the article
            title_link = article.find('h3', class_='elementor-post__title').find('a')
            if title_link:
                title_href = title_link['href']
                title_text = title_link.text.strip()
            else:
                title_href = None
                title_text = None
            
            # Extract post date
            date_span = article.find('span', class_='elementor-post-date')
            post_date = date_span.text.strip() if date_span else None
            
            # Store article data in a dictionary
            article_data = {
                'title': title_text,
                'tags': tag_classes,
                'category': category_classes,
                'date': post_date,
                'link': title_href
            }
            data_list.append(article_data)  # Add article data to the list

    return data_list  

scrape_data()  # Start the scraping process
