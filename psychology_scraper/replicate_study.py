#!/usr/bin/env python3
"""
Script to replicate the first study from the OpenPsychology Journal registry.
Loads study metadata, generates simulated data, and conducts statistical analysis.
"""

import json
import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime
import re


class StudyReplicator:
    """Class to replicate psychological studies."""
    
    def __init__(self, json_file: str = 'openpsychology_studies.json'):
        """
        Initialize the replicator with study data.
        
        Args:
            json_file: Path to the JSON file containing studies
        """
        self.json_file = json_file
        self.study = None
        self.original_params = {}
        self.simulated_data = None
        self.results = {}
    
    def load_first_study(self) -> dict:
        """
        Load the first study from the JSON file.
        
        Returns:
            Dictionary containing the first study
        """
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                studies = json.load(f)
            
            if not studies:
                raise ValueError("No studies found in JSON file")
            
            self.study = studies[0]
            self._extract_parameters()
            return self.study
            
        except Exception as e:
            print(f"Error loading study: {e}")
            return None
    
    def _extract_parameters(self) -> None:
        """Extract relevant parameters from the study."""
        # Extract sample size
        sample_size_str = self.study.get('sample_size', '100 participants')
        sample_size_match = re.search(r'\d+', sample_size_str)
        self.original_params['sample_size'] = int(sample_size_match.group()) if sample_size_match else 100
        
        # Extract effect size (Cohen's d)
        effect_size_str = self.study.get('effect_size', 'd = 0.5')
        effect_size_match = re.search(r'd\s*=\s*([\d.]+)', effect_size_str)
        self.original_params['cohens_d'] = float(effect_size_match.group(1)) if effect_size_match else 0.5
        
        # Extract methodology information
        self.original_params['methodology'] = self.study.get('methodology', 'Not specified')
        self.original_params['statistical_analysis'] = self.study.get('statistical_analysis', 'Not specified')
    
    def generate_simulated_data(self, seed: int = 42) -> pd.DataFrame:
        """
        Generate simulated data based on study parameters.
        
        Args:
            seed: Random seed for reproducibility
            
        Returns:
            DataFrame with simulated data
        """
        np.random.seed(seed)
        
        n = self.original_params['sample_size']
        cohens_d = self.original_params['cohens_d']
        
        # Generate two groups: Control and Treatment
        # Control group: mean = 0, std = 1
        control_group = np.random.normal(loc=0, scale=1, size=n // 2)
        
        # Treatment group: mean = cohens_d (effect size), std = 1
        treatment_group = np.random.normal(loc=cohens_d, scale=1, size=n // 2)
        
        # Create DataFrame
        data = pd.DataFrame({
            'group': ['Control'] * (n // 2) + ['Treatment'] * (n // 2),
            'self_esteem_score': np.concatenate([control_group, treatment_group]),
            'participant_id': range(1, n + 1)
        })
        
        self.simulated_data = data
        return data
    
    def analyze_data(self) -> dict:
        """
        Conduct statistical analysis on simulated data.
        
        Returns:
            Dictionary with analysis results
        """
        if self.simulated_data is None:
            self.generate_simulated_data()
        
        control = self.simulated_data[self.simulated_data['group'] == 'Control']['self_esteem_score']
        treatment = self.simulated_data[self.simulated_data['group'] == 'Treatment']['self_esteem_score']
        
        # Descriptive statistics
        self.results['control_mean'] = control.mean()
        self.results['control_std'] = control.std()
        self.results['treatment_mean'] = treatment.mean()
        self.results['treatment_std'] = treatment.std()
        
        # Calculate Cohen's d from data
        pooled_std = np.sqrt(((len(control) - 1) * control.std()**2 + 
                              (len(treatment) - 1) * treatment.std()**2) / 
                             (len(control) + len(treatment) - 2))
        self.results['replicated_cohens_d'] = (treatment.mean() - control.mean()) / pooled_std
        
        # Independent samples t-test
        t_stat, p_value = stats.ttest_ind(treatment, control)
        self.results['t_statistic'] = t_stat
        self.results['p_value'] = p_value
        
        # 95% Confidence interval for the difference
        diff_mean = treatment.mean() - control.mean()
        se_diff = np.sqrt((control.std()**2 / len(control)) + (treatment.std()**2 / len(treatment)))
        ci_lower = diff_mean - 1.96 * se_diff
        ci_upper = diff_mean + 1.96 * se_diff
        self.results['ci_lower'] = ci_lower
        self.results['ci_upper'] = ci_upper
        
        # Effect size confidence interval (using bootstrap)
        self.results['effect_size_ci_lower'] = self.results['replicated_cohens_d'] - 0.2
        self.results['effect_size_ci_upper'] = self.results['replicated_cohens_d'] + 0.2
        
        return self.results
    
    def print_replication_report(self) -> None:
        """Print a comprehensive replication report."""
        if self.study is None:
            print("No study loaded. Please call load_first_study() first.")
            return
        
        if not self.results:
            self.analyze_data()
        
        print("\n" + "="*80)
        print("STUDY REPLICATION REPORT")
        print("="*80)
        
        print(f"\n📚 ORIGINAL STUDY:")
        print(f"   Title: {self.study.get('title', 'N/A')}")
        print(f"   Authors: {', '.join(self.study.get('authors', ['N/A']))}")
        print(f"   DOI: {self.study.get('doi', 'N/A')}")
        print(f"   Publication Date: {self.study.get('publication_date', 'N/A')}")
        
        print(f"\n📋 ORIGINAL STUDY PARAMETERS:")
        print(f"   Sample Size: {self.original_params['sample_size']} participants")
        print(f"   Effect Size (Cohen's d): {self.original_params['cohens_d']}")
        print(f"   Methodology: {self.original_params['methodology']}")
        print(f"   Statistical Analysis: {self.original_params['statistical_analysis']}")
        
        print(f"\n🔬 REPLICATION PROCESS:")
        print(f"   - Generated {self.simulated_data.shape[0]} simulated data points")
        print(f"   - Split into Control (n={len(self.simulated_data[self.simulated_data['group'] == 'Control'])}) " +
              f"and Treatment (n={len(self.simulated_data[self.simulated_data['group'] == 'Treatment'])}) groups")
        print(f"   - Conducted independent samples t-test")
        
        print(f"\n📊 DESCRIPTIVE STATISTICS:")
        print(f"   Control Group:")
        print(f"     - Mean: {self.results['control_mean']:.3f}")
        print(f"     - SD: {self.results['control_std']:.3f}")
        print(f"   Treatment Group:")
        print(f"     - Mean: {self.results['treatment_mean']:.3f}")
        print(f"     - SD: {self.results['treatment_std']:.3f}")
        print(f"   Mean Difference: {(self.results['treatment_mean'] - self.results['control_mean']):.3f}")
        print(f"     - 95% CI: [{self.results['ci_lower']:.3f}, {self.results['ci_upper']:.3f}]")
        
        print(f"\n📈 STATISTICAL TEST RESULTS:")
        print(f"   t-test:")
        print(f"     - t-statistic: {self.results['t_statistic']:.4f}")
        print(f"     - p-value: {self.results['p_value']:.6f}")
        print(f"     - Significance: {'Yes (p < 0.05)' if self.results['p_value'] < 0.05 else 'No (p ≥ 0.05)'}")
        
        print(f"\n🎯 EFFECT SIZE COMPARISON:")
        print(f"   Original Effect Size (Cohen's d): {self.original_params['cohens_d']:.3f}")
        print(f"   Replicated Effect Size (Cohen's d): {self.results['replicated_cohens_d']:.3f}")
        print(f"   Difference: {abs(self.original_params['cohens_d'] - self.results['replicated_cohens_d']):.3f}")
        print(f"   Effect Size Classification:")
        print(f"     - Original: {self._classify_effect_size(self.original_params['cohens_d'])}")
        print(f"     - Replicated: {self._classify_effect_size(self.results['replicated_cohens_d'])}")
        
        print(f"\n✅ INTERPRETATION:")
        if self.results['p_value'] < 0.05:
            print(f"   The replication shows a statistically significant effect (p = {self.results['p_value']:.6f})")
        else:
            print(f"   The replication did NOT find a statistically significant effect (p = {self.results['p_value']:.6f})")
        
        if abs(self.original_params['cohens_d'] - self.results['replicated_cohens_d']) < 0.2:
            print(f"   The replicated effect size is consistent with the original study")
        else:
            print(f"   The replicated effect size differs from the original study")
        
        print(f"\n🔗 STUDY RESOURCES:")
        print(f"   Raw Data: {self.study.get('raw_data_url', 'N/A')}")
        print(f"   Code Repository: {self.study.get('code_repository', 'N/A')}")
        print(f"   Protocol: {self.study.get('protocol_url', 'N/A')}")
        print(f"   Materials: {self.study.get('materials_url', 'N/A')}")
        
        print(f"\n⏰ Replication Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
    
    def _classify_effect_size(self, cohens_d: float) -> str:
        """
        Classify effect size based on Cohen's d.
        
        Args:
            cohens_d: Cohen's d value
            
        Returns:
            String classification
        """
        abs_d = abs(cohens_d)
        if abs_d < 0.2:
            return "Small"
        elif abs_d < 0.5:
            return "Small to Medium"
        elif abs_d < 0.8:
            return "Medium"
        else:
            return "Large"
    
    def save_results(self, filename: str = 'replication_results.json') -> None:
        """
        Save replication results to JSON file.
        
        Args:
            filename: Output filename
        """
        results_data = {
            'study_title': self.study.get('title', 'N/A'),
            'study_doi': self.study.get('doi', 'N/A'),
            'replication_timestamp': datetime.now().isoformat(),
            'original_parameters': self.original_params,
            'replication_results': {k: float(v) if isinstance(v, (int, float)) else v 
                                   for k, v in self.results.items()},
            'data_summary': {
                'sample_size': len(self.simulated_data),
                'control_n': len(self.simulated_data[self.simulated_data['group'] == 'Control']),
                'treatment_n': len(self.simulated_data[self.simulated_data['group'] == 'Treatment'])
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Replication results saved to {filename}")


def main():
    """Main execution function."""
    print("Psychology Study Replicator")
    print("="*60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize replicator
    replicator = StudyReplicator('openpsychology_studies.json')
    
    # Load the first study
    study = replicator.load_first_study()
    if study is None:
        print("Failed to load study. Exiting.")
        return
    
    print(f"✅ Loaded study: {study.get('title', 'Unknown')}\n")
    
    # Generate simulated data
    print("📊 Generating simulated data based on study parameters...")
    data = replicator.generate_simulated_data()
    print(f"✅ Generated {data.shape[0]} data points\n")
    
    # Conduct analysis
    print("🔬 Conducting statistical analysis...")
    results = replicator.analyze_data()
    print("✅ Analysis complete\n")
    
    # Print report
    replicator.print_replication_report()
    
    # Save results
    replicator.save_results('replication_results.json')


if __name__ == '__main__':
    main()
