#include <iostream>
#include "httplib.h"
#include "nlohmann/json.hpp"


using json = nlohmann::json;
using namespace httplib;


int main() {
    Server svr;

    svr.Post("/api/data", [](const Request& req, Response& res) {
        try {
            json received = json::parse(req.body);
            std::cout << "Получено: " << received.dump(4) << std::endl;

            json response_data;
            response_data["status"] = "ok";
            response_data["echo"] = received;

            res.set_content(response_data.dump(), "application/json");
            res.status = 200;
        } catch (const std::exception& e) {
            json error_response;
            error_response["status"] = "error";
            error_response["message"] = e.what();
            res.status = 400;
            res.set_content(error_response.dump(), "application/json");
        }
    });

    std::cout << "Server is active on http://localhost:8080" << std::endl;
    svr.listen("localhost", 8080);

    return 0;
}