import argparse
import logging
import multiprocessing
import os
import sys

import gentle

parser = argparse.ArgumentParser(
        description='Align a transcript to audio by generating a new language model.  Outputs JSON')
parser.add_argument(
        '--nthreads', default=multiprocessing.cpu_count(), type=int,
        help='number of alignment threads')
parser.add_argument(
        '-o', '--output', metavar='output', type=str, 
        help='output filename')
parser.add_argument(
        '--conservative', dest='conservative', action='store_true',
        help='conservative alignment')
parser.add_argument(
        '--disfluency', dest='disfluency', action='store_true',
        help='include disfluencies (uh, um) in alignment')
parser.set_defaults(disfluency=False)
parser.add_argument(
        '--log', default="INFO",
        help='the log level (DEBUG, INFO, WARNING, ERROR, or CRITICAL)')
parser.add_argument(
        'audiofile', type=str,
        help='audio file')
parser.add_argument(
        'transcript', type=str,
        help='transcript')
args = parser.parse_args()

log_level = args.log.upper()
logging.getLogger().setLevel(log_level)

disfluencies = set(['uh', 'um'])

def on_progress(p):
    for k,v in p.items():
        logging.debug("%s: %s" % (k, v))


from pathlib import Path
transcript = args.transcript
if Path(transcript).exists():
    transcript = Path(transcript).read_text()

resources = gentle.Resources()
logging.info("converting and resampling to wav")

with gentle.resampled(args.audiofile) as wavfile:
    logging.info("starting alignment")
    aligner = gentle.ForcedAligner(resources, transcript, nthreads=args.nthreads, disfluency=args.disfluency, conservative=args.conservative, disfluencies=disfluencies)
    result = aligner.transcribe(wavfile, progress_cb=on_progress, logging=logging)

fh = open(args.output, 'w', encoding="utf-8") if args.output else sys.stdout
fh.write(result.to_json(indent=2))
if args.output:
    logging.info("output written to %s" % (args.output))
