echo 'process the mean max min'
python3 /home/chendi/githdd/plot/process.py 'data/processed_ncu/raw4090' 'data/4090csv'
python3 /home/chendi/githdd/plot/process.py 'data/processed_ncu/raw3090' 'data/3090csv'

echo 'data/4090csv'
echo 'gen gflops'

python3 gflops_gen.py 'data/4090csv'
python3 gflops_gen.py 'data/3090csv'


# roller 



echo 'performance data gen done'
