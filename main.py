# -*- coding: UTF-8 -*-
import cv2 as cv
import argparse
import numpy as np
import time
from utils import choose_run_mode, load_pretrain_model, set_video_writer
from Pose.pose_visualizer import TfPoseVisualizer
from Action.recognizer import load_action_premodel, framewise_recognize

parser = argparse.ArgumentParser(description='Action Recognition by OpenPose')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

# 모델 불러오기
estimator = load_pretrain_model('VGG_origin')
action_classifier = load_action_premodel('Action/taekwondo_recognition.h5')

# 매개변수 초기화
realtime_fps = '0.0000'
start_time = time.time()
fps_interval = 1
fps_count = 0
run_timer = 0
frame_count = 0

# video file 읽기 및 쓰기
cap = choose_run_mode(args)
video_writer = set_video_writer(cap, write_fps=int(7.0))

# skeleton data for Training을 txt 파일로 저장
# f = open('data\\txt_data\\taekwondoskill2-3-1.txt', 'a+')

while cv.waitKey(1) < 0:
    has_frame, show = cap.read()
    if has_frame:
        fps_count += 1
        frame_count += 1

        # pose estimation
        humans = estimator.inference(show)
        # get pose info
        pose = TfPoseVisualizer.draw_pose_rgb(show, humans)  # return frame, joints, bboxes, xcenter
        # recognize the action framewise
        show = framewise_recognize(pose, action_classifier)

        height, width = show.shape[:2]
        # 실시간 FPS 값 표시
        if (time.time() - start_time) > fps_interval:
            # calculate the number of frames in this interval, if interval is 1second(FPS)
            realtime_fps = fps_count / (time.time() - start_time)
            fps_count = 0  # 프레임 수 지우기
            start_time = time.time()
        fps_label = 'FPS:{0:.2f}'.format(realtime_fps)
        cv.putText(show, fps_label, (width-160, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # 감지된 사람 수 표시
        num_label = "Human: {0}".format(len(humans))
        cv.putText(show, num_label, (5, height-45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # 현재 실행 시간과 총 프레임 수를 표시
        if frame_count == 1:
            run_timer = time.time()
        run_time = time.time() - run_timer
        time_frame_label = '[Time:{0:.2f} | Frame:{1}]'.format(run_time, frame_count)
        cv.putText(show, time_frame_label, (5, height-15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv.imshow('Action Recognition based on OpenPose', show)
        video_writer.write(show)

        # skeleton data for Training을 txt 파일로 저장
        # joints_norm_per_frame = np.array(pose[-1]).astype(np.str)
        # f.write(' '.join(joints_norm_per_frame))
        # f.write('\n')

video_writer.release()
cap.release()
# f.close()
