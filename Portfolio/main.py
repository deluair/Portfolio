import sys
from simulation.simulation_engine import SimulationEngine
from analytics.visualization import SimulationVisualizer
import matplotlib.pyplot as plt

def main():
    print("🚀 Welcome to the Portfolio Wealth Simulation Platform!")
    print("📊 Running comprehensive simulation with advanced analytics and visualizations...")
    print("="*80)
    
    # Initialize simulation engine with more clients for better visualization
    engine = SimulationEngine(n_clients=50, n_periods=252)
    
    # Run the simulation
    engine.run()
    
    # Initialize visualizer
    visualizer = SimulationVisualizer()
    
    print("\n📈 Generating comprehensive visualizations...")
    print("="*80)
    
    # Create individual analysis plots
    print("1. Portfolio Performance Analysis...")
    visualizer.plot_portfolio_performance(engine.portfolio_history)
    
    print("2. Risk Metrics Analysis...")
    visualizer.plot_risk_metrics(engine.risk_metrics)
    
    print("3. ESG Analysis...")
    visualizer.plot_esg_analysis(engine.esg_scores)
    
    print("4. Behavioral Finance Analysis...")
    visualizer.plot_behavioral_analysis(engine.behavioral_impacts)
    
    print("5. Comprehensive Dashboard...")
    visualizer.plot_comprehensive_dashboard(
        engine.portfolio_history,
        engine.risk_metrics,
        engine.esg_scores,
        engine.behavioral_impacts
    )
    
    print("\n✅ Simulation and visualization complete!")
    print("📋 Check the generated charts above for detailed analysis.")
    print("="*80)
    
    # Print some key insights
    print("\n🔍 KEY INSIGHTS:")
    print("-"*40)
    
    # Portfolio insights
    final_values = [hist.iloc[-1] for hist in engine.portfolio_history]
    avg_final_value = sum(final_values) / len(final_values)
    best_performer = max(final_values)
    worst_performer = min(final_values)
    
    print(f"📈 Portfolio Performance:")
    print(f"   • Average final value: ${avg_final_value:,.2f}")
    print(f"   • Best performer: ${best_performer:,.2f}")
    print(f"   • Worst performer: ${worst_performer:,.2f}")
    print(f"   • Performance spread: {((best_performer/worst_performer - 1) * 100):.1f}%")
    
    # Risk insights
    avg_var = sum(rm['var_95'] for rm in engine.risk_metrics) / len(engine.risk_metrics)
    avg_vol = sum(rm['volatility'] for rm in engine.risk_metrics) / len(engine.risk_metrics)
    
    print(f"\n⚠️  Risk Analysis:")
    print(f"   • Average VaR (95%): {avg_var:.2%}")
    print(f"   • Average volatility: {avg_vol:.2%}")
    print(f"   • Risk-adjusted return: {(avg_final_value/1000 - 1 - 0.02) / avg_vol:.2f}")
    
    # ESG insights
    avg_esg = sum(esg['esg_score'] for esg in engine.esg_scores) / len(engine.esg_scores)
    high_esg_count = len([esg for esg in engine.esg_scores if esg['esg_score'] >= 70])
    
    print(f"\n🌱 ESG Performance:")
    print(f"   • Average ESG score: {avg_esg:.1f}")
    print(f"   • High ESG portfolios: {high_esg_count}/{len(engine.esg_scores)} ({high_esg_count/len(engine.esg_scores)*100:.1f}%)")
    
    # Behavioral insights
    avg_impact = sum(bi['behavioral_impact'] for bi in engine.behavioral_impacts) / len(engine.behavioral_impacts)
    total_decisions = sum(len(bi['trading_decisions']) for bi in engine.behavioral_impacts)
    
    print(f"\n🧠 Behavioral Finance:")
    print(f"   • Average behavioral impact: {avg_impact:.2%}")
    print(f"   • Total trading decisions: {total_decisions}")
    print(f"   • Decisions per client: {total_decisions/len(engine.clients):.1f}")
    
    print("\n" + "="*80)
    print("🎯 Simulation completed successfully!")
    print("📚 See wealth_simulation_prompt.md for full system requirements.")
    print("🔧 The platform is ready for further customization and analysis.")

if __name__ == "__main__":
    main() 