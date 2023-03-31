#!/usr/bin/env python3
# Copyright 2023 Georg Novotny
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from math import pi, sin, cos
from numpy import array
from numpy.linalg import norm
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from vision_msgs.msg import Detection3DArray
from vision_msgs.msg import Detection3D
from vision_msgs.msg import BoundingBox3D
from vision_msgs.msg import ObjectHypothesisWithPose


def quaternion_about_axis(angle, axis):
    axis = array(axis)
    axis = axis / norm(axis)
    half_angle = angle / 2
    sine = sin(half_angle)
    w = cos(half_angle)
    x, y, z = axis * sine
    return x, y, z, w


class pub_detection3_d_array(Node):
    def __init__(self):
        super().__init__("pub_detection3_d_array_sample")
        self.__pub = self.create_publisher(
            Detection3DArray, "detection3_d_array", 10)
        self.__timer = self.create_timer(0.1, self.pub_sample)
        self.__counter = 0
        self.__header = Header()
        self.__msg_def = {
            "score": [20.0, 40.0],
            "obj_id": ["human", "AMR"]
        }

    def create_msg(self, bbox: BoundingBox3D, scores, obj_ids) -> Detection3D:
        msg = Detection3D()
        msg.header = self.__header
        msg.bbox = bbox
        for score, obj_id in zip(scores, obj_ids):
            obj = ObjectHypothesisWithPose()
            obj.hypothesis.score = score
            obj.hypothesis.class_id = obj_id
            msg.results.append(obj)
        return msg

    def pub_sample(self):
        while self.__pub.get_subscription_count() == 0:
            return
        self.__header.stamp = self.get_clock().now().to_msg()
        self.__header.frame_id = "map"
        msg = Detection3DArray()
        msg.header = self.__header

        bbox_human = BoundingBox3D()
        if self.__counter >= 200:
            self.__counter=0

        bbox_human.center.orientation.x = 0.0 
        bbox_human.center.orientation.y = 0.0 
        bbox_human.center.orientation.z = 0.0
        bbox_human.center.orientation.w = 1.0


        if self.__counter < 50:
            bbox_human.center.position.x = 0. + 0.1*self.__counter
            bbox_human.center.position.y = 0. 
        elif self.__counter < 100:
            bbox_human.center.position.x = 5.0
            bbox_human.center.position.y = -5.0 + 0.1*self.__counter
        elif self.__counter < 150:
            bbox_human.center.position.x = 15.0 - 0.1*self.__counter
            bbox_human.center.position.y = 5.0 
        elif self.__counter < 200:
            bbox_human.center.position.x = 0. 
            bbox_human.center.position.y = 20.0 - 0.1*self.__counter

        bbox_human.size.x = 0.8
        bbox_human.size.y = 0.6
        bbox_human.size.z = 1.9
        bbox_human.center.position.z = bbox_human.size.z *0.5
        score = 20.0
        obj_id = "human"
        

        detection_msg = self.create_msg(
            bbox=bbox_human, scores=[score], obj_ids=[obj_id]
        )
        msg.detections.append(detection_msg)



        bbox_amr = BoundingBox3D()
        quat_amr = [0,0,0,1]
        bbox_amr.center.orientation.x = 0.0
        bbox_amr.center.orientation.y = 0.0
        bbox_amr.center.orientation.z = 0.0
        bbox_amr.center.orientation.w = 1.0

        if self.__counter < 50:
            bbox_amr.center.position.x = 0. + 0.2*self.__counter -1.
            bbox_amr.center.position.y = -3.0
        elif self.__counter < 100:
            bbox_amr.center.position.x = 10.0 -1.0
            bbox_amr.center.position.y = -10.0 + 0.2*self.__counter -3.0
        elif self.__counter < 150:
            bbox_amr.center.position.x = 30.0 - 0.2*self.__counter -1.0
            bbox_amr.center.position.y = 10.0 -3.0
        elif self.__counter < 200:
            bbox_amr.center.position.x = 0.  -1.0
            bbox_amr.center.position.y = 40.0 - 0.2*self.__counter -3.0

        bbox_amr.size.x = 0.8
        bbox_amr.size.y = 0.6
        bbox_amr.size.z = 0.8
        bbox_amr.center.position.z = bbox_amr.size.z *0.5
        score = 40.0
        obj_id = "AMR"

        detection_msg = self.create_msg(
            bbox=bbox_amr, scores=[score], obj_ids=[obj_id]
        )
        msg.detections.append(detection_msg)
        self.__pub.publish(msg)
        self.__counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = pub_detection3_d_array()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
