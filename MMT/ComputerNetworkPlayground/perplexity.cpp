#define a
#include <boost/asio.hpp>
#include <iostream>
#include <string>

using asio::ip::tcp;

void send_packet(tcp::socket& socket, int32_t type, const std::vector<uint8_t>& data) {
    // Send header
    int32_t len = data.size();
    asio::write(socket, asio::buffer(&type, 4));
    asio::write(socket, asio::buffer(&len, 4));
    
    // Send data
    if (!data.empty()) {
        asio::write(socket, asio::buffer(data));
    }
}

int main() {
    asio::io_context io_context;
    tcp::socket socket(io_context);
    socket.connect(tcp::endpoint(asio::ip::address::from_string("112.137.129.129"), 27001));

    // Send PKT_HELLO
    std::string student_code = "21127014"; // Replace with your code
    send_packet(socket, 0, std::vector<uint8_t>(student_code.begin(), student_code.end()));

    while (true) {
        // Read header
        int32_t type, len;
        asio::read(socket, asio::buffer(&type, 4));
        asio::read(socket, asio::buffer(&len, 4));
        
        // Read data
        std::vector<uint8_t> data(len);
        if (len > 0) {
            asio::read(socket, asio::buffer(data));
        }

        switch (type) {
            case 1: { // PKT_CALC
                int32_t a = *reinterpret_cast<int32_t*>(data.data());
                int32_t b = *reinterpret_cast<int32_t*>(data.data() + 4);
                int32_t result = a + b;
                send_packet(socket, 2, std::vector<uint8_t>(
                    reinterpret_cast<uint8_t*>(&result),
                    reinterpret_cast<uint8_t*>(&result) + 4
                ));
                break;
            }
            case 3: // PKT_BYE
                return 0;
            case 4: // PKT_FLAG
                std::cout << "Flag: " << std::string(data.begin(), data.end()) << "\n";
                return 0;
        }
    }
}
