import argparse

import tiktoken

import jsonl_utils


def flatten_messages(requests):
    message_content_list = []
    for request in requests:
        for message in request['messages']:
            message_content_list.append(message['content'])
    return message_content_list


def count_token(encoder, text):
    tokens = encoder.encode(text)
    return len(tokens)


def do_estimation(requests, openai_model_name, price_per_million_tokens_input, price_per_million_tokens_output):
    encoder = tiktoken.encoding_for_model(openai_model_name)

    messages = flatten_messages(requests)

    n_requests = len(requests)
    n_messages = len(messages)

    tokens = [count_token(encoder, message) for message in messages]

    input_total_tokens = sum(tokens)
    output_total_token = input_total_tokens  # the output should be similar to the input len

    input_cost = input_total_tokens / 1000000 * price_per_million_tokens_input
    output_cost = output_total_token / 1000000 * price_per_million_tokens_output

    total_cost_no_tax = input_cost + output_cost
    total_cost_with_tax = total_cost_no_tax * 1.22

    print('n_requests', n_requests)
    print('n_messages', n_messages)

    print('input_tokens:', round(input_total_tokens, 2))
    print('output_tokens:', round(output_total_token, 2))

    print('input_cost:', round(input_cost, 2))
    print('output_cost:', round(output_cost, 2))

    print('total_cost_no_tax:', round(total_cost_no_tax, 2))
    print('total_cost_with_tax:', round(total_cost_with_tax, 2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_jsonl_path', type=str, required=True)
    parser.add_argument('--openai_model_name', type=str, required=True)
    parser.add_argument('--price_per_million_tokens_input', type=float, required=True)
    parser.add_argument('--price_per_million_tokens_output', type=float, required=True)
    args = parser.parse_args()

    requests = jsonl_utils.load_jsonl(args.source_jsonl_path)
    do_estimation(requests, args.openai_model_name, args.price_per_million_tokens_input, args.price_per_million_tokens_output)
