clear
mv pops/pop0 .
rm -rf pops/pop*
mv pop0 pops/
rm childs/*
# python3 train.py
python3 train_v2.py
