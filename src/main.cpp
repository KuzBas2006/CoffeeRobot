#include <iostream>
#include "httplib.h"
#include "nlohmann/json.hpp"
#include <thread>
#include <chrono>
#include <map>
#include "bot_gpio.h"

using json = nlohmann::json;
using namespace httplib;

int main() {
    httplib::Server svr;

    svr.Post("/commands", [](const httplib::Request& req, httplib::Response& res) {
        if (req.get_header_value("Content-Type") != "application/json") {
            res.status = 415;
            res.set_content("Unsupported Content-Type. Expected application/json", "text/plain");
            return;
        }

        try {
            json request_json = json::parse(req.body);
            std::string command = request_json.value("command", "");
            int duration = request_json.value("duration", 0);

            // Исправлен синтаксис map
            std::map<std::string, void(*)()> funcs;
            funcs["FORWARD/ms"] = robot_forward;
            funcs["RIGHT/ms"] = robot_right;
            funcs["LEFT/ms"] = robot_left;
            funcs["STOP"] = robot_stop;

            // Проверяем, существует ли команда
            if (funcs.find(command) != funcs.end()) {
                funcs[command]();  // Выполняем команду
                std::cout << "[ROBOT] " << command << " executed." << std::endl;

                // Если задана длительность и команда не STOP, запускаем авто-стоп
                if (duration > 0 && command != "STOP") {
                    std::thread([duration]() {
                        std::this_thread::sleep_for(std::chrono::milliseconds(duration));
                        robot_stop();
                        std::cout << "[ROBOT] Auto-stop after " << duration << " ms\n";
                    }).detach();
                }

                json response_json;
                response_json["command"] = command;
                response_json["status"] = "success";
                res.set_content(response_json.dump(), "application/json");
                res.status = 200;
            } else {
                res.status = 400;
                res.set_content("Unknown command: " + command, "text/plain");
            }

        } catch (const json::parse_error& e) {
            res.status = 400;
            res.set_content("Invalid JSON format: " + std::string(e.what()), "text/plain");
        }
    });

    std::cout << "Server listening on http://192.168.1.101:8080" << std::endl;
    svr.listen("192.168.1.101", 8080);

    robot_gpio_cleanup();
    return 0;
}