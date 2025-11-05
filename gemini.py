# ===============================================================
# gemini.py — Iron Core Fitness Predictive Analytics Assistant
# ===============================================================

import os
import google.genai as genai
from dotenv import load_dotenv

# ---------------------------------------------------------------
# 1. Load environment and configure Gemini client
# ---------------------------------------------------------------
load_dotenv()  # Automatically load GEMINI_API_KEY from .env

def get_client():
    """Initialize and return Gemini client."""
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY. Please check your .env file or environment variables.")

    genai.configure(api_key=api_key)
    return genai


# ---------------------------------------------------------------
# 2. Chat with knowledge base (main assistant logic)
# ---------------------------------------------------------------
def chat_with_knowledge_base(user_question: str, knowledge_base: str, chat_history: list = None) -> str:
    """
    Chat with AI using the knowledge base as context.
    Produces clear, factual, and data-grounded insights.
    """
    system_prompt = f"""You are an expert AI assistant for Iron Core Fitness Company.
Your goal is to analyze business data and provide professional, actionable insights.

INSTRUCTIONS:
- Use ONLY the data and facts from the knowledge base provided.
- Give clear, confident, and structured responses.
- Always back up your answers with numbers, percentages, or metrics.
- Maintain a professional and readable tone suitable for business reports.

RESPONSE RULES:
1. Begin with a direct, one-sentence answer.
2. Follow with supporting figures and observations.
3. Use bullet points (with hyphens -) for clarity.
4. Avoid fluff — focus on insights and numbers.
5. Never use asterisks, markdown bold, or italics.
6. Always format money as $X,XXX.00 (two decimal places).
7. Format percentages with one decimal place (e.g., 43.5%).
8. If the question is not covered by the knowledge base, say:
   "I’m sorry, I can only answer questions based on the Iron Core Fitness dataset."

EXAMPLE RESPONSES:

Q: "What’s the total revenue?"
A: The total revenue is $4,100,000.00.  
- This comes from 100 payment transactions  
- Average payment per client: $41,000.00  
- Revenue growth compared to last year: +12.4%

Q: "Which membership is most popular?"
A: Silver membership is the most popular, with 35 members.  
- Gold: 33 members  
- Platinum: 32 members  
- The distribution is balanced, indicating consistent appeal across tiers.

Q: "How can retention be improved?"
A: Current retention rate is 44% (44 of 100 members are active).  
- Identify reasons for 56 inactive members  
- Offer re-engagement incentives  
- Personalize programs to common goals  
- Track improvement monthly

KNOWLEDGE BASE:
{knowledge_base}
"""

    try:
        client = get_client()

        if chat_history is None:
            chat_history = []

        messages = [system_prompt] + chat_history[-10:] + [f"User Question: {user_question}"]
        full_prompt = "\n\n".join(messages)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config={
                "temperature": 0.25,
                "top_p": 0.9,
                "max_output_tokens": 1200,
            }
        )

        return response.text.strip() if response.text else "I couldn’t generate a response. Please try again."

    except Exception as e:
        return f"Error: {str(e)}"


# ---------------------------------------------------------------
# 3. Comprehensive business insights report generator
# ---------------------------------------------------------------
def generate_comprehensive_report(knowledge_base: str) -> str:
    """
    Generate a structured, professional business insights report.
    """
    prompt = f"""You are Francis Afful Gyan, Business Intelligence Specialist for Iron Core Fitness.
Generate a complete professional business report (dated 25 October 2025) using ONLY the data provided below.

KNOWLEDGE BASE:
{knowledge_base}

FORMAT THE REPORT AS FOLLOWS:

# IRON CORE FITNESS BUSINESS INSIGHTS REPORT
Date: 25 October 2025
Prepared by: Francis Afful Gyan, Business Intelligence Specialist

## 1. Executive Summary
- Brief overview of company performance and key findings
- Highlight major insights and data-driven results

## 2. Financial Performance Analysis
- Total revenue, expenses, and net profit (exact values)
- Profit margin percentage
- Notable trends and growth rates
- Overall financial health assessment

## 3. Client Analytics and Demographics
- Active vs inactive members
- Age range and average BMI
- Gender distribution
- Common fitness goals and behavioral insights

## 4. Membership Performance
- Distribution by tier (Platinum, Gold, Silver)
- Membership retention and churn analysis
- Lifetime value comparison across tiers

## 5. Payment and Revenue Trends
- Payment method breakdown
- Payment completion rate
- Average transaction value
- Revenue optimization recommendations

## 6. Expense Analysis
- Expense categories and their shares
- Top cost drivers
- Opportunities for cost efficiency

## 7. Trainer Performance
- Number of active trainers
- Trainer-to-client ratio
- Trainer effectiveness and utilization rates

## 8. Challenges and Opportunities
- Data-backed challenges affecting performance
- Areas with strong potential for growth

## 9. Strategic Recommendations
- 5–7 actionable recommendations with expected impact
- Include measurable KPIs for tracking results

STYLE RULES:
- Use clear markdown headings (#, ##)
- Use bullet points with hyphens (-)
- No asterisks, bold, or italics
- Keep the tone businesslike, factual, and insight-focused
- Use formatted currency and percentages consistently
"""

    try:
        client = get_client()

        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config={
                "temperature": 0.35,
                "top_p": 0.9,
                "max_output_tokens": 8192,
            }
        )

        return response.text.strip() if response.text else "Unable to generate report."

    except Exception as e:
        return f"Error generating report: {str(e)}"
