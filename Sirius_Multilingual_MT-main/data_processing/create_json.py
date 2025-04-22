import json
import os

OUTPUT_PATH = "train_jsonl/en_"

# Mapping of Flores-200 ISO language codes to more standard ISO language names
FLORES200_ISO_MAPPING = {
    "uzn_Latn": "uz",
    "heb_Hebr": "he",
    "kaz_Cyrl": "kk",
    "kir_Cyrl": "ky",
    "pes_Arab": "fa",
    "tur_Latn": "tr",
    "azb_Arab": "az_Arab",
    "azj_Latn": "az_Latn",
    "arb_Arab": "ar"
}


def create_json(split_name):
    langs = [f"{lang}.{split_name}" for lang in FLORES200_ISO_MAPPING.keys()]
    en_filename = f"eng_Latn.{split_name}"
    path_to_data = f"flores200_dataset/{split_name}/"

    for lang in langs:
        lang_code = lang.split('.')[0]
        lang_name = FLORES200_ISO_MAPPING.get(lang_code, lang_code)

        lang_file_path = os.path.join(path_to_data, lang)
        en_file_path = os.path.join(path_to_data, en_filename)
        output_file_path = f"{OUTPUT_PATH}{lang_name}_{split_name}.jsonl"

        with open(lang_file_path, 'r', encoding="utf-8") as lang_file, \
                open(en_file_path, 'r', encoding="utf-8") as en_file, \
                open(output_file_path, 'w', encoding="utf-8") as output_jsonl:

            lang_data = lang_file.readlines()
            en_data = en_file.readlines()

            # Ensure both files have the same number of lines
            assert len(lang_data) == len(en_data), f"Line mismatch in {lang} and {en_filename}"

            for i in range(len(lang_data)):
                dict_data = {"en": en_data[i].strip(), lang_name: lang_data[i].strip()}
                output_jsonl.write(json.dumps(dict_data) + '\n')


def concat_json(lang_name, json_file1_name, json_file2_name):
    input_file1 = f"{OUTPUT_PATH[:-3]}{json_file1_name}"
    input_file2 = f"{OUTPUT_PATH[:-3]}{json_file2_name}"
    output_file = f"{OUTPUT_PATH}{lang_name}_{json_file1_name.split('.')[0].split('_')[-1]}.jsonl"

    with open(input_file1, 'r', encoding="utf-8") as file1, \
            open(input_file2, 'r', encoding="utf-8") as file2, \
            open(output_file, 'w', encoding="utf-8") as output_jsonl:
        output_jsonl.writelines(file1.readlines())
        output_jsonl.writelines(file2.readlines())


if __name__ == "__main__":
    create_json("dev")
    create_json("devtest")
    concat_json("az", "en_az_Arab_dev.jsonl", "en_az_Latn_dev.jsonl")
    concat_json("az", "en_az_Arab_devtest.jsonl", "en_az_Latn_devtest.jsonl")
