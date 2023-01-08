from queue import Queue
from gentle import standard_kaldi

def build(exp, nthreads=4, hclg_path=None):
    kaldi_queue = Queue()
    for i in range(nthreads):
        kaldi_queue.put(standard_kaldi.Kaldi(exp, hclg_path))
    return kaldi_queue
