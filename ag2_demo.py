"""
AG2 (AutoGen) Browser AI Demo
"""

import asyncio
from ag2_agents import AG2Orchestrator


async def main():
    print("\n" + "="*60)
    print("="*60)
    
    orchestrator = AG2Orchestrator(headless=False)
    
    task = "price of nifty 50 '"
    result = await orchestrator.execute_task(task)
    
    if result["success"]:
        print("\n✅ Task completed!")
    else:
        print(f"\n❌ Failed: {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())