from re import search, DOTALL
from json import loads
from json.decoder import JSONDecodeError

import openai


def completion(content, summary_len, tags_len, apikey):
    '''
    Generates a prompt and requests a completion from ChatGPT.
    Returns the completion in a Python dictionary.
    DISCLAIMER
    ChatGPT is not deterministic, so eventually the response will break
    the code.
    '''
    system_prompt = '\n'.join([
        'You are the SEO Advisor for my texts.',
        'My texts are written in Markdown format.',
        'You create title, summary, and tags for my texts.',
        'You create clear SEO friendly titles for my texts of 5 words tops.',
        f'You create short summaries for my texts of {summary_len} words tops.',
        f'You create {tags_len} SEO friendly, lowercase, and single worded tags for my texts.',
        'Title and summary are strings and tags are a list of strings.',
        'You only answer in JSON, nothing more.'
    ])
    user_prompt = content
    tokens_in_prompt = (len(system_prompt) + len(user_prompt)) * 0.75
    if tokens_in_prompt > 4096:
        # max tokens - tokens_in_sys / 0.75 ~= words/chars available
        available = int((4096 - len(system_prompt) * 0.75) / 0.75)
        user_prompt = user_prompt[:available]
    prompt = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    openai.api_key = apikey
    model_id = 'gpt-3.5-turbo'
    response = openai.ChatCompletion.create(
        # complete list of parameters:
        # https://platform.openai.com/docs/api-reference/completions/create
        model=model_id,
        temperature=0.8,
        messages=prompt
    )
    # print(response.choices[-1].message.content)
    return loads(response.choices[-1].message.content)

def text_processor(path, summary_len, tags_len, apikey):
    '''
    Gets the user parameters for a single file and calls completion.
    Returns the completion response of None in case of issues.
    '''
    # file starts with header which is delimited by plus signals
    # this regex wipes the header out to return only the content
    re_content = r'\++?.*\++\n+(.*)'
    with open(path,'r') as f:
        data = f.read()
        content = search(re_content, data, DOTALL)[1]
        try:
            res = completion(content, summary_len, tags_len, apikey)
        except JSONDecodeError:
            res = None
        return res
