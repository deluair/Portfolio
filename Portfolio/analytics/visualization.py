import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SimulationVisualizer:
    def __init__(self, figsize=(15, 10)):
        self.figsize = figsize
    
    def plot_portfolio_performance(self, portfolio_history: List[pd.Series], 
                                 save_path: str = None) -> None:
        """Plot portfolio value evolution over time"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # Plot individual portfolio paths
        for i, portfolio in enumerate(portfolio_history):
            ax1.plot(portfolio.index, portfolio.values, alpha=0.7, linewidth=1)
        
        ax1.set_title('Portfolio Value Evolution - All Clients', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Time Period')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.grid(True, alpha=0.3)
        
        # Plot average portfolio performance
        portfolio_df = pd.concat(portfolio_history, axis=1)
        mean_portfolio = portfolio_df.mean(axis=1)
        std_portfolio = portfolio_df.std(axis=1)
        
        ax2.plot(mean_portfolio.index, mean_portfolio.values, 'b-', linewidth=3, label='Average Portfolio')
        ax2.fill_between(mean_portfolio.index, 
                        mean_portfolio.values - std_portfolio.values,
                        mean_portfolio.values + std_portfolio.values,
                        alpha=0.3, color='blue', label='±1 Std Dev')
        
        ax2.set_title('Average Portfolio Performance with Standard Deviation', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Time Period')
        ax2.set_ylabel('Portfolio Value ($)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_risk_metrics(self, risk_metrics: List[Dict], save_path: str = None) -> None:
        """Plot risk metrics distribution"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Extract metrics
        var_values = [rm['var_95'] for rm in risk_metrics]
        cvar_values = [rm['cvar_95'] for rm in risk_metrics]
        vol_values = [rm['volatility'] for rm in risk_metrics]
        
        # VaR distribution
        axes[0, 0].hist(var_values, bins=20, alpha=0.7, color='red', edgecolor='black')
        axes[0, 0].set_title('VaR (95%) Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('VaR Value')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].axvline(np.mean(var_values), color='red', linestyle='--', 
                          label=f'Mean: {np.mean(var_values):.3f}')
        axes[0, 0].legend()
        
        # CVaR distribution
        axes[0, 1].hist(cvar_values, bins=20, alpha=0.7, color='orange', edgecolor='black')
        axes[0, 1].set_title('CVaR (95%) Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('CVaR Value')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].axvline(np.mean(cvar_values), color='orange', linestyle='--',
                          label=f'Mean: {np.mean(cvar_values):.3f}')
        axes[0, 1].legend()
        
        # Volatility distribution
        axes[1, 0].hist(vol_values, bins=20, alpha=0.7, color='green', edgecolor='black')
        axes[1, 0].set_title('Volatility Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Volatility')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].axvline(np.mean(vol_values), color='green', linestyle='--',
                          label=f'Mean: {np.mean(vol_values):.3f}')
        axes[1, 0].legend()
        
        # Risk scatter plot
        axes[1, 1].scatter(vol_values, var_values, alpha=0.6, color='purple')
        axes[1, 1].set_title('Volatility vs VaR', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Volatility')
        axes[1, 1].set_ylabel('VaR (95%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_esg_analysis(self, esg_scores: List[Dict], save_path: str = None) -> None:
        """Plot ESG analysis results"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Extract ESG scores
        overall_scores = [esg['esg_score'] for esg in esg_scores]
        env_scores = [esg['environmental'] for esg in esg_scores]
        soc_scores = [esg['social'] for esg in esg_scores]
        gov_scores = [esg['governance'] for esg in esg_scores]
        
        # Overall ESG distribution
        axes[0, 0].hist(overall_scores, bins=20, alpha=0.7, color='green', edgecolor='black')
        axes[0, 0].set_title('Overall ESG Score Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('ESG Score')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].axvline(np.mean(overall_scores), color='green', linestyle='--',
                          label=f'Mean: {np.mean(overall_scores):.1f}')
        axes[0, 0].legend()
        
        # ESG components comparison
        components = ['Environmental', 'Social', 'Governance']
        component_means = [np.mean(env_scores), np.mean(soc_scores), np.mean(gov_scores)]
        
        bars = axes[0, 1].bar(components, component_means, 
                             color=['lightgreen', 'lightblue', 'lightcoral'], alpha=0.8)
        axes[0, 1].set_title('Average ESG Component Scores', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('Average Score')
        axes[0, 1].set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, value in zip(bars, component_means):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # ESG scatter plot
        axes[1, 0].scatter(env_scores, soc_scores, alpha=0.6, color='blue')
        axes[1, 0].set_title('Environmental vs Social Scores', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Environmental Score')
        axes[1, 0].set_ylabel('Social Score')
        axes[1, 0].grid(True, alpha=0.3)
        
        # ESG rating distribution
        ratings = []
        for score in overall_scores:
            if score >= 80:
                ratings.append('AAA')
            elif score >= 70:
                ratings.append('AA')
            elif score >= 60:
                ratings.append('A')
            elif score >= 50:
                ratings.append('BBB')
            elif score >= 40:
                ratings.append('BB')
            else:
                ratings.append('B')
        
        rating_counts = pd.Series(ratings).value_counts()
        axes[1, 1].pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%',
                      startangle=90, colors=plt.cm.Set3(np.linspace(0, 1, len(rating_counts))))
        axes[1, 1].set_title('ESG Rating Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_behavioral_analysis(self, behavioral_impacts: List[Dict], save_path: str = None) -> None:
        """Plot behavioral finance analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Behavioral impact distribution
        impacts = [bi['behavioral_impact'] for bi in behavioral_impacts]
        axes[0, 0].hist(impacts, bins=20, alpha=0.7, color='purple', edgecolor='black')
        axes[0, 0].set_title('Behavioral Impact Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Behavioral Impact')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].axvline(np.mean(impacts), color='purple', linestyle='--',
                          label=f'Mean: {np.mean(impacts):.3f}')
        axes[0, 0].legend()
        
        # Trading decisions analysis
        all_decisions = []
        for bi in behavioral_impacts:
            for decision in bi['trading_decisions']:
                all_decisions.append(decision['action'])
        
        decision_counts = pd.Series(all_decisions).value_counts()
        bars = axes[0, 1].bar(decision_counts.index, decision_counts.values,
                             color=['lightgreen', 'lightcoral', 'lightblue'], alpha=0.8)
        axes[0, 1].set_title('Trading Decisions by Behavioral Bias', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('Count')
        
        # Add value labels on bars
        for bar, value in zip(bars, decision_counts.values):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                           str(value), ha='center', va='bottom', fontweight='bold')
        
        # Bias strength analysis
        bias_strengths = []
        bias_types = []
        for bi in behavioral_impacts:
            for decision in bi['trading_decisions']:
                bias_strengths.append(decision['strength'])
                bias_types.append(decision['bias'])
        
        bias_df = pd.DataFrame({'Bias': bias_types, 'Strength': bias_strengths})
        bias_means = bias_df.groupby('Bias')['Strength'].mean()
        
        bars = axes[1, 0].bar(bias_means.index, bias_means.values,
                             color=plt.cm.Set3(np.linspace(0, 1, len(bias_means))), alpha=0.8)
        axes[1, 0].set_title('Average Bias Strength by Type', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('Average Strength')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, bias_means.values):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # Impact vs strength scatter
        impact_strength_data = []
        for bi in behavioral_impacts:
            for decision in bi['trading_decisions']:
                impact_strength_data.append({
                    'impact': bi['behavioral_impact'],
                    'strength': decision['strength']
                })
        
        if impact_strength_data:
            impact_df = pd.DataFrame(impact_strength_data)
            axes[1, 1].scatter(impact_df['strength'], impact_df['impact'], alpha=0.6, color='orange')
            axes[1, 1].set_title('Behavioral Impact vs Bias Strength', fontsize=14, fontweight='bold')
            axes[1, 1].set_xlabel('Bias Strength')
            axes[1, 1].set_ylabel('Behavioral Impact')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_comprehensive_dashboard(self, portfolio_history: List[pd.Series],
                                   risk_metrics: List[Dict],
                                   esg_scores: List[Dict],
                                   behavioral_impacts: List[Dict],
                                   save_path: str = None) -> None:
        """Create a comprehensive dashboard with all metrics"""
        fig = plt.figure(figsize=(20, 16))
        
        # Create grid layout
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Portfolio performance (top row, full width)
        ax1 = fig.add_subplot(gs[0, :2])
        portfolio_df = pd.concat(portfolio_history, axis=1)
        mean_portfolio = portfolio_df.mean(axis=1)
        ax1.plot(mean_portfolio.index, mean_portfolio.values, 'b-', linewidth=2)
        ax1.set_title('Average Portfolio Performance', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Time Period')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.grid(True, alpha=0.3)
        
        # Risk metrics summary
        ax2 = fig.add_subplot(gs[0, 2:])
        var_values = [rm['var_95'] for rm in risk_metrics]
        vol_values = [rm['volatility'] for rm in risk_metrics]
        ax2.scatter(vol_values, var_values, alpha=0.6, color='red')
        ax2.set_title('Risk Profile: Volatility vs VaR', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Volatility')
        ax2.set_ylabel('VaR (95%)')
        ax2.grid(True, alpha=0.3)
        
        # ESG scores
        ax3 = fig.add_subplot(gs[1, :2])
        overall_scores = [esg['esg_score'] for esg in esg_scores]
        ax3.hist(overall_scores, bins=15, alpha=0.7, color='green', edgecolor='black')
        ax3.set_title('ESG Score Distribution', fontsize=14, fontweight='bold')
        ax3.set_xlabel('ESG Score')
        ax3.set_ylabel('Frequency')
        ax3.axvline(np.mean(overall_scores), color='red', linestyle='--',
                   label=f'Mean: {np.mean(overall_scores):.1f}')
        ax3.legend()
        
        # Behavioral impacts
        ax4 = fig.add_subplot(gs[1, 2:])
        impacts = [bi['behavioral_impact'] for bi in behavioral_impacts]
        ax4.hist(impacts, bins=15, alpha=0.7, color='purple', edgecolor='black')
        ax4.set_title('Behavioral Impact Distribution', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Behavioral Impact')
        ax4.set_ylabel('Frequency')
        ax4.axvline(np.mean(impacts), color='red', linestyle='--',
                   label=f'Mean: {np.mean(impacts):.3f}')
        ax4.legend()
        
        # Summary statistics
        ax5 = fig.add_subplot(gs[2:, :])
        ax5.axis('off')
        
        # Calculate summary statistics
        final_values = [hist.iloc[-1] for hist in portfolio_history]
        avg_final_value = np.mean(final_values)
        avg_var = np.mean(var_values)
        avg_vol = np.mean(vol_values)
        avg_esg = np.mean(overall_scores)
        avg_impact = np.mean(impacts)
        
        summary_text = f"""
        COMPREHENSIVE SIMULATION SUMMARY
        
        Portfolio Performance:
        • Average Final Value: ${avg_final_value:,.2f}
        • Average VaR (95%): {avg_var:.2%}
        • Average Volatility: {avg_vol:.2%}
        
        ESG Analysis:
        • Average ESG Score: {avg_esg:.1f}
        • ESG Rating Distribution: {len([s for s in overall_scores if s >= 70])} High, {len([s for s in overall_scores if 50 <= s < 70])} Medium, {len([s for s in overall_scores if s < 50])} Low
        
        Behavioral Finance:
        • Average Behavioral Impact: {avg_impact:.2%}
        • Total Trading Decisions: {sum(len(bi['trading_decisions']) for bi in behavioral_impacts)}
        
        Risk-Return Profile:
        • Sharpe Ratio (estimated): {(avg_final_value/1000 - 1 - 0.02) / avg_vol:.2f}
        • Risk-Adjusted Performance: {'Good' if avg_esg > 70 and avg_impact < 0.01 else 'Needs Improvement'}
        """
        
        ax5.text(0.05, 0.95, summary_text, transform=ax5.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.suptitle('Wealth Management Simulation Dashboard', fontsize=20, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show() 