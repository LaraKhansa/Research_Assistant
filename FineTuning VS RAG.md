# FineTuning VS RAG:
This document is a brief high-level explanation & comparison between FineTuning & RAG, aiming to provide a basic idea on the differences, similarities, when & how to use each one of them.

## Introduction:
RAG, standing for **Retrieval Augmented Generation**, is a technique used to enhance the capabilities of LLM models, enabling them to answer questions more accurately relying on domain-specific knowledge from a given data source.

Finetuning, on the other hand, is like making the model specialize in a certain topic or field, by training it on a well-prepared dataset so its weights are adjusted in service of that specific topic needed.

Both techniques, have shown mind blowing results in the terms of the improvement they can offer for pretrained models, enabling small/medium sized models to compete with the largest models in specific tasks.

The best way probably to desrcibe the analogy behind the 2 techniques, is what ["openai-cookbook"](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb?ref=blog.langchain.dev) states:

> As an analogy, model weights are like long-term memory. When you fine-tune a model, it's like studying for an exam a week away. When the exam arrives, the model may forget details, or misremember facts it never read.

> In contrast, message inputs are like short-term memory. When you insert knowledge into a message, it's like taking an exam with open notes. With notes in hand, the model is more likely to arrive at correct answers.

## The Components
### RAG
Basically made of 2 main components (plus the pretrained model):
- **Data Source:** The set of documents to be given to the model must be embedded. Embedding, shortly, is representing text as a vector in a high-dimensional space. This enables us to save text as a vector database, efficiently preserving contents' semantics & keeping it accesible easily and quickly for the retriever.

- **Retriever:** Say the model is asked a question, instead of answering directly from the knowledge it gained during its training, it will seek the help of the available data. A retriever, is the one that will search for and get the relevant information from the database depending on the user query. The retrieved information then is provided for the pretrained model as a context along with the query.

### FineTuning:
- **Dataset:** The dataset to be used for fine-tuning, must be prepared in a way that best serves the domain we want the model to specialize in. Preparing a finetuning dataset is considered relatively hard, as it requires a good quality & well cleaned dataset.

- **Training**: FineTuning modifies the model itself seeking to improve it on a specific task. Rather than training the model from the ground up, some/all of the existing layers parameters are adjusted.

## Pros & Cons
### RAG
- **Pros:**
    - **Avoiding Hallucinations**: It significantly lowers the chance of hallucinations, since it relies on the given data to fill knowledge gaps.
    - **Efficiency:** It is very efficient, as it doesn't require additional training or any costy computation, it is relatively a fast recipe.
    - **Flexibility:** It is a relatively flexible technique, as it can be used with any document & model, since it does not depend on the model architecture, parameters, training...
- **Cons:**
    - **Latency**: It requires the model to search and take into consideration relevant information from the database, which takes some time, depending on the retriever speed & database size, adding a noticeable latency to the model responses.
    - **Sensitivity to Data Quality**: It forces the model to rely on the given data. This means, in a way or another, it trusts it, and its responses will reflect the quality of the given data.
    - **Runtime Cost**: It requires a saved database as long as the model is running, this means additional space & computation while the model is used.
    - **Context Window Size Limitation**: Any LLM model, accepts
    flexible-size input up to a specific limit, which consequently limits the size of context we can provide to our model.

### FineTuning
- **Pros:**
    - **Faster than Re-training**
    - **Domain Adaptation**: Finetuning is a good tool to leverage a pretrained model capabilities for a different task, adapting its knowledge into the new field it is trained on during finetuning.
- **Cons**
    - **Cost**: It is expensive to train the model on more data, in terms of time & computational power.
    - **Data Quality**: It requires a well prepared dataset, which is not always available or easy to acquire. The dataset may also affect the model existing knowledge or accuracy depending on its quality.

# When to Use?
RAG is usually preferred when we need to:
- Minimze forgetting
- Get specific informative answers
- Up-to-date model

It is usually considered first before finetuning, since it is less expensive & easier.

Finetuning is used when we need to:
- Provide the model with permenant knowledge in a specific topic
- Get it to do a specific task that can't be implied in a prompt (like summarization, text classification, NER...)
- Set the style/tone/format of the model answers

<img src="https://global.discourse-cdn.com/openai1/optimized/3X/9/8/98dc9dab752ffd45e8b3a645eb8281c7af4b94d8_2_690x416.jpeg" alt="Which to use?" width="400" style="margin:30px 0"/>



# Summarized Comparison:
| | RAG | FineTuning |
| --- | --- | --- |
| Accuracy | Improved | Improved |
| Hallucinations | Lower Chance | Same |
| Response Latency | Retrieving Latency | &empty; |
| Cost | Fast Recipe | Needs Time + Computation |
| Dependence on Data | High | Moderate |
| Flexibility | High | Low |
| Maintenance | Easier | Harder |

## Resources:
- [OpanAI CookBook - Example on QA using embedding-based search](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb?ref=blog.langchain.dev)
- [RAG vs FineTuning - Monte Carlo Blog](https://www.montecarlodata.com/blog-rag-vs-fine-tuning/)
- [RAG vs Finetuning - Article on Medium](https://towardsdatascience.com/rag-vs-finetuning-which-is-the-best-tool-to-boost-your-llm-application-94654b1eaba7)