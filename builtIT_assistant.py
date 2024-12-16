from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("BuiltIT_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)


def create_thread():
    # Creation du Thread
    thread = client.beta.threads.create()
    my_thread_id = thread.id
    
    return my_thread_id

def update_thread(my_thread_id, ass_id, user_input):
    # Met a jour le thread avec les nouveau messages
    client.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=user_input
    )
    run = client.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=ass_id
    )
    return run.id, my_thread_id


def check_status(run_id, thread_id):
    # Verifie le status de la rÃ©ponse
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status

def interact_with_assistant(assistant_id):
    print("Start interacting with the assistant. Type 'exit' to quit.")
    my_thread_id = create_thread()
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Exiting the interaction. Goodbye!")
            client.beta.threads.delete(thread_id=my_thread_id)
            break
        # Create a thread and get the run ID
        my_run_id, my_thread_id = update_thread(my_thread_id, assistant_id, user_input)


        # Check the status of the response
        status = check_status(my_run_id, my_thread_id)
        while status != "completed":
            status = check_status(my_run_id, my_thread_id)

        # Retrieve the response
        response = client.beta.threads.messages.list(thread_id=my_thread_id)

        # Parse and print the assistant's response
        if response.data:
            for message in response.data:
                if message.role == "assistant":
                    # Extract the value from the TextContentBlock
                    assistant_reply = message.content[0].text.value
                    print("Assistant:", assistant_reply)
                    break
        else:
            print("No response received from the assistant.")


assistant_id = "asst_z7Ae71fbnBfLWGp6ChWz98NG"
interact_with_assistant(assistant_id)