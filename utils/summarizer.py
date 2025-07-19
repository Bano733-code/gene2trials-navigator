import torch
from transformers import BartForConditionalGeneration, BartTokenizer

# Load model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)

def chunk_text(text, max_token_length=1024):
    """
    Splits a long string into chunks that fit the model's max token size.
    """
    inputs = tokenizer.encode(text, return_tensors="pt", truncation=False)[0]
    chunks = []
    for i in range(0, len(inputs), max_token_length):
        chunk = inputs[i:i + max_token_length]
        chunks.append(chunk.unsqueeze(0))
    return chunks

def summarize_pubmed_abstracts(abstracts):
    combined_text = " ".join(abstracts)

    # Split the input into chunks of max 1024 tokens
    input_chunks = chunk_text(combined_text)
    summaries = []

    for chunk in input_chunks:
        chunk = chunk.to(device)
        summary_ids = model.generate(
            chunk,
            max_length=130,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary_text)

    return " ".join(summaries)
