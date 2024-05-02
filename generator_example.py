import argparse

import jsonl_utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_jsonl_path', type=str, required=True)
    args = parser.parse_args()

    for i in range(5):
        model_data = {
            "id": i,
            "model": f'gpt-3.5-turbo-0125',
            "messages": [
                {
                    "role": "system",
                    "content": 'You are a math expert'
                },
                {
                    "role": "user",
                    "content": f'Evaluate the following sum: 30 + {i}'
                }
            ],
        }
        jsonl_utils.append_to_jsonl(args.source_jsonl_path, model_data)
