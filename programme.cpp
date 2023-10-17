#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <directory_path>" << std::endl;
        return 1;
    }

    std::string directory_path = argv[1];

    if (!fs::is_directory(directory_path)) {
        std::cerr << "Error: The specified path is not a directory." << std::endl;
        return 1;
    }

    // Create a subdirectory for the text files if it doesn't exist
    std::string output_directory = directory_path + "/text_output";
    if (fs::exists(output_directory)) {
        fs::remove_all(output_directory);
    }
    fs::create_directory(output_directory);

    std::vector<std::string> pdf_files;

    // Find all PDF files in the specified directory
    for (const auto& entry : fs::directory_iterator(directory_path)) {
        if (entry.is_regular_file() && entry.path().extension() == ".pdf") {
            pdf_files.push_back(entry.path().string());
        }
    }

    if (pdf_files.empty()) {
        std::cerr << "No PDF files found in the specified directory." << std::endl;
        return 1;
    }

    int option;
    std::cout << "Choose an option (1-3): ";
    std::cin >> option;

    if (option < 1 || option > 3) {
        std::cerr << "Invalid option. Please choose between 1 and 3." << std::endl;
        return 1;
    }

    for (const std::string& pdf_file : pdf_files) {
        std::string pdf_name = fs::path(pdf_file).filename();
        std::string txt_output_file = output_directory + "/" + pdf_name + ".txt";

        std::string pdftotext_command = "pdftotext";
        if (option == 2) {
            pdftotext_command += " -layout";
        } else if (option == 3) {
            pdftotext_command += " -raw";
        }

        pdftotext_command += " \"" + pdf_file + "\" \"" + txt_output_file + "\"";

        int result = std::system(pdftotext_command.c_str());

        if (result == 0) {
            std::cout << "Converted " << pdf_name << " to text." << std::endl;
        } else {
            std::cerr << "Error converting " << pdf_name << " to text." << std::endl;
        }
    }

    return 0;
}