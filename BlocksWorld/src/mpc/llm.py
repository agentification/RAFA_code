import torch
import openai
from fastchat.model import load_model, get_conversation_template


def chat_with_gpt(messages: str, engine: str="gpt-3.5-turbo", temperature=0, top_p=0):
    response = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message['content']


vmodel, vtokenizer = None, None
@torch.inference_mode()
def chat_with_vicuna(messages: str,
                     model_path: str='lmsys/vicuna-7b-v1.3',
                     temperature=0,
                     num_gpus=3,
                     max_new_tokens=300,
                     repetition_penalty=0.5,
                     system_msg=""):
    # load model
    global vmodel, vtokenizer
    if vmodel is None or vtokenizer is None:
        vmodel, vtokenizer = load_model(
            model_path=model_path,
            device='cuda',
            num_gpus=num_gpus,
            max_gpu_memory='40GiB',
        )
    # prepare conversation
    conv = get_conversation_template(model_path)
    conv.system_message = system_msg
    for i, msg in enumerate(messages):
        if i % 2:
            conv.append_message(conv.roles[1], msg)
        else:
            conv.append_message(conv.roles[0], msg)
    conv.append_message(conv.roles[1], None)
    # collect the conv info into a prompt
    prompt = conv.get_prompt()
    # encode
    input_ids = vtokenizer([prompt]).input_ids
    # inference
    output_ids = vmodel.generate(
        torch.as_tensor(input_ids).cuda(),
        do_sample=True,
        temperature=temperature,
        repetition_penalty=repetition_penalty,
        max_new_tokens=max_new_tokens,
    )
    # rearrange
    if vmodel.config.is_encoder_decoder:
        output_ids = output_ids[0]
    else:
        output_ids = output_ids[0][len(input_ids[0]) :]
    # decode
    outputs = vtokenizer.decode(
        output_ids, skip_special_tokens=True, spaces_between_special_tokens=False
    )
    return outputs