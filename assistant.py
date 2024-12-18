from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("api_key")
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

def interact_with_assistant(assistant_id, user_input, my_thread_id):
    print("Start interacting with the assistant.")
    # END est le mot clef pour mettre fin à l'intéraction
    if user_input.lower() == "end":
        client.beta.threads.delete(thread_id=my_thread_id)
        return '"END" keyword user. Deleting the Thread. Goodbye!'
    # Create a thread and get the run ID
    my_run_id, my_thread_id = update_thread(my_thread_id, assistant_id, user_input)

    # Check the status of the response
    status = check_status(my_run_id, my_thread_id)
    while status != "completed":
        status = check_status(my_run_id, my_thread_id)
    
    x = client.beta.threads.messages.list(run_id=my_run_id, thread_id=my_thread_id)

    # Retrieve the response
    response = client.beta.threads.messages.list(thread_id=my_thread_id)

    # Parse and print the assistant's response
    if response.data:
        for message in response.data:
            if message.role == "assistant":
                # Extract the value from the TextContentBlock
                assistant_reply = message.content[0].text.value
                return assistant_reply
    else:    
        return "Err : No response received from the assistant."

