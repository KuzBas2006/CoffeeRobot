import cv2
import numpy as np
import math
import time
from processState import process_state
import json

last_sent = 0.0

class QRCode:
    def __init__(self, text, center, pts):
        self.text = text
        self.center = center
        self.pts = pts
        self.role = self._detect_role()
        self.last_seen = time.time()

    def _detect_role(self):
        if 'front' in self.text.lower() or 'перед' in self.text.lower():
            return 'front'
        elif 'back' in self.text.lower() or 'зад' in self.text.lower():
            return 'back'
        elif 'object' in self.text.lower() or 'объект' in self.text.lower() or 'target' in self.text.lower():
            return 'object'
        return 'unknown'


class GeometryCalculator:
    def midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def angle_between_lines(self, line1_p1, line1_p2, line2_p1, line2_p2):
        # Вектор направления робота
        robot_dir = (line1_p1[0] - line1_p2[0], line1_p1[1] - line1_p2[1])
        # Вектор от робота до цели
        to_target = (line2_p2[0] - line2_p1[0], line2_p2[1] - line2_p1[1])

        robot_angle = math.atan2(robot_dir[1], robot_dir[0])
        target_angle = math.atan2(to_target[1], to_target[0])

        diff = target_angle - robot_angle
        diff = math.degrees(diff)

        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        return diff  # Положительный = против часовой, отрицательный = по часовой

    def angle_between_points(self, p1, p2):
        return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))


class RobotCalculator:
    def __init__(self):
        self.front_qr = None
        self.back_qr = None
        self.object_qr = None
        self.geom = GeometryCalculator()
        self.smooth_center = None
        self.smooth_object = None
        self.alpha = 0.7
        self.timeout = 1.0

    def update_qr_codes(self, qr_codes):
        current_time = time.time()

        for qr in qr_codes:
            if qr.role == 'front':
                self.front_qr = qr
            elif qr.role == 'back':
                self.back_qr = qr
            elif qr.role == 'object':
                self.object_qr = qr

        if self.front_qr and current_time - self.front_qr.last_seen > self.timeout:
            self.front_qr = None
        if self.back_qr and current_time - self.back_qr.last_seen > self.timeout:
            self.back_qr = None
        if self.object_qr and current_time - self.object_qr.last_seen > self.timeout:
            self.object_qr = None

    def has_all_three(self):
        return self.front_qr is not None and self.back_qr is not None and self.object_qr is not None

    def get_robot_center(self):
        if self.front_qr and self.back_qr:
            raw = self.geom.midpoint(self.front_qr.center, self.back_qr.center)
            if self.smooth_center is None:
                self.smooth_center = raw
            else:
                x = int(self.smooth_center[0] * self.alpha + raw[0] * (1 - self.alpha))
                y = int(self.smooth_center[1] * self.alpha + raw[1] * (1 - self.alpha))
                self.smooth_center = (x, y)
            return self.smooth_center
        return None

    def get_object_center(self):
        if self.object_qr:
            raw = self.object_qr.center
            if self.smooth_object is None:
                self.smooth_object = raw
            else:
                x = int(self.smooth_object[0] * self.alpha + raw[0] * (1 - self.alpha))
                y = int(self.smooth_object[1] * self.alpha + raw[1] * (1 - self.alpha))
                self.smooth_object = (x, y)
            return self.smooth_object
        return None

    def get_distance_to_object(self):
        robot = self.get_robot_center()
        obj = self.get_object_center()
        if robot and obj:
            return self.geom.distance(robot, obj)
        return None

    def get_angle_to_object(self):
        if not self.has_all_three():
            return None
        robot_center = self.get_robot_center()
        object_center = self.get_object_center()
        if robot_center and object_center:
            robot_line = (self.front_qr.center, self.back_qr.center)
            target_line = (robot_center, object_center)
            return self.geom.angle_between_lines(
                robot_line[0], robot_line[1],
                target_line[0], target_line[1]
            )
        return None


class QRScanner:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()
        self.robot = RobotCalculator()
        self.last_output = ""

    def print_results(self, robot_center, object_center, distance, angle):
        output = f"""========================================
Центр робота: {robot_center}
Центр цели: {object_center}
Расстояние до цели: {int(distance)} px
Угол до цели: {int(angle)}°
========================================"""
        if output != self.last_output:
            self.last_output = output
            print(output)

    def run(self):
        global last_sent
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            print("Ошибка: камера не найдена")
            return None

        print("Сканирование запущено. Нажмите Q для выхода.")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            retval, texts, points, _ = self.detector.detectAndDecodeMulti(frame)
            qr_objects = []

            if retval and points is not None:
                for i, text in enumerate(texts):
                    if text:
                        pts = points[i].astype(int)
                        center_x = sum(p[0] for p in pts) // 4
                        center_y = sum(p[1] for p in pts) // 4
                        qr = QRCode(text, (center_x, center_y), pts)
                        qr_objects.append(qr)

                        if qr.role == 'front':
                            color = (0, 255, 0)
                            label = "FRONT"
                        elif qr.role == 'back':
                            color = (0, 0, 255)
                            label = "BACK"
                        elif qr.role == 'object':
                            color = (255, 0, 0)
                            label = "TARGET"
                        else:
                            color = (255, 255, 0)
                            label = "QR"

                        cv2.polylines(frame, [pts], True, color, 2)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                        cv2.putText(frame, label, (center_x - 30, center_y - 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            self.robot.update_qr_codes(qr_objects)

            if self.robot.front_qr and self.robot.back_qr:
                cv2.line(frame, self.robot.front_qr.center, self.robot.back_qr.center, (0, 255, 255), 3)

            robot_center = self.robot.get_robot_center()
            object_center = self.robot.get_object_center()

            if robot_center:
                cv2.circle(frame, robot_center, 10, (0, 255, 255), -1)
                cv2.putText(frame, "ROBOT", (robot_center[0] - 30, robot_center[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

            if object_center:
                cv2.circle(frame, object_center, 10, (255, 0, 0), -1)
                cv2.putText(frame, "TARGET", (object_center[0] - 30, object_center[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

            if robot_center and object_center:
                cv2.line(frame, robot_center, object_center, (255, 0, 0), 2)

            cv2.putText(frame, f"CODES: {len([q for q in qr_objects if q.text])}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if self.robot.has_all_three():
                cv2.putText(frame, "READY", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                distance = self.robot.get_distance_to_object()
                angle = self.robot.get_angle_to_object()
                time_diff = time.time() - last_sent
                if distance and angle and time_diff > 0.5:
                    self.print_results(robot_center, object_center, distance, angle)
                    data = {
                        "angle": angle,
                        "distance": distance
                    }
                    json_string = json.dumps(data)

                    process_state(json_string)
                    last_sent = time.time()
            else:
                missing = []
                if not self.robot.front_qr: missing.append("FRONT")
                if not self.robot.back_qr: missing.append("BACK")
                if not self.robot.object_qr: missing.append("TARGET")
                cv2.putText(frame, f"WAITING: {' '.join(missing)}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

            cv2.putText(frame, "Q = exit", (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            cv2.imshow('QR Scanner', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return None


class App:
    def run(self):
        scanner = QRScanner()
        scanner.run()


if __name__ == "__main__":
    App().run()