# parallel-openai
parallel-openai is an open-source project that allows you to perform parallel processing of OpenAI's API requests. It is designed to be used with OpenAI's ChatCompletion, but it can be easily adapted to work with other APIs as well. 
The project is written in Python and uses the `concurrent.futures` module to perform parallel processing of API requests. 
It also includes a rate limiting mechanism to prevent exceeding the OpenAI API's usage limits. 
The project is designed to be easy to use and flexible, allowing you to easily adapt it to your specific needs.


## Features
- **OpenAI API**: The project uses official OpenAI's API to generate paraphrases of texts.
- **Multithreading**: The project uses multithreading to maximize computational efficiency for large datasets.
- **Rate Limiting**: The project uses rate limiting to avoid exceeding OpenAI APIs usage limits.

## Setup
Create an account on OpenAI and get your API key.

Create a virtual environment and install the requirements.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
Customize and run the `generator_example.py` script to map your OpenAI requests into the `source.jsonl` file.\
Add an `id` field to each request to identify the request in the output file. 
```bash
python3 generator_example.py 
```

Run the `main.py` script to perform parallel requests to the OpenAI API.\
The script will read the requests from the `source.jsonl` file and write the responses to the `output.jsonl` file.
```bash
python3 main.py --api_key YOUR_API_KEY 
                --source_jsonl_path source.jsonl
                --output_jsonl_path output.jsonl 
                --max_calls_per_minute 400
                --n_thread 4
                --shuffle
```


## License
[MIT](https://choosealicense.com/licenses/mit/)