#pragma once

#ifndef BUFFER_UTILS_HPP
#define BUFFER_UTILS_HPP

#include "asio.hpp"
#include <iostream>
#include <cstdint>
#include <string>
#include <vector>
#include <queue>
#include <array>



typedef uint8_t byte;

template <typename T>
union AnyBuffer {
	T value;
	byte buffer[sizeof(T)];

	AnyBuffer() {
		memset(buffer, 0, sizeof(T));
	}
	AnyBuffer(T value) : value(value) {}
	AnyBuffer(const std::vector<byte>& buffer) {
		memcpy(this->buffer, buffer.data(), sizeof(T));
	}
	AnyBuffer(const std::string& buffer) {
		memcpy(this->buffer, buffer.data(), sizeof(T));
	}
	AnyBuffer(const AnyBuffer<T>& other) {
		memcpy(buffer, other.buffer, sizeof(T));
	}

	std::string toString() const {
		std::string result;
		for (const byte& b : buffer) {
			result.push_back(b);
		}
		return result;
	}
};

template<typename T>
asio::mutable_buffer& operator >> (asio::mutable_buffer& buffer, T& var) {
	memcpy(&var, buffer.data(), sizeof(T));
	buffer += sizeof(T);
	return buffer;
}

size_t read_timeout(asio::ip::tcp::socket& socket, asio::mutable_buffer& buffer, asio::error_code& ec, std::chrono::seconds timeout) {
	size_t bytes_transferred = 0;
	std::thread read_thread([&]() {
		bytes_transferred = asio::read(socket, buffer, ec);
		});
	std::this_thread::sleep_for(timeout);
	if (read_thread.joinable()) {
		read_thread.join();
	}
	return bytes_transferred;
}

#endif