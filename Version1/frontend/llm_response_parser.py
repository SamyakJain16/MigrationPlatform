import json
# from get_results_openai import result_openai


def parse_llm_response(new_results):
    parsed_list = []
    for result in new_results:
        # Step 1: Check if the result contains the markers that indicate it needs cleaning
        if result.startswith('```json') and result.endswith('```'):
            # Step 2: Remove the backticks and the '```json' or '```' markers
            clean_output = result.strip("```json").strip("```")
        else:
            # If no markers are found, keep the result as-is
            clean_output = result

        # Step 3: Parse the remaining string into a JSON object, if it's valid JSON
        try:
            parsed_json = json.loads(clean_output)
            parsed_list.append(parsed_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for result: {result[:30]}...: {e}")
            # Optionally, append the original result if decoding fails
            parsed_list.append(result)

    return parsed_list


# final_result = parse_llm_response(result_openai)
