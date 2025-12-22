#include "asio.hpp"
#include <iostream>
#include <cstdint>
#include <string>
#include <vector>
#include "../buffer_utils.hpp"
const int port_num = 27003;
const std::string student_id = "23021639";
using asio::ip::tcp;

void send_packet(tcp::socket& socket, uint32_t type, uint32_t len, const std::vector<byte>& data)
{
	std::vector<asio::const_buffer> bufs;
	bufs.push_back(asio::buffer(&type, sizeof(type)));
	bufs.push_back(asio::buffer(&len, sizeof(len)));
	bufs.push_back(asio::buffer(data));
	asio::write(socket, bufs);
}



bool is_prime(uint32_t n)
{
	for (uint32_t i = 2; i * i <= n; i++)
	{
		if (n % i == 0)
			return false;
	}
	return true;
}
void calc(tcp::socket& socket, asio::mutable_buffer& buf)
{
	uint32_t n;
	buf >> n;
	while (!is_prime(++n));
	send_packet(socket, 2, 4, std::vector<byte>(reinterpret_cast<byte*>(&n), reinterpret_cast<byte*>(&n) + sizeof(n)));
}

void send_hello(tcp::socket& socket)
{
	send_packet(socket, 0, student_id.size(), std::vector<byte>(student_id.begin(), student_id.end()));
}	

int main() {
	asio::io_context context;
	tcp::socket socket(context);

	std::cout << "Connecting to server" << std::endl;
	socket.connect(tcp::endpoint(asio::ip::make_address("112.137.129.129"), port_num));
	std::cout << "Connected" << std::endl;

	send_hello(socket);
	
	std::cout << "Sent hello message" << std::endl;
	int question = 0;
	while (1)
	{
		uint32_t type, len;
		asio::mutable_buffer buf = asio::buffer(&type, sizeof(type));
		asio::error_code ec;

		asio::read(socket, buf, ec);

		if (ec == asio::error::eof)
		{
			std::cout << "Server close connection" << std::endl;
			return 1;
		}
		buf = asio::buffer(&len, sizeof(len));
		asio::read(socket, buf), ec);
		if (ec == asio::error::eof)
		{
			std::cout << "Server close connection" << std::endl;
			return 1;
		}
		std::vector<byte> data(len);
		buf = asio::buffer(data, len);
		asio::read(socket, buf, ec);
		if (ec == asio::error::eof)
		{
			std::cout << "Server close connection" << std::endl;
			return 1;
		}
		switch (type)
		{
		case 1:
			calc(socket, buf);
			break;
		case 3:
			std::cout << "Server reject our answer" << std::endl;
			return 1;
			break;
		case 4:
			std::cout << "Server accept our answer, flag:" << std::endl;
			std::cout << std::string(data.begin(), data.end()) << std::endl;
			return 0;
			break;
		default:
			std::cout << "Unknow type, or server say hello back, type: " << type << std::endl;
			std::cout << std::string(data.begin(), data.end()) << std::endl;
			break;
		}
	}
}

