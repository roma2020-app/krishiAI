from krishi_ai.router import IntelligentRouter
from krishi_ai.call_adk import ask_adk

router = IntelligentRouter()

print("=" * 60)
print("🌾 KRISHI AI")
print("=" * 60)

while True:

    query = input("\n👨‍🌾 Farmer: ").strip()

    if query.lower() in ["exit", "quit"]:
        break

    result = router.route(query)

    route = result["route"]

    print(f"\n📌 Route : {route}")

    if route == "llm":

        answer = ask_adk(query)

        print(answer)

    else:

        print(result["result"])