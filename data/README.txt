Here is how I partitioned out 1K sentences for dev:

[15:55][turian@rubis:~/data/conll2000-chunking]$ ./one-sentence-per-line.pl orig/test.txt > test.1.txt
[15:55][turian@rubis:~/data/conll2000-chunking]$ less test.1.txt
[15:55][turian@rubis:~/data/conll2000-chunking]$ ./one-sentence-per-line.pl orig/train.txt > train-original.1.txt
[15:55][turian@rubis:~/data/conll2000-chunking]$ ~/common/scripts/shuffle.sh < train-original.1.txt > train-original.shuffle.1.txt
[15:55][turian@rubis:~/data/conll2000-chunking]$ less train-original.shuffle.1.txt
[15:55][turian@rubis:~/data/conll2000-chunking]$ cp train-original.shuffle.1.txt
[15:55][turian@rubis:~/data/conll2000-chunking]$ head -1000 train-original.shuffle.1.txt > dev.1.txt
[15:56][turian@rubis:~/data/conll2000-chunking]$ wc -l train-original.shuffle.1.txt
8936 train-original.shuffle.1.txt
[15:56][turian@rubis:~/data/conll2000-chunking]$ tail -7936 train-original.shuffle.1.txt > train.1.txt
[15:56][turian@rubis:~/data/conll2000-chunking]$ cat dev.1.txt train.1.txt | diff - train-original.shuffle.1.txt
[15:56][turian@rubis:~/data/conll2000-chunking]$ head -1000 train.1.txt > train-1000.1.txt

[13:56][turian@dormeur:~/data/conll2000-chunking]$ cat dev.1.txt | perl -ne 's/ /\n/g; s/\|/ /g; print' > dev-partition.txt
[13:56][turian@dormeur:~/data/conll2000-chunking]$ cat train.1.txt | perl -ne 's/ /\n/g; s/\|/ /g; print' > train-partition.txt
