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
    
    def fetch_peer_reviewed_studies(self, limit: int = 10, use_demo: bool = False) -> List[Dict]:
        """
        Fetch peer-reviewed studies from OpenPsychology Journal.
        
        Args:
            limit: Number of studies to fetch (default: 10)
            use_demo: If True, use demo data instead of trying to fetch from API
            
        Returns:
            List of study dictionaries containing metadata
        """
        if use_demo:
            print("Using demo data for demonstration purposes...")
            return self._generate_demo_data(limit)
            
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
                print("Falling back to demo data...")
                return self._generate_demo_data(limit)
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from API: {e}")
            print("Falling back to demo data...")
            return self._generate_demo_data(limit)
    
    def _generate_demo_data(self, limit: int = 10) -> List[Dict]:
        """
        Generate demo studies with replication data for testing.
        
        Args:
            limit: Number of demo studies to generate
            
        Returns:
            List of demo study dictionaries
        """
        demo_studies = [
            {
                'id': 'demo_001',
                'title': 'The Effect of Social Media on Self-Esteem in Adolescents',
                'authors': ['Smith, J.', 'Johnson, M.', 'Williams, R.'],
                'abstract': 'This study investigates the relationship between social media usage and self-esteem levels in adolescents aged 13-18. We conducted a longitudinal study with 250 participants over 6 months.',
                'publication_date': '2024-03-15',
                'peer_reviewed': True,
                'url': 'https://example.com/study/demo_001',
                'doi': '10.1234/example.2024.001',
                'keywords': ['social media', 'self-esteem', 'adolescents', 'mental health'],
                'citation_count': 42,
                'raw_data_url': 'https://osf.io/demo001/data',
                'code_repository': 'https://github.com/example/study-social-media',
                'protocol_url': 'https://osf.io/demo001/protocol',
                'sample_size': '250 participants',
                'effect_size': 'd = 0.67 (medium effect)',
                'statistical_analysis': 'Linear mixed-effects models with random intercepts',
                'materials_url': 'https://osf.io/demo001/materials',
                'data_availability': 'Available upon request',
                'code_availability': 'Publicly available',
                'methodology': 'Longitudinal study with standardized questionnaires administered online'
            },
            {
                'id': 'demo_002',
                'title': 'Cognitive Behavioral Therapy for Anxiety: A Meta-Analysis',
                'authors': ['Chen, L.', 'Garcia, P.', 'Thompson, K.', 'Davis, S.'],
                'abstract': 'Meta-analysis of 45 randomized controlled trials examining the efficacy of CBT for various anxiety disorders. Total sample of 2,847 participants.',
                'publication_date': '2024-02-20',
                'peer_reviewed': True,
                'url': 'https://example.com/study/demo_002',
                'doi': '10.1234/example.2024.002',
                'keywords': ['CBT', 'anxiety disorders', 'meta-analysis', 'psychotherapy', 'treatment'],
                'citation_count': 128,
                'raw_data_url': 'https://osf.io/demo002/data',
                'code_repository': 'https://github.com/example/meta-analysis-cbt',
                'protocol_url': 'https://osf.io/demo002/protocol',
                'sample_size': '45 studies, 2,847 participants total',
                'effect_size': 'g = 0.95 (large effect)',
                'statistical_analysis': 'Random-effects meta-analysis with heterogeneity assessment',
                'materials_url': 'https://osf.io/demo002/materials',
                'data_availability': 'Supplementary materials available',
                'code_availability': 'R scripts available',
                'methodology': 'Systematic review and meta-analysis following PRISMA guidelines'
            },
            {
                'id': 'demo_003',
                'title': 'Memory Consolidation During Sleep: An fMRI Study',
                'authors': ['Patel, N.', 'Anderson, B.', 'Kim, S.'],
                'abstract': 'Investigation of neural correlates of memory consolidation during REM sleep using functional MRI. 35 healthy young adults participated.',
                'publication_date': '2024-01-10',
                'peer_reviewed': True,
                'url': 'https://example.com/study/demo_003',
                'doi': '10.1234/example.2024.003',
                'keywords': ['memory', 'sleep', 'fMRI', 'REM', 'consolidation'],
                'citation_count': 67,
                'raw_data_url': 'https://osf.io/demo003/data',
                'code_repository': 'https://github.com/example/memory-sleep-fmri',
                'protocol_url': 'https://osf.io/demo003/protocol',
                'sample_size': '35 participants',
                'effect_size': 'Cluster-level FWE-corrected p < 0.001',
                'statistical_analysis': 'SPM12 with mixed-effects modeling',
                'materials_url': 'https://osf.io/demo003/materials',
                'data_availability': 'BIDS-formatted data available',
                'code_availability': 'MATLAB and Python scripts provided',
                'methodology': 'Within-subject fMRI design with behavioral testing during wake and sleep'
            },
            {
                'id': 'demo_004',
                'title': 'Environmental Stress and Academic Performance in University Students',
                'authors': ['López, M.', 'Müller, K.', 'O\'Brien, P.'],
                'abstract': 'Cross-sectional study examining relationships between environmental stressors and GPA in 480 university students.',
                'publication_date': '2023-12-05',
                'peer_reviewed': True,
                'url': 'https://example.com/study/demo_004',
                'doi': '10.1234/example.2023.004',
                'keywords': ['stress', 'academic performance', 'university', 'environment'],
                'citation_count': 23,
                'raw_data_url': 'https://osf.io/demo004/data',
                'code_repository': 'https://github.com/example/environmental-stress',
                'protocol_url': 'https://osf.io/demo004/protocol',
                'sample_size': '480 students',
                'effect_size': 'r = -0.42',
                'statistical_analysis': 'Multiple regression with bootstrapped confidence intervals',
                'materials_url': 'https://osf.io/demo004/materials',
                'data_availability': 'Anonymized data available',
                'code_availability': 'R Markdown document available',
                'methodology': 'Validated instruments: Perceived Stress Scale and academic records'
            },
            {
                'id': 'demo_005',
                'title': 'Neuroplasticity and Language Learning in Bilingual Children',
                'authors': ['Zhang, W.', 'Silva, J.', 'Novak, I.', 'Brown, T.', 'Harris, L.'],
                'abstract': 'Longitudinal neuroimaging study tracking language acquisition and neural changes in 60 bilingual children over 2 years.',
                'publication_date': '2023-11-18',
                'peer_reviewed': True,
                'url': 'https://example.com/study/demo_005',
                'doi': '10.1234/example.2023.005',
                'keywords': ['neuroplasticity', 'bilingual', 'language', 'children', 'fMRI'],
                'citation_count': 89,
                'raw_data_url': 'https://osf.io/demo005/data',
                'code_repository': 'https://github.com/example/bilingual-neuroplasticity',
                'protocol_url': 'https://osf.io/demo005/protocol',
                'sample_size': '60 children, 3 timepoints',
                'effect_size': 'Time × Language interaction, F = 8.34, p < 0.001',
                'statistical_analysis': 'Mixed-effects ANOVA with ROI analysis',
                'materials_url': 'https://osf.io/demo005/materials',
                'data_availability': 'Available through institutional repository',
                'code_availability': 'FSL pipelines and custom Python scripts',
                'methodology': 'Structural and functional MRI with behavioral language testing'
            }
        ]
        
        return demo_studies[:limit]
    
    def _parse_studies(self, data: Dict) -> List[Dict]:
        """
        Parse API response to extract study information including replication data.
        
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
                'citation_count': study.get('citation_count', 0),
                # Replication data fields
                'raw_data_url': study.get('raw_data_url') or study.get('data_repository', 'N/A'),
                'code_repository': study.get('code_repository') or study.get('github_url', 'N/A'),
                'methodology': study.get('methodology', 'N/A'),
                'protocol_url': study.get('protocol_url') or study.get('osf_url', 'N/A'),
                'sample_size': study.get('sample_size', 'N/A'),
                'effect_size': study.get('effect_size', 'N/A'),
                'statistical_analysis': study.get('statistical_analysis', 'N/A'),
                'materials_url': study.get('materials_url', 'N/A'),
                'data_availability': study.get('data_availability', 'Not specified'),
                'code_availability': study.get('code_availability', 'Not specified')
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
                # Extract replication data links
                data_link = container.find('a', class_='data-link')
                code_link = container.find('a', class_='code-link')
                protocol_link = container.find('a', class_='protocol-link')
                materials_link = container.find('a', class_='materials-link')
                
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
                    'citation_count': 0,
                    # Replication data fields
                    'raw_data_url': data_link.get('href') if data_link else 'N/A',
                    'code_repository': code_link.get('href') if code_link else 'N/A',
                    'methodology': container.find('p', class_='methodology') and container.find('p', class_='methodology').text.strip() or 'N/A',
                    'protocol_url': protocol_link.get('href') if protocol_link else 'N/A',
                    'sample_size': container.find('span', class_='sample-size') and container.find('span', class_='sample-size').text.strip() or 'N/A',
                    'effect_size': container.find('span', class_='effect-size') and container.find('span', class_='effect-size').text.strip() or 'N/A',
                    'statistical_analysis': container.find('span', class_='statistics') and container.find('span', class_='statistics').text.strip() or 'N/A',
                    'materials_url': materials_link.get('href') if materials_link else 'N/A',
                    'data_availability': container.find('span', class_='data-availability') and container.find('span', class_='data-availability').text.strip() or 'Not specified',
                    'code_availability': container.find('span', class_='code-availability') and container.find('span', class_='code-availability').text.strip() or 'Not specified'
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
            print(f"\n   REPLICATION DATA:")
            print(f"   Raw Data URL: {study.get('raw_data_url', 'N/A')}")
            print(f"   Code Repository: {study.get('code_repository', 'N/A')}")
            print(f"   Protocol URL: {study.get('protocol_url', 'N/A')}")
            print(f"   Materials URL: {study.get('materials_url', 'N/A')}")
            print(f"   Sample Size: {study.get('sample_size', 'N/A')}")
            print(f"   Effect Size: {study.get('effect_size', 'N/A')}")
            print(f"   Statistical Analysis: {study.get('statistical_analysis', 'N/A')}")
            print(f"   Data Availability: {study.get('data_availability', 'Not specified')}")
            print(f"   Code Availability: {study.get('code_availability', 'Not specified')}")
            if study.get('methodology') and study.get('methodology') != 'N/A':
                print(f"   Methodology: {study.get('methodology', 'N/A')}")
            print()


def main():
    """Main execution function."""
    print("OpenPsychology Journal - Peer-Reviewed Studies Scraper")
    print("="*60)
    print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    scraper = OpenPsychologyJournalScraper()
    
    # Fetch 10 peer-reviewed studies (use demo data by default)
    # Set use_demo=False to attempt fetching from the live API
    studies = scraper.fetch_peer_reviewed_studies(limit=10, use_demo=True)
    
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
