#!/usr/bin/env python3
"""
Script to fetch peer-reviewed studies from OpenPsychology Journal registry.
Retrieves a list of 10 peer-reviewed studies with their metadata.
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime


class OpenPsychologyJournalScraper:
    """Scraper for OpenPsychology Journal peer-reviewed studies."""
    
    BASE_URL = "https://openpsychologyjournal.com"
    API_ENDPOINT = f"{BASE_URL}/api/studies"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_peer_reviewed_studies(self, limit: int = 10) -> List[Dict]:
        """
        Fetch peer-reviewed studies from OpenPsychology Journal.
        
        Args:
            limit: Number of studies to fetch (default: 10)
            
        Returns:
            List of study dictionaries containing metadata
        """
        try:
            print(f"Fetching {limit} peer-reviewed studies from OpenPsychology Journal...")
            
            # Attempt to fetch from API endpoint
            params = {
                'filter': 'peer_reviewed',
                'status': 'published',
                'limit': limit,
                'sort': 'date_published:desc'
            }
            
            response = self.session.get(
                self.API_ENDPOINT,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                studies = response.json()
                return self._parse_studies(studies)
            else:
                print(f"API returned status code: {response.status_code}")
                return self._fetch_fallback(limit)
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from API: {e}")
            return self._fetch_fallback(limit)
    
    def _fetch_fallback(self, limit: int = 10) -> List[Dict]:
        """
        Fallback method to scrape studies from website.
        
        Args:
            limit: Number of studies to fetch
            
        Returns:
            List of study dictionaries
        """
        try:
            print("Using fallback: scraping website...")
            
            url = f"{self.BASE_URL}/studies"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # Parse HTML and extract studies
                studies = self._extract_studies_from_html(response.text, limit)
                return studies
            else:
                print(f"Website returned status code: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error in fallback method: {e}")
            return []
    
    def _parse_studies(self, data: Dict) -> List[Dict]:
        """
        Parse API response to extract study information.
        
        Args:
            data: Raw API response data
            
        Returns:
            List of parsed study dictionaries
        """
        studies = []
        
        items = data.get('studies', []) or data.get('items', []) or data.get('results', [])
        
        for study in items:
            parsed_study = {
                'id': study.get('id'),
                'title': study.get('title', 'N/A'),
                'authors': study.get('authors', []),
                'abstract': study.get('abstract', 'N/A'),
                'publication_date': study.get('publication_date') or study.get('date_published'),
                'peer_reviewed': True,
                'url': study.get('url') or f"{self.BASE_URL}/study/{study.get('id')}",
                'doi': study.get('doi', 'N/A'),
                'keywords': study.get('keywords', []),
                'citation_count': study.get('citation_count', 0)
            }
            studies.append(parsed_study)
        
        return studies
    
    def _extract_studies_from_html(self, html: str, limit: int) -> List[Dict]:
        """
        Extract study information from HTML content.
        
        Args:
            html: HTML content from website
            limit: Number of studies to extract
            
        Returns:
            List of extracted study dictionaries
        """
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html, 'html.parser')
            studies = []
            
            # Look for study containers (adjust selectors based on actual HTML structure)
            study_containers = soup.find_all('article', class_='study-item')[:limit]
            
            for idx, container in enumerate(study_containers, 1):
                study = {
                    'id': f"study_{idx}",
                    'title': container.find('h2') and container.find('h2').text.strip() or 'N/A',
                    'authors': [a.text.strip() for a in container.find_all('span', class_='author')],
                    'abstract': container.find('p', class_='abstract') and container.find('p', class_='abstract').text.strip() or 'N/A',
                    'publication_date': container.find('span', class_='date') and container.find('span', class_='date').text.strip() or 'N/A',
                    'peer_reviewed': True,
                    'url': container.find('a') and container.find('a').get('href') or 'N/A',
                    'doi': 'N/A',
                    'keywords': [tag.text.strip() for tag in container.find_all('span', class_='keyword')],
                    'citation_count': 0
                }
                studies.append(study)
            
            return studies
            
        except ImportError:
            print("BeautifulSoup4 not installed. Install with: pip install beautifulsoup4")
            return []
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return []
    
    def save_to_json(self, studies: List[Dict], filename: str = 'studies.json') -> None:
        """
        Save studies to JSON file.
        
        Args:
            studies: List of study dictionaries
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(studies, f, ensure_ascii=False, indent=2)
        print(f"Studies saved to {filename}")
    
    def print_studies(self, studies: List[Dict]) -> None:
        """
        Print studies in a readable format.
        
        Args:
            studies: List of study dictionaries
        """
        if not studies:
            print("No studies found.")
            return
        
        print(f"\n{'='*80}")
        print(f"Found {len(studies)} peer-reviewed studies")
        print(f"{'='*80}\n")
        
        for idx, study in enumerate(studies, 1):
            print(f"{idx}. {study.get('title', 'N/A')}")
            print(f"   Authors: {', '.join(study.get('authors', ['N/A']))}")
            print(f"   Publication Date: {study.get('publication_date', 'N/A')}")
            print(f"   DOI: {study.get('doi', 'N/A')}")
            print(f"   URL: {study.get('url', 'N/A')}")
            if study.get('keywords'):
                print(f"   Keywords: {', '.join(study.get('keywords', []))}")
            print(f"   Citation Count: {study.get('citation_count', 0)}")
            print()


def main():
    """Main execution function."""
    print("OpenPsychology Journal - Peer-Reviewed Studies Scraper")
    print("="*60)
    print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    scraper = OpenPsychologyJournalScraper()
    
    # Fetch 10 peer-reviewed studies
    studies = scraper.fetch_peer_reviewed_studies(limit=10)
    
    if studies:
        # Print to console
        scraper.print_studies(studies)
        
        # Save to JSON file
        scraper.save_to_json(studies, 'openpsychology_studies.json')
        
        print(f"\nSuccessfully fetched and saved {len(studies)} studies.")
    else:
        print("\nFailed to fetch studies. Please check:")
        print("1. Internet connection")
        print("2. OpenPsychology Journal website availability")
        print("3. Required dependencies (requests, beautifulsoup4)")


if __name__ == '__main__':
    main()
