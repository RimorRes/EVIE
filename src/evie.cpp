//
// Created by maxim on 05/09/2025.
//

#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <cstdint>

#include "../include/evie.h"

// Convert from the X1202 formula used in Python
double readVoltage(const int file) {
    constexpr uint8_t reg = 0x02; // register for voltage
    if (write(file, &reg, 1) != 1) { perror("Write reg"); return -1; }

    uint8_t buf[2];
    if (read(file, buf, 2) != 2) { perror("Read voltage"); return -1; }

    const uint16_t raw = (buf[0] << 8) | buf[1];        // big endian from the device
    const double voltage = raw * 1.25 / 1000 / 16;
    return voltage;
}

double readCapacity(const int file) {
    constexpr uint8_t reg = 0x04; // register for capacity
    if (write(file, &reg, 1) != 1) { perror("Write reg"); return -1; }

    uint8_t buf[2];
    if (read(file, buf, 2) != 2) { perror("Read capacity"); return -1; }

    const uint16_t raw = (buf[0] << 8) | buf[1];
    const double capacity = raw / 256.0;
    return capacity;
}

std::string getBatteryStatus(const double voltage) {
    if (voltage >= 3.87 && voltage <= 4.2) return "Full";
    if (voltage >= 3.7) return "High";
    if (voltage >= 3.55) return "Medium";
    if (voltage >= 3.4) return "Low";
    if (voltage < 3.4) return "Critical";
    return "Unknown";
}

int main() {
    const auto dev = "/dev/i2c-1";
    const int file = open(dev, O_RDWR);
    if (file < 0) { perror("Open I2C"); return 1; }

    if (constexpr int addr = 0x36; ioctl(file, I2C_SLAVE, addr) < 0) { perror("ioctl"); return 1; }

    const double voltage = readVoltage(file);
    const double capacity = readCapacity(file);
    const std::string status = getBatteryStatus(voltage);

    std::cout << "Voltage: " << voltage << " V" << std::endl;
    std::cout << "Capacity: " << capacity << " % (" << status << ")" << std::endl;

    close(file);
    return 0;
}
