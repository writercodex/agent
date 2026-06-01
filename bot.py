from ai import chat_with_ai

print("STEP 1")

try:

    print("STEP 2")

    reply = chat_with_ai("Halo")

    print("STEP 3")

    print(reply)

except Exception as e:

    print("ERROR:")

    print(str(e))
