#!/bin/bash

NUM_SEGMENTS=30
NUM_OUTPUTS=50

SRC="/root/dlstreamer/stream_batch_error/datasets/mp4/1192116-sd_640_360_30fps/1192116-sd_640_360_30fps.mp4"

BASE_DIR=$(dirname "$SRC")
FILENAME=$(basename "$SRC")
BASENAME="${FILENAME%.*}"

SEG_DIR="$BASE_DIR/segments"
OUT_DIR="$BASE_DIR/input"

mkdir -p "$SEG_DIR" "$OUT_DIR"
rm -f "$SEG_DIR"/*.mp4 "$OUT_DIR"/*.mp4

# 1. 取时长
DURATION=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "$SRC")

SEG_LEN=$(awk "BEGIN {print $DURATION/$NUM_SEGMENTS}")

echo "Each segment length: $SEG_LEN"

# 2. 等量切分
for ((i=0;i<NUM_SEGMENTS;i++)); do
    START=$(awk "BEGIN {print $i*$SEG_LEN}")
    ffmpeg -y -ss "$START" -t "$SEG_LEN" -i "$SRC" -c copy \
        "$SEG_DIR/seg_$i.mp4"
done

# 3. 随机重排拼接（每个视频用全部段）
for ((i=1;i<=NUM_OUTPUTS;i++)); do
    LISTFILE="$OUT_DIR/list_$i.txt"
    > "$LISTFILE"   # 强制创建空文件

    ls "$SEG_DIR"/seg_*.mp4 | shuf | while read f; do
        echo "file '$f'" >> "$LISTFILE"
    done

    ffmpeg -y -f concat -safe 0 -i "$LISTFILE" -c copy \
        "$OUT_DIR/${BASENAME}_$i.mp4"

    echo "Generated: ${BASENAME}_$i.mp4"
done

echo "Done."
