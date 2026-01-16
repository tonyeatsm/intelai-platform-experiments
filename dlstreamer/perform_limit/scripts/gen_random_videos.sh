#!/bin/bash

######################## 可配置参数 ########################
NUM_SEGMENTS=30      # 原视频切成多少段
NUM_OUTPUTS=8        # 生成多少个随机拼接视频
LEN_OUTPUTS=100      # 每个输出视频由多少段组成（可重复）
##########################################################

SRC="/root/dlstreamer/perform_limit/datasets/mp4/1192116-sd_640_360_30fps/1192116-sd_640_360_30fps.mp4"

BASE_DIR=$(dirname "$SRC")
FILENAME=$(basename "$SRC")
BASENAME="${FILENAME%.*}"

SEG_DIR="$BASE_DIR/segments"
OUT_DIR="$BASE_DIR/input"

mkdir -p "$SEG_DIR" "$OUT_DIR"
rm -f "$SEG_DIR"/*.mp4 "$OUT_DIR"/*.mp4

# 1. 获取视频总时长
DURATION=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "$SRC")

SEG_LEN=$(awk "BEGIN {print $DURATION/$NUM_SEGMENTS}")
echo "Each segment length: $SEG_LEN seconds"

# 2. 等长切分
for ((i=0;i<NUM_SEGMENTS;i++)); do
    START=$(awk "BEGIN {print $i*$SEG_LEN}")
    ffmpeg -y -ss "$START" -t "$SEG_LEN" -i "$SRC" -c copy \
        "$SEG_DIR/seg_$i.mp4"
done

# 3. 随机拼接（带放回抽样 LEN_OUTPUTS 次）
for ((i=1;i<=NUM_OUTPUTS;i++)); do
    LISTFILE="$OUT_DIR/list_$i.txt"
    > "$LISTFILE"

    for ((k=0;k<LEN_OUTPUTS;k++)); do
        IDX=$((RANDOM % NUM_SEGMENTS))
        echo "file '$SEG_DIR/seg_$IDX.mp4'" >> "$LISTFILE"
    done

    ffmpeg -y -f concat -safe 0 -i "$LISTFILE" -c copy \
        "$OUT_DIR/${BASENAME}_$i.mp4"

    echo "Generated: ${BASENAME}_$i.mp4  (segments=$LEN_OUTPUTS)"
done

echo "All done."
