# /main.py
import config  # This will run the environment loading
from graph.builder import build_graph
from langchain_core.messages import HumanMessage
from IPython.display import display, Markdown

def main():
    """Main function to run the Samsung assistant chat."""
    app = build_graph()
    
    print("Welcome to the Samsung Phone Assistant! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        # The graph expects a list of messages
        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        # Invoke the graph
        response = app.invoke(inputs)
        
        # The final message is the last one in the list
        final_message = response["messages"][-1]
        
        # Display the response
        print("\nAssistant:")
        # display(Markdown(final_message))
        print(final_message)
        print("-" * 50)

if __name__ == "__main__":
    main()