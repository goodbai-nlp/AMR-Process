corpus=LDC2020

OutPath=outputs/${corpus}
if [ ! -d ${OutPath} ];then
  mkdir -p ${OutPath}
fi

for cate in train val test
do
    echo "Processing ${cate}..."
    if [ "$cate" == "train" ]; then
        cate2="training"
    elif [ "$cate" == "val" ]; then
        cate2="dev"
    else
        cate2=$cate
    fi
    python read_and_process.py --config config-default.yaml --input_file data/${corpus}/amrs/split/${cate2}/*-all.txt --output_prefix ${OutPath}/$cate
done