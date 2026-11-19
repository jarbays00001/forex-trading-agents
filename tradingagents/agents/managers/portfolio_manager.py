"""Portfolio Manager: synthesises the risk-analyst debate."""

from __future__ import annotations

from tradingagents.agents.context import (
    get_instrument_context_from_state,
    get_language_instruction,
    get_portfolio_context_from_state,
)
from tradingagents.agents.rating import parse_rating
from tradingagents.agents.schemas import PortfolioDecision
from tradingagents.agents.structured import (
    NO_EXTERNAL_TOOLS,
    bind_structured,
    invoke_structured,
    render_pm_decision,
)

def create_portfolio_manager(llm):
    # PERBAIKAN: Menambahkan argumen ketiga "Portfolio Manager"
    structured_llm = bind_structured(llm, PortfolioDecision, "Portfolio Manager")

    def portfolio_manager_node(state) -> dict:
        instrument_context = get_instrument_context_from_state(state)
        portfolio_context = get_portfolio_context_from_state(state)

        history = state["risk_debate_state"]["history"]
        risk_debate_state = state["risk_debate_state"]
        research_plan = state["investment_plan"]
        trader_plan = state["trader_investment_plan"]

        past_context = state.get("past_context", "")
        lessons_line = (
            f"- Lessons from prior decisions and outcomes:\n{past_context}\n"
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
Write these sections, in this order, starting with the rating:
- **Rating**: exactly one of Buy / Overweight / Hold / Underweight / Sell
- **Executive Summary**: A brief summary of the decision.
- **Investment Thesis**: the evidence that decided it.

CRITICAL INSTRUCTION: 
1. First, determine the Trading Action (Rating: Buy, Sell, etc.).
2. For the Stop Loss calculation, you MUST use the ATR (Average True Range) value mentioned in the technical report. Use this formula:
   - If Action is Sell: Stop Loss = Entry Price + (1.5 * ATR)
   - If Action is Buy: Stop Loss = Entry Price - (1.5 * ATR)
3. You MUST explicitly extract and provide absolute values for these 4 fields in your structured output:
   - entry_price (e.g., 1.1050)
   - stop_loss (e.g., 1.1102)
   - take_profit (e.g., 1.0900)
   - position_size (e.g., 1.5%)

{NO_EXTERNAL_TOOLS}{get_language_instruction()}"""

        decision = invoke_structured(structured_llm, prompt)
        if decision is not None:
            final_trade_decision = render_pm_decision(decision)
            final_rating = decision.rating.value
        else:
            final_trade_decision = llm.invoke(prompt).content
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
