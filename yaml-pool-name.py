import requests
import yaml
from concurrent.futures import ThreadPoolExecutor

def fetch_yaml_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching YAML file from {url}: {e}")
        return None

def parse_yaml(content):
    try:
        yaml_data = yaml.safe_load(content)
        if 'pool' in yaml_data:
            return yaml_data['pool']['name']
        else:
            return None
    except Exception as e:
        print(f"Error parsing YAML content: {e}")
        return None

def fetch_pool_names(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_yaml_file, urls)
        for url, result in zip(urls, results):
            if result:
                pool_name = parse_yaml(result)
                if pool_name:
                    print(f"Pool name for {url}: {pool_name}")

# Azure DevOps organization and project details
organization = 'your-organization'
project = 'your-project'

# Personal access token with appropriate permissions
token = 'your-personal-access-token'

# Azure DevOps repository details
repository = 'your-repository'

# Generate URLs for the YAML files
urls = [f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository}/items?recursionLevel=Full&includeContent=true&api-version=6.0-preview.1&path=/{path}&versionDescriptor.version=main' for path in range(1, 1001)]

# Fetch and parse YAML files to extract pool names
fetch_pool_names(urls)
