import os

print("🛠️ Memulai Patch Bypass Pydantic...")
pm_path = "tradingagents/agents/managers/portfolio_manager.py"

if os.path.exists(pm_path):
    # Kita tulis ulang total file portfolio_manager.py
    new_code = '''"""Portfolio Manager: synthesises the risk-analyst debate."""

from __future__ import annotations

from tradingagents.agents.context import (
    get_instrument_context_from_state,
    get_language_instruction,
    get_portfolio_context_from_state,
)
from tradingagents.agents.rating import parse_rating
from tradingagents.agents.structured import NO_EXTERNAL_TOOLS

def create_portfolio_manager(llm):
    def portfolio_manager_node(state) -> dict:
        instrument_context = get_instrument_context_from_state(state)
        portfolio_context = get_portfolio_context_from_state(state)

        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        research_plan = state["investment_plan"]
        trader_plan = state["trader_investment_plan"]

        past_context = state.get("past_context", "")
        lessons_line = (
            f"- Lessons from prior decisions and outcomes:\\n{past_context}\\n"
            if past_context
            else ""
        )

        prompt = f"""As the Portfolio Manager, synthesize the debate and finalize the transaction proposal.

{instrument_context}

{portfolio_context}

---
**Rating Scale** (use exactly one):
- **Buy**: Strong conviction to enter or add to position
- **Overweight**: Favorable outlook, gradually increase exposure
- **Hold**: Maintain current position, no action needed
- **Underweight**: Reduce exposure, take partial profits
- **Sell**: Exit position or avoid entry

**Context:**
- Research Manager's investment plan: **{research_plan}**
- Trader's transaction proposal: **{trader_plan}**
{lessons_line}
**Risk Analysts Debate History:**
{history}

---
Ground every conclusion in specific evidence from the analysts.

## Output
Format your response EXACTLY as follows:

**Rating**: [Choose exactly one: Buy / Overweight / Hold / Underweight / Sell]

**Executive Summary**:
[Write a brief summary]

**Investment Thesis**:
| Parameter | Nilai / Keputusan |
| :--- | :--- |
| **Entry Price** | [absolute price] |
| **Stop Loss** | [absolute price] |
| **Take Profit** | [absolute price] |
| **Position Size** | [e.g., 1.5%] |

[Write the evidence that decided it here.]

{NO_EXTERNAL_TOOLS}{get_language_instruction()}"""

        # BYPASS PYDANTIC: Ambil teks mentah langsung dari AI
        response = llm.invoke(prompt)
        final_trade_decision = response.content
        
        # Baca rating dari teks
        final_rating = parse_rating(final_trade_decision)

        new_risk_debate_state = {
            "history": risk_debate_state["history"],
            "aggressive_history": risk_debate_state["aggressive_history"],
            "conservative_history": risk_debate_state["conservative_history"],
            "neutral_history": risk_debate_state["neutral_history"],
            "latest_speaker": "Judge",
            "current_aggressive_response": risk_debate_state["current_aggressive_response"],
            "current_conservative_response": risk_debate_state["current_conservative_response"],
            "current_neutral_response": risk_debate_state["current_neutral_response"],
            "count": risk_debate_state["count"],
        }
        
        return {
            "risk_debate_state": new_risk_debate_state,
            "final_trade_decision": final_trade_decision,
            "final_rating": final_rating,
        }

    return portfolio_manager_node
'''
    with open(pm_path, "w") as f:
        f.write(new_code)
    print("✅ portfolio_manager.py berhasil di-bypass (Full Overwrite).")
else:
    print("❌ File portfolio_manager.py tidak ditemukan!")

print("🎉 Patch selesai! Sekarang AI dipaksa mengeluarkan teks mentahnya.")
