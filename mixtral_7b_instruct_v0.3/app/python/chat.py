from IPython.display import display, HTML
import transformers
import os, yaml
import logging
import gradio
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatStatus():
    """Manages the conversation history for a turn-based chatbot"""

    def __init__(self, pipeline, tokenizer, max_position_embeddings=32768) -> None:
        self.pipeline = pipeline
        self.tokenizer = tokenizer
        self.history = []
        self.max_position_embeddings = max_position_embeddings
    
    def add_message(self, role: str, content: str):
        """Adds a message to the history."""
        if role not in ("user", "assistant"):
            raise ValueError("Role must be either 'user' or 'assistant'")
        self.history.append({"role": role, "content": content})
        
    def get_history_as_text(self) -> str:
        """Returns the chat history as a formatted string."""
        return "\n".join(f"{msg['role']}: {msg['content']}" for msg in self.history)

    def _truncate_history(self):
        """
        Truncates history if it exceeds the model's max input length.
        Removes the oldest entries first.
        """
        while True:
            encoded = self.tokenizer(
                self.get_history_as_text(),
                return_tensors="pt",
                truncation=False
            )["input_ids"]

            if encoded.shape[1] <= self.max_position_embeddings or len(self.history) <= 1:
                break
            self.history.pop(0)  # drop oldest message

    def send_message(self, message: str) -> str:
        """
        Sends a user message, gets the model response, and updates history.
        """
        self.add_message("user", message)
        self._truncate_history()

        response = self.pipeline(self.history)
        reply = response[0]["generated_text"]

        self.add_message("assistant", reply)
        return reply
    
def load_model(config):

    model_dir = os.path.join("/src/app", config['model']['path'])

    snapshots = os.listdir(model_dir)
    if snapshots:
        latest_snapshot = snapshots[0] # Assuming the first one is the latest
        full_model_dir = os.path.join(model_dir, latest_snapshot)
        logger.info(f"Model path: {full_model_dir}")
    else:
        logger.info(f"No snapshots found inside {model_dir}")

    try:
        logger.info(f"Attempting to load tokenizer and model from {full_model_dir}")
        tokenizer = transformers.AutoTokenizer.from_pretrained(full_model_dir)
        logger.info("Model and tokenizer successfully loaded from primary directory.")
        model_id = full_model_dir
    except (OSError, ValueError) as e:
        logger.error(f"Failed to load from {model_dir}: {e}")
        raise SystemExit(f"Failed to load the model: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise SystemExit(f"An unexpected error occurred: {e}")

    pipeline = transformers.pipeline(
        "text-generation",
        model=model_id,
        tokenizer = tokenizer,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
        return_full_text=False,
        max_new_tokens=300,
    )

    return tokenizer, pipeline  

if __name__=="__main__":

    config_path = "/src/config/config.yml"
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    tokenizer, pipeline = load_model(config)

    chat_status = ChatStatus(pipeline, tokenizer)

    app = gradio.Interface(
        fn= chat_status.send_message,
        inputs=gradio.Textbox(lines=2, placeholder="Type your message here..."),
        outputs="text",
        title="Mixtral-7B-Instruct-v0.3 Model Chat Interface",
        description="Chat with the model."
    )

    app.launch(server_port=7860, server_name="0.0.0.0", debug=True)