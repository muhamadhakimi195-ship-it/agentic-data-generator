ANALYZER_USER_PROMPT="""Analyze the structure and patterns of this sample data:

{sample_data}

Provide a concise summary of the following 
1. formatting of the dataset, be crystal clear when decribing the structure of the CSV
2. What the dataset represents, what each column stands for
3. how new data should look like, based on the patterns you've identified
"""
GENERATOR_USER_PROMPT = """ Generate {num_rows} new CSV rows based on this analystics and sample data:

Analysis:
{analysis_result}

Sample_data:
{sample_data}

Use the exact same formatting as the original data. Output only the generted rows, no extra text.

DO NOT INCLUDE ANY TEXT BEFORE/AFTER THE DATA. JUST START BY OUTPUTTING THE NEW ROWS. NO EXTRA TEXT!!!
"""