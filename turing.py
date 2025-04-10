from openai import OpenAI
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI()
client.api_key  = os.getenv('OPENAI_API_KEY')

abstract = """
A sustainable low-carbon transition via electric vehicles will require a comprehensive understanding of lithium-ion batteries’ global supply chain environmental impacts. Here, we analyze the cradle-to-gate energy use and greenhouse gas emissions of current and future nickel-manganese-cobalt and lithium-iron-phosphate battery technologies. We consider existing battery supply chains and future electricity grid decarbonization prospects for countries involved in material mining and battery production. Currently, around two-thirds of the total global emissions associated with battery production are highly concentrated in three countries as follows: China (45%), Indonesia (13%), and Australia (9%). On a unit basis, projected electricity grid decarbonization could reduce emissions of future battery production by up to 38% by 2050. An aggressive electric vehicle uptake scenario could result in cumulative emissions of 8.1 GtCO2eq by 2050 due to the manufacturing of nickel-based chemistries. However, a switch to lithium iron phosphate-based chemistry could enable emission savings of about 1.5 GtCO2eq. Secondary materials, via recycling, can help reduce primary supply requirements and alleviate the environmental burdens associated with the extraction and processing of materials from primary sources, where direct recycling offers the lowest impacts, followed by hydrometallurgical and pyrometallurgical, reducing greenhouse gas emissions by 61, 51, and 17%, respectively. This study can inform global and regional clean energy strategies to boost technology innovations, decarbonize the electricity grid, and optimize the global supply chain toward a net-zero future.
"""

prompt_system = f"""
You are given a scientific paper abstract.
Your task is to review the given text and provide a report on the following:
- Summarize the finding and explain all the scientific terms next to them in brackets.
- Structure the output as a numbered list.
- Give explanations of any scientific jargon between square brackets next to, in the sentence.
- Each bullet-point should start with words "The scientific evidence shows that..."
- There should be no more than 3 items in the list
- Return emojis as part of the text to make it more visually appealing and for better readability     
- The output should be a one-page web page in html format with headings, an intro, a numbered list as a table, one sentence summary at the bottom, and a call to action to the original paper. 
"""

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": prompt_system},
    {"role": "user", "content": abstract}
  ],
  max_tokens=150
)

print(completion.choices[0].message.content)