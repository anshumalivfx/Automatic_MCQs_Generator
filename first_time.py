from parrot import Parrot

def download_model(model_tag):
    # Instantiate the Parrot object with the desired model_tag
    parrot = Parrot(model_tag=model_tag, use_gpu=False)
    return parrot

if __name__ == "__main__":
    model_tag = "prithivida/parrot_paraphraser_on_T5"
    if model_tag == "prithivida/parrot_paraphraser_on_T5":
        print("Downloading the model for the first time. This might take a while...")
        if download_model(model_tag):
            print("Model downloaded successfully!")
