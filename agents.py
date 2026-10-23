import os 
import io
import csv
from openai import OpenAI 
import prompts

if not os.getenv("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = input("Enter you OpenRouter API Key: ")

client= OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=os.environ["OPENROUTER_API_KEY"],
    )
nemotron = "nvidia/nemotron-3-ultra-550b-a55b:free"

# read  the csv file from the User
def read_csv(file_path):
    data=[]
    with open(file_path, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a'
    with open(output_file, mode , newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(io.StringIO(data), strict=True):
            writer.writerow(row)

def analyzer_agent(sample_data):
    response = client.chat.completions.create(
        model=nemotron,
        max_tokens=1500,
        temperature=0.1,
        messages=[
            {
                "role":"user",
                "content": prompts.ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return response.choices[0].message.content

def generator_agent(analysis_results, sample_data, num_rows=30):
    response = client.chat.completions.create(
        model=nemotron,
        max_tokens=4000,
        temperature=1,
        
            messages=[
                {
                    "role":"user",
                    "content":prompts.GENERATOR_USER_PROMPT.format(
                        num_rows=num_rows,
                        analysis_result= analysis_results,
                        sample_data= sample_data,
                    ),
                }
        ]
    )
    choice = response.choices[0]

    if choice.finish_reason == "length":
        raise ValueError("Response was cut off. Reduce the batch size.")

    if not choice.message.content:
        raise ValueError("The model returned no CSV text.")

    return choice.message.content


file_path = input("\nEnter the name of your CSV file: ")
file_path = os.path.join('/app/data', file_path)
desired_rows = int(input("Enter the number of rows you want in the new dataset: "))

sample_data = read_csv(file_path)
sample_buffer = io.StringIO(newline="")
csv.writer(sample_buffer).writerows(sample_data)
sample_data_str = sample_buffer.getvalue()

print("\nLaunching team of Agents...")
analysis_result= analyzer_agent(sample_data_str)
print("\n### Analyzer Agent output: ###\n")
print(analysis_result)
print("\n---------------------------\n\nGenerating new data...")

#setup output file
output_file = "/app/data/new_dataset.csv"
headers = sample_data[0]

save_to_csv("", output_file, headers)

batch_size = 5
generated_rows =0

while generated_rows < desired_rows:
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    generated_data = generator_agent(
        analysis_result, sample_data_str, rows_to_generate
        )
    rows = list(
        csv.reader(io.StringIO(generated_data), strict=True)
    )

    if len(rows) != rows_to_generate:
        raise ValueError("Wrong number of generated rows.")

    if any(len(row) != len(headers) for row in rows):
        raise ValueError("Generated rows have incorrect column counts.")
    
    save_to_csv(generated_data, output_file)
    
    generated_rows += len(rows)
    print(f"Generated {generated_rows} rows out of {desired_rows}")
    
