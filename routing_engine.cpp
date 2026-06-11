#include <iostream>
#include <fstream>
#include <vector>
#include <queue>    // Added for the VIP line (Priority Queue)
#include <cmath>    // Added for math (Distance calculation)
#include "json.hpp"

using json = nlohmann::json;

struct Banana {
    int id;
    double age;
    int x, y;

    // This tells C++ how to compare two bananas
    // The "Oldest" banana wins and goes to the front of the line
    bool operator<(const Banana& other) const {
        return age < other.age; 
    }
};

// Simple math to find distance between two points
double calculate_distance(int x1, int y1, int x2, int y2) {
    return std::sqrt(std::pow(x2 - x1, 2) + std::pow(y2 - y1, 2));
}

int main() {
    std::ifstream file("warehouse_data.json");
    json data;
    file >> data;

    // 1. Create our "VIP Line" (Priority Queue)
    std::priority_queue<Banana> vip_line;

    // 2. Load bananas into the VIP Line
    for (auto& item : data["inventory"]) {
        vip_line.push({
            item["id"],
            item["age"],
            item["shelf_pos"][0],
            item["shelf_pos"][1]
        });
    }

    std::cout << "--- DAY 8: ROUTING STRATEGY ---" << std::endl;

    // 3. Process the top 5 most URGENT bananas
    for(int i = 0; i < 5; i++) {
        Banana urgent = vip_line.top(); // Get the oldest
        vip_line.pop();                // Remove it from the line

        // Find distance to "Store A" (located at 10, 80)
        double dist = calculate_distance(urgent.x, urgent.y, 10, 80);

        std::cout << "Assigning Banana #" << urgent.id 
                  << " (Age: " << urgent.age << " days) "
                  << "to Truck 1. Distance to Store A: " << dist << "m" << std::endl;
    }

    return 0;
}