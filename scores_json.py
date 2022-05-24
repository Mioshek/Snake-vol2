import json

def write_to_json(data):
    sorted_data = sorted(data, reverse=True)
    data_ready_to_write = {index:score for index, score in enumerate(sorted_data)}
    print(data_ready_to_write)
    with open('ten_best_scores.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        print("done")
    json_file.close()
    
def read_from_json():
    with open('ten_best_scores.json', 'r') as json_file:
        loaded_json_data = json.load(json_file)
    json_file.close()
    return loaded_json_data