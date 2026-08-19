# How to Check for Windows 11 and WSL Capability

To determine if a laptop is running **Windows 11** and is fully capable of activating and running the **Windows Subsystem for Linux (WSL)**, you can check the operating system version, hardware virtualization settings, and system features using a few quick steps.

---

### Step 1: Verify Windows 11
1. Press the **Windows Key + R** to open the Run dialog
   or open a Windows PowerShell terminal.
2. Type `winver` and press **Enter**.
3. A window will pop up showing your Windows version.
   Ensure it states **Windows 11** (along with a specific version/build number like 23H2 or 24H2).

>**Note:** This should work for editions of Windows 11
>— Home, Pro, Enterprise — support WSL and previous version like Windows 10, 9, etc.<br>
>**Note:** While Windows 10 also supports WSL 2, Microsoft officially introduced the wsl
>-- install simplified installation command in later updates of Windows 10 Version 2004 and higher;
>older Windows 10 builds required enabling the optional features and downloading the Linux kernel package manually).

---

### Step 2: Check Hardware Virtualization Support
WSL 2 relies on Microsoft’s Virtual Machine Platform, which requires hardware-assisted virtualization (Intel VT-x or AMD-V) to be enabled in the laptop's BIOS/UEFI.

1. Press **Ctrl + Shift + Esc** to open the **Task Manager**.
2. Click on the **Performance** tab on the left sidebar, then select **CPU**.
3. Look at the bottom right information pane for **Virtualization**.
4. It must say **Enabled**.
   * *If it says Disabled*, you will need to restart your laptop, enter the BIOS/UEFI settings during boot, and turn on Intel Virtualization Technology or AMD-SVM.

---

### Step 3: Check or Activate WSL
The easiest way to test if WSL is ready or can be activated is straight from the command line:

1. Right-click the Start menu and select **Terminal (Admin)** or **PowerShell (Admin)**.
2. Run the following command:

   ```powershell
   wsl --install
