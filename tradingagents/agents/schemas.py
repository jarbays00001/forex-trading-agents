from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field

# --- ANALYST REPORTS ---

class MarketReport(BaseModel):
    trend: str = Field(description="The current trend of the market (e.g., bullish, bearish, neutral)")
    support_levels: list[str] = Field(description="Key support levels")
    resistance_levels: list[str] = Field(description="Key resistance levels")
    indicators: str = Field(description="Summary of technical indicators")
    summary: str = Field(description="Overall technical summary")

def render_market_report(report: MarketReport) -> str:
    parts = [
        f"**Trend**: {report.trend}",
        f"**Support Levels**: {', '.join(report.support_levels)}",
        f"**Resistance Levels**: {', '.join(report.resistance_levels)}",
        f"**Indicators**: {report.indicators}",
        f"**Summary**: {report.summary}"
    ]
    return "\n".join(parts)

class SentimentReport(BaseModel):
    overall_sentiment: str = Field(description="Overall market sentiment (e.g., bullish, bearish, neutral)")
    social_media_buzz: str = Field(description="Summary of social media sentiment")
    news_sentiment: str = Field(description="Summary of news sentiment")
    summary: str = Field(description="Overall sentiment summary")

def render_sentiment_report(report: SentimentReport) -> str:
    parts = [
        f"**Overall Sentiment**: {report.overall_sentiment}",
        f"**Social Media Buzz**: {report.social_media_buzz}",
        f"**News Sentiment**: {report.news_sentiment}",
        f"**Summary**: {report.summary}"
    ]
    return "\n".join(parts)

class NewsReport(BaseModel):
    key_events: list[str] = Field(description="Key news events impacting the asset")
    economic_indicators: str = Field(description="Relevant macroeconomic indicators")
    summary: str = Field(description="Overall news summary")

def render_news_report(report: NewsReport) -> str:
    parts = [
        f"**Key Events**: {', '.join(report.key_events)}",
        f"**Economic Indicators**: {report.economic_indicators}",
        f"**Summary**: {report.summary}"
    ]
    return "\n".join(parts)

class FundamentalsReport(BaseModel):
    valuation: str = Field(description="Valuation metrics")
    financial_health: str = Field(description="Financial health analysis")
    growth_outlook: str = Field(description="Growth outlook")
    summary: str = Field(description="Overall fundamental summary")

def render_fundamentals_report(report: FundamentalsReport) -> str:
    parts = [
        f"**Valuation**: {report.valuation}",
        f"**Financial Health**: {report.financial_health}",
        f"**Growth Outlook**: {report.growth_outlook}",
        f"**Summary**: {report.summary}"
    ]
    return "\n".join(parts)

# --- MANAGER DECISIONS ---

class TraderProposal(BaseModel):
    action: Literal["Buy", "Sell", "Hold"] = Field(description="The recommended trading action")
    reasoning: str = Field(description="The reasoning behind the action")
    entry_price: Optional[str] = Field(default=None, description="Suggested entry price")
    stop_loss: Optional[str] = Field(default=None, description="Suggested stop loss")
    take_profit: Optional[str] = Field(default=None, description="Suggested take profit")

def render_trader_proposal(proposal: TraderProposal) -> str:
    parts = [
        f"**Action**: {proposal.action}",
        f"**Reasoning**: {proposal.reasoning}"
    ]
    if proposal.entry_price:
        parts.append(f"**Entry Price**: {proposal.entry_price}")
    if proposal.stop_loss:
        parts.append(f"**Stop Loss**: {proposal.stop_loss}")
    if proposal.take_profit:
        parts.append(f"**Take Profit**: {proposal.take_profit}")
    return "\n".join(parts)

class PortfolioRating(str, Enum):
    BUY = "Buy"
    OVERWEIGHT = "Overweight"
    HOLD = "Hold"
    UNDERWEIGHT = "Underweight"
    SELL = "Sell"

class PortfolioDecision(BaseModel):
    rating: PortfolioRating = Field(description="Final portfolio rating")
    executive_summary: str = Field(description="Executive summary of the decision")
    investment_thesis: str = Field(description="Detailed investment thesis")
    price_target: Optional[str] = Field(default=None, description="Price target")
    time_horizon: Optional[str] = Field(default=None, description="Time horizon for the trade")
    
    # --- FIELD TAMBAHAN UNTUK SL/TP ---
    entry_price: Optional[str] = Field(default=None, description="The absolute entry price")
    stop_loss: Optional[str] = Field(default=None, description="The absolute stop loss price")
    take_profit: Optional[str] = Field(default=None, description="The absolute take profit price")
    position_size: Optional[str] = Field(default=None, description="The position size percentage")

def render_pm_decision(decision: PortfolioDecision) -> str:
    entry = getattr(decision, 'entry_price', None) or "N/A"
    sl = getattr(decision, 'stop_loss', None) or "N/A"
    tp = getattr(decision, 'take_profit', None) or decision.price_target or "N/A"
    size = getattr(decision, 'position_size', None) or "N/A"

    table = f"""| Parameter | Nilai / Keputusan |
| :--- | :--- |
| **Rating** | {decision.rating.value} |
| **Entry Price** | {entry} |
| **Stop Loss** | {sl} |
| **Take Profit** | {tp} |
| **Position Size** | {size} |"""

    return f"""{table}

**Executive Summary**:
{decision.executive_summary}

**Investment Thesis**:
{decision.investment_thesis}

**Time Horizon**: {decision.time_horizon or 'N/A'}"""
