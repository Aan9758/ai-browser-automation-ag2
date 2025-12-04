"""
Simple Browser AI Demo - Single File Version
"""

from playwright.sync_api import sync_playwright
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_plan(task: str) -> str:
    """Get AI to create a plan for the task"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a web browsing assistant. Create a simple step-by-step plan for this task."},
            {"role": "user", "content": task}
        ]
    )
    return response.choices[0].message.content


def extract_search_query(task: str) -> str:
    """Extract search query from task"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract the search query from this task. Return only the query, nothing else."},
            {"role": "user", "content": task}
        ]
    )
    return response.choices[0].message.content.strip()


def summarize_page(content: str) -> str:
    """Summarize page content"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this webpage content in 2-3 sentences."},
            {"role": "user", "content": content[:3000]}
        ]
    )
    return response.choices[0].message.content


def run_browser_agent(task: str):
    """Run the browser agent"""
    
    print(f"\n{'='*60}")
    print(f"🎯 TASK: {task}")
    print('='*60)
    
    # Get AI plan
    plan = get_ai_plan(task)
    print(f"\n📋 AI PLAN:\n{plan}\n")
    
    with sync_playwright() as p:
        print("🚀 Starting browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})
        
        # Determine what to do based on task
        task_lower = task.lower()
        
        if "google" in task_lower:
            query = extract_search_query(task)
            print(f"🌐 Opening Google...")
            page.goto("https://www.google.com")
            page.wait_for_timeout(2000)
            
            print(f"🔍 Searching: {query}")
            page.fill('textarea[name="q"]', query)
            page.press('textarea[name="q"]', "Enter")
            page.wait_for_timeout(3000)
            
        elif "wikipedia" in task_lower:
            query = extract_search_query(task)
            print(f"🌐 Opening Wikipedia...")
            page.goto("https://www.wikipedia.org")
            page.wait_for_timeout(2000)
            
            print(f"🔍 Searching: {query}")
            page.fill('input[name="search"]', query)
            page.press('input[name="search"]', "Enter")
            page.wait_for_timeout(3000)
            
        else:
            # Default: Google search
            query = extract_search_query(task)
            print(f"🌐 Opening Google...")
            page.goto("https://www.google.com")
            page.wait_for_timeout(2000)
            
            print(f"🔍 Searching: {query}")
            page.fill('textarea[name="q"]', query)
            page.press('textarea[name="q"]', "Enter")
            page.wait_for_timeout(3000)
        
        # Get results
        title = page.title()
        url = page.url
        
        print(f"\n📄 Page Title: {title}")
        print(f"🔗 URL: {url}")
        
        # Screenshot
        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
        
        # Get page summary
        try:
            content = page.evaluate("document.body.innerText")
            summary = summarize_page(content)
            print(f"\n📝 PAGE SUMMARY:\n{summary}")
        except Exception as e:
            print(f"Could not summarize: {e}")
        
        # Keep browser open to view
        print("\n⏳ Browser will close in 10 seconds...")
        page.wait_for_timeout(10000)
        
        browser.close()
        print("✅ Browser closed!")
    
    print(f"\n{'='*60}")
    print("✅ TASK COMPLETED!")
    print('='*60)


if __name__ == "__main__":
    # Example tasks - try different ones!
    tasks = [
        "Search Google for 'best Python web frameworks 2024'",
        # "Search Wikipedia for 'Artificial Intelligence'",
        # "Find information about machine learning on Google",
    ]
    
    for task in tasks:
        run_browser_agent(task)