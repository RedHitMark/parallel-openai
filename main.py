import os
import time
import json
import random
import argparse

import jsonl_utils

from openai import OpenAI, NotGiven

from threading import Lock
from ratelimit import limits, sleep_and_retry
from concurrent.futures import ThreadPoolExecutor

LOCK = Lock()

MINUTES = 60
DEFAULT_N_THREADS = 2
DEFAULT_MAX_CALLS_PER_MINUTE = 500


@sleep_and_retry
@limits(calls=DEFAULT_MAX_CALLS_PER_MINUTE, period=MINUTES)
def do_openai_request(openai_client: OpenAI, request):
    try:
        response = openai_client.chat.completions.create(
            model=request['model'],
            messages=request['messages'],
            stream=False,
            frequency_penalty=request['frequency_penalty'] if 'frequency_penalty' in request else NotGiven(),
            logit_bias=request['logit_bias'] if 'logit_bias' in request else NotGiven(),
            logprobs=request['logprobs'] if 'logprobs' in request else NotGiven(),
            max_tokens=request['max_tokens'] if 'max_tokens' in request else NotGiven(),
            n=request['n'] if 'n' in request else NotGiven(),
            presence_penalty=request['presence_penalty'] if 'presence_penalty' in request else NotGiven(),
            response_format=request['response_format'] if 'response_format' in request else NotGiven(),
            seed=request['seed'] if 'seed' in request else NotGiven(),
            temperature=request['temperature'] if 'temperature' in request else NotGiven(),
            top_logprobs=request['top_logprobs'] if 'top_logprobs' in request else NotGiven(),
            top_p=request['top_p'] if 'top_p' in request else NotGiven(),
        )
        request['response'] = json.loads(response.json())
        return request
    except Exception as e:
        print(e)
        time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--openai_api_key', type=str, required='OPENAI_API_KEY' not in os.environ, default=os.getenv('OPENAI_API_KEY', ''))
    parser.add_argument('--source_jsonl_path', type=str, required=True)
    parser.add_argument('--output_jsonl_path', type=str, required=True)
    parser.add_argument('--max_calls_per_minute', type=int, default=DEFAULT_MAX_CALLS_PER_MINUTE)
    parser.add_argument('--n_threads', type=int, default=DEFAULT_N_THREADS)
    parser.add_argument('--shuffle', type=bool, default=False)
    args = parser.parse_args()

    # Customize the rate limiting decorator based on the user input
    do_openai_request = limits(calls=args.max_calls_per_minute, period=MINUTES)(do_openai_request)
    do_openai_request = sleep_and_retry(do_openai_request)

    # Initialize the OpenAI client
    client = OpenAI(api_key=args.openai_api_key)

    # Load requests
    requests = jsonl_utils.load_jsonl(args.source_jsonl_path)

    # Load done requests ids
    done_requests_id = set([r['id'] for r in jsonl_utils.load_jsonl(args.output_jsonl_path)])

    # Filter requests already done
    requests = [r for r in requests if r['id'] not in done_requests_id]

    # Shuffle the requests if requested
    if args.shuffle:
        random.shuffle(requests)

    # Process the requests
    with ThreadPoolExecutor(args.n_threads) as p:
        for result in p.map(lambda request: do_openai_request(client, request, args.output_jsonl_path), requests):
            with LOCK:
                jsonl_utils.append_to_jsonl(args.output_jsonl_path, result)
