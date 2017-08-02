import os
import tempfile
import shutil
import json

import numpy as np

import unittest
import unittest.mock as mock

from gulpio.utils import (check_ffmpeg_exists,
                          burst_video_into_frames,
                          resize_by_short_edge,
                          resize_images,
                          )


class TestCheckFFMPEGExists(unittest.TestCase):

    @mock.patch('os.system', mock.Mock(return_value=0))
    def test_exists(self):
        self.assertEqual(True, check_ffmpeg_exists())

    @mock.patch('os.system', mock.Mock(return_value=1))
    def test_does_not_exists(self):
        self.assertEqual(False, check_ffmpeg_exists())


class TestBurstVideoIntoFrames(unittest.TestCase):

    def test(self):
        video_path = os.path.join(os.path.dirname(__file__), 'test.mp4')
        temp_dir, imgs = burst_video_into_frames(video_path, '/dev/shm')
        self.assertEqual(21, len(imgs))
        shutil.rmtree(temp_dir)


class TestResizeImages(unittest.TestCase):

    @mock.patch('cv2.imread')
    @mock.patch('gulpio.utils.resize_by_short_edge')
    def test(self, mock_resize, mock_imread):
        mock_imread.side_effect = ['READ_IMAGE1',
                                   'READ_IMAGE2',
                                   'READ_IMAGE3']
        mock_resize.side_effect = ['RESIZED_IMAGE1',
                                   'RESIZED_IMAGE2',
                                   'RESIZED_IMAGE3']
        input_ = ['ANY_IMAGE1',
                  'ANY_IMAGE2',
                  'ANY_IMAGE3']
        received = list(resize_images(input_, img_size=1))
        self.assertEqual(['RESIZED_IMAGE1',
                          'RESIZED_IMAGE2',
                          'RESIZED_IMAGE3'],
                         received)


class TestResizeByShortEdge(unittest.TestCase):

    def test_resize_first_edge_shorter(self):
        input_image = np.zeros((6, 10))
        size = 3
        correct_result = np.zeros((3, 5))
        result = resize_by_short_edge(input_image, size)
        np.testing.assert_array_equal(correct_result, result)

    def test_resize_second_edge_shorter(self):
        input_image = np.zeros((10, 6))
        size = 3
        correct_result = np.zeros((5, 3))
        result = resize_by_short_edge(input_image, size)
        np.testing.assert_array_equal(correct_result, result)
