
corpus=LDC2020
cate=test

OutPath=outputs/${corpus}

if [ ! -d ${OutPath} ];then
  mkdir -p ${OutPath}
fi

python read_and_process.py --config config-default.yaml --input_file $1 --output_prefix ${OutPath}/$cate
