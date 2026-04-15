import cv2
import numpy as np
import json
from datetime import datetime
import math

class QRCode:
    """Хранит данные одного QR-кода"""

    def __init__(self, text, center, pts):
        self.text = text
        self.center = center
        self.pts = pts
        self.role = self._detect_role()

    def _detect_role(self):
        # Определяет роль по тексту QR-кода
        if 'front' in self.text.lower() or 'перед' in self.text.lower():
            return 'front'
        elif 'back' in self.text.lower() or 'зад' in self.text.lower():
            return 'back'
        return 'unknown'

class GeometryCalculator:
    """Геометрические расчёты"""

    def midpoint(self, p1, p2):
        # Середина между двумя точками
        return ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

    def distance(self, p1, p2):
        # Расстояние между двумя точками
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def angle_between_points(self, p1, p2):
        # Угол между двумя точками (от горизонтали)
        return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

    def angle_between_lines(self, line1_p1, line1_p2, line2_p1, line2_p2):
        # Угол между двумя линиями
        v1 = (line1_p2[0] - line1_p1[0], line1_p2[1] - line1_p1[1])
        v2 = (line2_p2[0] - line2_p1[0], line2_p2[1] - line2_p1[1])

        dot = v1[0] * v2[0] + v1[1] * v2[1]
        len1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
        len2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

        return math.degrees(math.acos(dot / (len1 * len2)))

class RobotCalculator:
    """Расчёты для робота"""

    def __init__(self):
        self.front_qr = None
        self.back_qr = None
        self.robot_center = None
        self.geom = GeometryCalculator()

    def update_qr_codes(self, qr_codes):
        # Обновляет данные о QR-кодах робота
        self.front_qr = None
        self.back_qr = None

        for qr in qr_codes:
            if qr.role == 'front':
                self.front_qr = qr
            elif qr.role == 'back':
                self.back_qr = qr

    def has_both_qrs(self):
        # Проверяет, видны ли оба QR-кода
        return self.front_qr is not None and self.back_qr is not None

    def get_robot_center(self):
        # Возвращает центр между двумя QR-кодами
        if self.has_both_qrs():
            self.robot_center = self.geom.midpoint(
                self.front_qr.center,
                self.back_qr.center
            )
            return self.robot_center
        return None

    def get_robot_distance(self, target_center):
        # Расстояние от центра робота до цели
        if self.robot_center and target_center:
            return self.geom.distance(self.robot_center, target_center)
        return None

    def get_robot_angle_to_target(self, target_center):
        # Угол между линией робота и линией к цели
        if not self.has_both_qrs() or not target_center:
            return None

        robot_line = (self.front_qr.center, self.back_qr.center)
        target_line = (self.robot_center, target_center)

        return self.geom.angle_between_lines(
            robot_line[0], robot_line[1],
            target_line[0], target_line[1]
        )

class ExternalObject:
    """Получает данные о внешнем объекте из другой программы"""

    def get_target_center(self):
        # Получает центр объекта из другой программы
        try:
            with open("target_coords.json", "r") as f:
                data = json.load(f)
                return tuple(data.get('center', (None, None)))
        except:
            return None


class QRScanner:
    """Основной класс сканера"""

    def __init__(self):
        self.detector = cv2.QRCodeDetector()
        self.robot = RobotCalculator()
        self.external = ExternalObject()
        self.scanned_codes = []

    def correct_perspective(self, image, points):
        src_points = np.float32(points)
        dst_points = np.float32([[0, 0], [300, 0], [300, 300], [0, 300]])
        homography_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        corrected = cv2.warpPerspective(image, homography_matrix, (300, 300))
        return corrected, homography_matrix

    def draw_info(self, frame, qr_codes, target_center):
        # Рисует всю информацию на кадре

        # Счётчик QR-кодов
        cv2.putText(frame, f"QR codes: {len(qr_codes)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Информация о роботе
        if self.robot.has_both_qrs():
            robot_center = self.robot.get_robot_center()
            if robot_center:
                cv2.circle(frame, robot_center, 10, (0, 255, 255), -1)
                cv2.putText(frame, "CENTER", (robot_center[0] - 35, robot_center[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            # Расстояние между QR-кодами
            dist = self.robot.geom.distance(
                self.robot.front_qr.center,
                self.robot.back_qr.center
            )
            cv2.putText(frame, f"Length: {int(dist)} px", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Информация о цели
        if target_center:
            cv2.circle(frame, target_center, 8, (255, 0, 255), -1)
            cv2.putText(frame, "TARGET", (target_center[0] - 30, target_center[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

            # Расстояние до цели
            distance = self.robot.get_robot_distance(target_center)
            if distance:
                cv2.putText(frame, f"Distance: {int(distance)} px", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.line(frame, self.robot.robot_center, target_center, (255, 0, 255), 2)

            # Угол до цели
            angle = self.robot.get_robot_angle_to_target(target_center)
            if angle:
                cv2.putText(frame, f"Angle: {int(angle)} deg", (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Подсказка
        cv2.putText(frame, "Press Q", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    def run(self):
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

            # Поиск QR-кодов
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

                        # Визуализация QR-кода
                        if qr.role == 'front':
                            color = (0, 255, 0)
                            label = "FRONT"
                        elif qr.role == 'back':
                            color = (0, 0, 255)
                            label = "BACK"
                        else:
                            color = (255, 255, 0)
                            label = "QR"

                        cv2.polylines(frame, [pts], True, color, 2)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                        # Надпись НАД QR-кодом (сверху)
                        cv2.putText(frame, label, (center_x - 25, center_y - 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                        # Логирование нового QR-кода
                        if text not in self.scanned_codes:
                            self.scanned_codes.append(text)
                            print(f"Найден: {text} -> {qr.role}")

            # Обновляем данные робота
            self.robot.update_qr_codes(qr_objects)

            # Получаем координаты цели из другой программы
            target_center = self.external.get_target_center()

            # Рисуем линию между передним и задним QR-кодами
            if self.robot.has_both_qrs():
                cv2.line(frame, self.robot.front_qr.center, self.robot.back_qr.center, (255, 0, 0), 3)

            # Вся информация на экране
            self.draw_info(frame, qr_objects, target_center)

            cv2.imshow('QR Scanner', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return self.scanned_codes

class App:
    def run(self):
        scanner = QRScanner()
        results = scanner.run()

        if results:
            print(f"\nВсего найдено QR-кодов: {len(results)}")
            for code in results:
                print(f"  {code}")
        else:
            print("QR-коды не найдены")


if __name__ == "__main__":
    App().run()