#include <windows.h>
#include <stdio.h>

__thread int tls_var;               // triggers TLS Table
int global_var = 42;                // triggers data section, relocations

// Function to export symbols in GCC (simulates Export Table)
__attribute__((visibility("default"))) void my_exported_function() {
    printf("Exported function\n");
}

// Main function
int main() {
    // Trigger Import Table / IAT
    MessageBoxA(NULL, "Hi", "Test", MB_OK);

    // Trigger TLS usage
    tls_var = 123;

    // Trigger relocation (by using a global variable)
    global_var += 1;

    // Call the "exported" function
    my_exported_function();

    return 0;
}
