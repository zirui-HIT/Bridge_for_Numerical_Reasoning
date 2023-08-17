ENGINE="gpt3.5"
PROMPT="FoT"
DATASET="GSM8K"
for MODE in answer erase translate answer;
do
    if [ $MODE = 'erase' ];
    then
        INPUT_PATH="./dataset/$DATASET/input/test.json"
    elif [ $MODE = 'decompose' ];
    then
        INPUT_PATH="./dataset/${DATASET}/output/${PROMPT}/$ENGINE/test.erase.json"
    elif [ $MODE = 'translate' ];
    then
        INPUT_PATH="./dataset/${DATASET}/output/${PROMPT}/$ENGINE/test.decompose.json"
    elif [ $MODE = 'answer' ];
    then
        INPUT_PATH="./dataset/${DATASET}/output/${PROMPT}/$ENGINE/test.translate.json"
    fi

    python3 run.py \
            --engine $ENGINE \
            --module_path prompt.${PROMPT}.${MODE} \
            --prompt_path ./prompt/$PROMPT/$DATASET/$MODE.txt \
            --input_path $INPUT_PATH \
            --output_path ./dataset/${DATASET}/output/${PROMPT}/$ENGINE/test.${MODE}.json \
            --parallel
done
python3 evaluate.py \
        --input_path ./dataset/${DATASET}/output/${PROMPT}/$ENGINE/test.answer.json \
        --output_path ./dataset/${DATASET}/output/${PROMPT}/$ENGINE/test.answer.eval.json
