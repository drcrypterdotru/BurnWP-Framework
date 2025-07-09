# 🔥 BurnWP Framework v1.0.0 💥

🌐 **Logo BurnWP-Framework 1.0.0**  
 ![Logo](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/logo.png)


## 📌 Introduction

We are proud to announce the release of **BurnWP Framework v1.0.0** — a powerful WordPress auto-exploitation tool built with a custom plugin for practical and effective penetration testing.

Unlike traditional vulnerability scanners that only detect potential issues, **BurnWP Framework** is designed to actively exploit known WordPress CVEs and gain shell access when possible.  
This makes it a valuable tool for security professionals who need results, not just reports.  
Version 1.0.0 focuses exclusively on WordPress vulnerabilities and is optimized for Windows users, offering a simple user interface for configuration and execution.  
This is just the beginning—expect more CMS support and advanced modules in future versions.

---


## 🚀 Features – BurnWP Framework v1.0.0

BurnWP Framework is designed for offensive security professionals who want more than just scanning—it provides real-world exploitation capabilities, a modular plugin system, and an intuitive user interface.

### ✅ 1. Mass Exploitation Using `Target_Lists.txt`

Run exploitation against multiple targets listed in `Target_Lists.txt` (one URL per line).

> **INFO:**  
> To fully utilize the framework, enable the following in `ui_config`:
> - CVE Exploiter  
> - LFI Scanner  
> - Plugin Exploiter  

When combined, these modules provide powerful exploitation capabilities across multiple attack vectors.

## 📷 DEMO Screenshot :


🌐 **command attack with lists.txt**  
 ![command attack with lists.txt](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/refs/heads/main/demo/attack_targets.txt.png)

 ![full screen](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/attack_targets.txt_full.png)


🌐 **Exploit & Success Accessed**  
 ![full screen](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/demo_shell_access.png)

---

### ✅ 2. Single Plugin with Bulk Targets

Select a specific plugin from `Plugin_Lists` and test it against a list of targets in `Lists.txt`.

> **Use Case:** Ideal for testing your favorite plugin against multiple websites (e.g., your own domains or local environments).

---

### ✅ 3. Single Plugin with Single Target

Test one specific plugin exploit against a single target domain.

> **Use Case:** 1-to-1 plugin testing — great for precision testing or local development.

🌐 **Demo Command with Single Target**  

 ![show plugins](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/list_plugin_targets.png)

 ![selection plugins](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/plugin_with_per_target.png)


---

### 🛠️ 4. Developer Mode – Build Your Own Plugins

Create and drop your own custom exploit plugins into the `Plugins_Exploiter/` directory.  
Simply run BurnWP using `install_plugin`, and your plugin will be:

- ✅ Loaded in real time  
- ✅ Validated for structure and errors  
- ✅ Debugged live with error notifications  

> **INFO:**
> - Supports WordPress CVEs and any other CVE-based web application exploits, including PHP, Laravel, etc.  
> - Use the `Plugin_BurnWP()` function as the entry point, similar to a `main()` function.  
> - Supports both GET and POST methods via prebuilt `Shell_Loader` forms.  
> - A full tutorial will be provided in future releases.

🌐 **Plugin Install & Listening in Real-Times**  
 ![UI Image](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/install_plugin.png)

---

### ⚙️ 5. User-Friendly Interface for Configuration

Configure BurnWP via a simple UI or directly by editing `Config/config.json`.

> **INFO:**  
> Enable or disable features with:  
> ```json
> "Enable": True  
> "Disable": False
> ```
> All modules are toggleable via the `ui_config` interface for quick adjustments.

🌐 **UI Config**  
 ![UI Image](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/ui.png)

 ![Full Settings](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/ui_2.png)
---
show_cve_info.png
### 📚 6. CVE Database Overview (Built-In)

BurnWP includes a detailed CVE index that gives you full visibility into available exploits:

| **Field**       | **Description**                                      |
|------------------|------------------------------------------------------|
| ID               | Total number of available exploits                   |
| Title            | Name of the exploit                                  |
| CVE              | CVE ID (e.g., CVE-2024-XXXX)                         |
| Severity         | Rating (Critical, High, 7.5, etc.)                   |
| Public Date      | When the exploit was publicly released               |
| CVE Date         | Year the CVE was registered                          |
| Description      | Type of vulnerability (e.g., RCE, LFI, SQLi)         |
| Source           | Whether from core built-in tools or external plugins |
| Plugin CVE       | Shows if related to a plugin CVE                     |
| Technology       | Target platform (e.g., WordPress, Laravel, PHP, etc.)|


 ![CVE Information Details](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/show_cve_info.png)


---

## 📥 Requirements and Installation

1. ✅ Download and install **Python 3.12 or the latest version**:  
   👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. ✅ Clone this repository:
```bash
git clone https://github.com/drcrypterdotru/BurnWP-Framework.git
cd BurnWP-Framework
```

<details>
<summary>🪟 How to Install on Windows</summary>

```bash
Option 1 — Manual installation
python3 -m pip install -r requirements.txt
python3 main.py

Option 2 — One-click installer
setup.bat
python3 main.py
```
</details>

<details>
<summary>🐧 How to Install on Linux</summary>

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```
</details>

<details>
<summary>🍎 How to Install on macOS</summary>

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```


</details>



<div style="text-align: center;">

🌐 **BurnWP Diagram**  
 ![BurnWP Diagram](https://raw.githubusercontent.com/drcrypterdotru/BurnWP-Framework/main/demo/BurnWP_Diagram.png)

## More Tools on Forums

Explore our community and connect with us on visit our website for more Tools and Resources!

[![Website](https://drcrypter.ru/data/assets/logo/logo1.png)](https://drcrypter.ru)

---

## 🤝 Contributing

We welcome contributions! Feel free to fork this repository, make enhancements, and open pull requests. Please check the [issues](#) page for ongoing tasks or bug reports.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

> ⚠️ **Disclaimer**: This tool is for educational purposes only. 🏫 The creator and contributors are not responsible for any misuse or damages caused. Use responsibly, and only on systems you own or have permission for. ✅

---