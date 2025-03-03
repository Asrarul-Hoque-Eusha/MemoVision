#==== Descriptions =====
answer_for_similar_images = "Here are some similar images to your search: "
answer_for_matching = "Here are some matching images similar to your search. "
answer_for_not_matching = "Unfortunately, there is no match for your search. However, here are some images that might be relevant to your search. If are looking for other images than, feel free to ask! "
chatbot_error_description = "An error occurred while processing the query."
ask_llm_answer = "I am MemoVision ChatBot, your AI-Powered Photo Gallery Assistant. Able to help you in find images from gallery and describe images. If you need assistance with image, let me know!"
no_image_found_message = "Sorry, no such images are found. If you have any other query about images in your gallery, feel free to ask!"

#===== Prompts =====
image_describer_prompt = "You are an image describer. Now answer to the query: `{query}` in between 200 words."
description_generation_prompt = """Analyze the given image and generate a structured description along with 3-10 relevant tags.
                                    Provide a concise, engaging summary of the image in 180 words or fewer. 
                                    **Include the following key elements if they are present in the scene** else don't discuss about this:
                                    - Scenes (e.g., sunset, sunrise)
                                    - Landscapes (e.g., beach, forest, hill, field)
                                    - Events (e.g., birthday, wedding, tours)
                                    - Objects (e.g., tree, car, bus, tiger, road, building, etc.)
                                    - Humans (e.g., boy, girl, children, man, woman, people, etc.)
                                    - Activities (e.g., running, walking, hiking, playing, skating, etc.)
                                    - Pets (e.g., cat, dog, bird, etc
                                    Create a space-separated string of 3–10 specific tags summarizing these key elements in description.
                                    **Strictly return only a valid Python dictionary with exactly two keys: "description" and "tags".** 
                                    **Do not include any extra text, markdown, or additional keys.** 
                                    Example: {"description": "A detailed image description here.", "tags": "sunset beach car family"} 
                                    """

description_summarization_prompt = """#### Task
                                    Summarize each description from the given list: `{description}`, ensuring relevance to the query: `{query}`.
                                    #### Actions
                                    - Generate a **40-50 word summary** for each description, preserving key details.
                                    - Number each summary in the format:  
                                        1. [Summary]  
                                        2. [Summary]  
                                        3. [Summary]  
                                    - Return `{alternate_answer}` along with the summaries placing the message before summaries.  
                                    #### Guidelines
                                    - **Strictly return only the output asked for. No reasoning, no explanation of your task.**  
                                    - **DO NOT** explain the your task, reasoning, query matching, or step-by-step process.  
                                    - Ensure the **entire response is between 270-300 words.**  
                                    """
text_query_keyword_extraction_prompt = """Analyze the given instruction: `{instruction}` . 
                                         - Extract and return only the key single-word keywords present in the instruction 
                                         such as scene , landscape, events , objects, humans (eg boy, girl, children, man, women, people etc) , activities (eg. running, walking, hiking, playing, skating etc), and pets (eg. cat, dog, bird etc) if they are present. 
                                         - Consider keywords explicitly mentioned as to **included** in the instruction.
                                         - Consider explicitly mentioned keywords followed by the words "without," "no," "avoid," "exclude," "not having," "not similar," or "dissimilar" as **excluded**.
                                         - Strictly follow the output format and do not add any extra keywords or explanations. And don't add same keyword in both lines.
                                         - Avoid irrelevant, redundant or overly generic keywords like environment, image, scene, scenery, outdoor, picture, nature, attire.
                                         - Don't include stopwords such as 'the', 'or', 'and', 'for', 'in' etc. as keywords.
                                         - **Strictly return only the output asked for.**
                                         - Output the keywords as a string of two lines with no additional text.
                                         Output:
                                             **First line:** [Space-separated keywords for features that should be **included**.]
                                             **Second line:** [Space-separated keywords for features that should be **excluded** if following words **"without," "no," "avoid," "exclude," "not having," "not similar," or "dissimilar" are present**, else give an empty line.]"""

multimodal_query_keyword_extraction_prompt = """Understand the instructions: `{instruction}` and analyze the given image as per the user instruction to extract key single-word keywords that can be used as tags to find similar images.
                                                - Identify and include only relevant key elements such scene (eg. sunset, sunrise, sunny), landscape (beach, forest, hill, field), events (eg. birthday, wedding, tours), objects , humans (eg boy, girl, man, women etc), activities (eg. running, walking, etc), and pets (eg. cat, dog, bird etc) if they are present.
                                                - Consider keywords explicitly mentioned as to **included** in the instruction.
                                                - Consider keywords explicitly mentioned as **excluded** (e.g., words following "without," "no," "avoid," "exclude", "not having", "not similar", "dissimilar", etc).
                                                - Do not generate extra or redundant keywords. And don't add same keyword in both lines.
                                                - Do not add explanations or any other texts.
                                                - **Give only 3-10 relevant keywords** with no additional text or formatting.
                                                - Avoid irrelevant, redundant or overly generic tags like environment, image, scene, scenery, outdoor, picture, nature, attire. Make sure the tags are specific to the image.
                                                - Don't include stopwords such as 'the', 'or', 'and', 'for', 'in' etc. as keywords.
                                                - **Strictly return only the output asked for.**
                                                - Output the keywords as a string of two lines with no additional text.
                                                 Output:
                                                     **First line:** [Space-separated keywords for features that should be **included**.]
                                                     **Second line:** [Space-separated keywords for features that should be **excluded** if following words **"without," "no," "avoid," "exclude," "not having," "not similar," or "dissimilar" are present**, else give an empty line.]"""