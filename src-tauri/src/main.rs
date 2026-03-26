use tauri::{Manager, Emitter};
use std::process::{Command};
use std::thread;
use std::io::{Write, Read};
use std::net::TcpListener;
use std::fs::OpenOptions;
use std::path::Path;
use std::fs;

// 读取配置文件获取快捷键设置
fn get_configured_hotkey() -> String {
    let config_path = "/Users/jszpc/Desktop/快捷总结笔记/config/config.yaml";
    if let Ok(content) = fs::read_to_string(config_path) {
        // 简单解析 YAML 提取 hotkey
        for line in content.lines() {
            if line.starts_with("hotkey:") {
                let value = line.replace("hotkey:", "").trim().to_string();
                if !value.is_empty() {
                    return value;
                }
            }
        }
    }
    "f2".to_string()  // 默认快捷键
}

#[tauri::command]
fn get_notes_dir() -> Result<String, String> {
    let notes_dir = std::path::PathBuf::from("/Users/jszpc/Desktop/快捷总结笔记/logs");
    Ok(notes_dir.to_string_lossy().to_string())
}

#[tauri::command]
fn start_api_server() -> Result<String, String> {
    let _child = Command::new("python3")
        .arg("api_server.py")
        .current_dir("/Users/jszpc/Desktop/快捷总结笔记")
        .spawn()
        .map_err(|e| format!("启动失败: {}", e))?;

    std::thread::sleep(std::time::Duration::from_secs(2));
    Ok("API服务器已启动".to_string())
}

#[tauri::command]
fn summarize_once() -> Result<String, String> {
    let output = Command::new("python3")
        .arg("src/main.py")
        .arg("--once")
        .current_dir("/Users/jszpc/Desktop/快捷总结笔记")
        .output()
        .map_err(|e| format!("执行失败: {}", e))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

// 记录删除日志
fn log_deletion(note_name: &str) {
    let log_path = "/Users/jszpc/Desktop/快捷总结笔记/logs/delete_log.txt";
    let timestamp = get_timestamp();
    let log_entry = format!("[{}] 删除了笔记: {}\n", timestamp, note_name);

    if let Ok(mut file) = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_path)
    {
        let _ = file.write_all(log_entry.as_bytes());
    }
}

fn get_timestamp() -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let secs = now as i64;
    // 手动格式化时间
    let days = secs / 86400;
    let remaining = secs % 86400;
    let hours = remaining / 3600;
    let minutes = (remaining % 3600) / 60;
    let seconds = remaining % 60;

    // 简单计算日期（从 1970-01-01 开始）
    let year = 1970 + days / 365;
    let remaining_days = days % 365;
    let month = remaining_days / 30 + 1;
    let day = remaining_days % 30 + 1;

    format!("{:04}-{:02}-{:02} {:02}:{:02}:{:02}", year, month, day, hours, minutes, seconds)
}

#[tauri::command]
fn get_notes_list() -> Result<Vec<serde_json::Value>, String> {
    use std::fs;
    use std::path::Path;

    let notes_dir = Path::new("/Users/jszpc/Desktop/快捷总结笔记/logs");
    let mut notes = Vec::new();
    let mut index = 1;  // 笔记编号从1开始

    if let Ok(entries) = fs::read_dir(notes_dir) {
        for entry in entries.flatten() {
            if let Ok(metadata) = entry.metadata() {
                if metadata.is_file() {
                    let path = entry.path();
                    if path.extension().map_or(false, |ext| ext == "md") {
                        // 读取文件内容来提取标题和预览
                        let mut title = String::new();
                        let mut preview = String::new();

                        if let Ok(content) = fs::read_to_string(&path) {
                            // 提取 markdown 代码块中的内容
                            let in_code_block = content.contains("```markdown");
                            let content_inside = if in_code_block {
                                let start = content.find("```markdown").map_or(0, |p| p + 11);
                                let end = content[start..].find("```").map_or(content.len(), |p| p + start);
                                &content[start..end]
                            } else {
                                &content
                            };

                            let lines: Vec<&str> = content_inside.lines().collect();

                            // 查找标题 - 跳过通用标题
                            let skip_titles = ["完成的任务", "已完成的任务", "任务完成", "会话总结", "执行的命令", "修改的文件", "问题与解决方案", "关键决策"];

                            for line in &lines[..lines.len().min(30)] {
                                let trimmed = line.trim();
                                if trimmed.starts_with("## ") && !trimmed.replace("## ", "").trim().is_empty() {
                                    let potential_title = trimmed.replace("## ", "").trim().to_string();
                                    if !skip_titles.iter().any(|&s| s == potential_title) {
                                        title = potential_title;
                                        break;
                                    }
                                }
                            }

                            // 如果没找到有意义的标题，尝试使用第一行的内容
                            if title.is_empty() {
                                for line in &lines[..5] {
                                    let trimmed = line.trim();
                                    // 跳过空行、标题、特殊标记
                                    if !trimmed.is_empty()
                                        && !trimmed.starts_with('#')
                                        && !trimmed.starts_with("**")
                                        && !trimmed.starts_with("---")
                                        && !trimmed.starts_with('*')
                                        && trimmed.len() > 5
                                    {
                                        // 取前30个字符作为标题
                                        let char_count = trimmed.chars().count().min(20);
                                        title = trimmed.chars().take(char_count).collect::<String>();
                                        break;
                                    }
                                }
                            }

                            // 如果还是没有标题，使用文件名
                            if title.is_empty() {
                                title = path.file_name().unwrap().to_string_lossy().to_string();
                            }

                            // 查找预览 - 跳过代码块和标题
                            let mut in_code = false;
                            for line in &lines {
                                let trimmed = line.trim();
                                if trimmed.starts_with("```") {
                                    in_code = !in_code;
                                    continue;
                                }
                                if in_code {
                                    continue;
                                }
                                if !trimmed.is_empty() && !trimmed.starts_with('#') && !trimmed.starts_with("**") && !trimmed.starts_with("---") && !trimmed.starts_with('*') && trimmed.len() > 10 {
                                    // 安全地截取中文字符串
                                    let char_count = trimmed.chars().count().min(50);
                                    preview = trimmed.chars().take(char_count).collect::<String>();
                                    break;
                                }
                            }
                        }

                        notes.push(serde_json::json!({
                            "id": index,
                            "name": path.file_name().unwrap().to_string_lossy(),
                            "path": path.to_string_lossy(),
                            "title": title,
                            "preview": preview,
                            "size": metadata.len(),
                            "modified": metadata.modified().unwrap().duration_since(std::time::UNIX_EPOCH).unwrap().as_secs()
                        }));
                        index += 1;
                    }
                }
            }
        }
    }

    notes.sort_by(|a, b| {
        b["modified"].as_u64().cmp(&a["modified"].as_u64())
    });

    // 重新编号（按时间排序后）
    for (i, note) in notes.iter_mut().enumerate() {
        note["id"] = serde_json::json!(i + 1);
    }

    Ok(notes)
}

#[tauri::command]
fn read_note(path: String) -> Result<String, String> {
    use std::fs;
    fs::read_to_string(&path)
        .map_err(|e| format!("读取失败: {}", e))
}

#[tauri::command]
fn delete_note(path: String) -> Result<(), String> {
    use std::fs;

    // 提取文件名用于日志
    let note_name = Path::new(&path)
        .file_name()
        .map(|n| n.to_string_lossy().to_string())
        .unwrap_or_default();

    // 记录删除日志
    log_deletion(&note_name);

    // 删除文件
    fs::remove_file(&path)
        .map_err(|e| format!("删除失败: {}", e))
}

// 简单的 HTTP 服务器来托管前端
fn start_frontend_server() {
    thread::spawn(|| {
        let ui_dir = "/Users/jszpc/Desktop/快捷总结笔记/ui";
        let listener = TcpListener::bind("127.0.0.1:8080").unwrap();

        println!("前端服务器启动: http://localhost:8080");

        for stream_result in listener.incoming() {
            let mut stream = match stream_result {
                Ok(s) => s,
                Err(_) => continue,
            };
            let mut buffer = [0u8; 2048];

            let bytes_read = match stream.read(&mut buffer) {
                Ok(n) => n,
                Err(_) => continue,
            };

            let request = String::from_utf8_lossy(&buffer[..bytes_read]);

            // 解析请求路径
            let request_line = request.lines().next().unwrap_or("");
            let path = if request_line.starts_with("GET /") {
                let parts: Vec<&str> = request_line.split_whitespace().collect();
                if parts.len() >= 2 {
                    let p = parts[1];
                    if p == "/" || p.is_empty() {
                        "/index.html"
                    } else {
                        p
                    }
                } else {
                    "/index.html"
                }
            } else {
                continue;
            };

            // 构建文件路径
            let file_path = if path == "/index.html" {
                format!("{}/index.html", ui_dir)
            } else {
                format!("{}{}", ui_dir, path)
            };

            // 读取文件并响应
            if let Ok(contents) = std::fs::read(&file_path) {
                let content_type = if path.ends_with(".html") {
                    "text/html"
                } else if path.ends_with(".css") {
                    "text/css"
                } else if path.ends_with(".js") {
                    "application/javascript"
                } else {
                    "text/plain"
                };

                let response = format!(
                    "HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n",
                    content_type,
                    contents.len()
                );

                let _ = stream.write_all(response.as_bytes());
                let _ = stream.write_all(&contents);
            } else {
                let response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n";
                let _ = stream.write_all(response.as_bytes());
            }
        }
    });
}

// 解析快捷键字符串为 Tauri 快捷键
fn parse_shortcut(hotkey: &str) -> (Option<tauri_plugin_global_shortcut::Modifiers>, tauri_plugin_global_shortcut::Code) {
    use tauri_plugin_global_shortcut::{Code, Modifiers};

    let hotkey_lower = hotkey.to_lowercase();

    // 解析修饰键
    let mut modifiers = Modifiers::empty();
    if hotkey_lower.contains("ctrl") || hotkey_lower.contains("control") {
        modifiers = modifiers | Modifiers::CONTROL;
    }
    if hotkey_lower.contains("shift") {
        modifiers = modifiers | Modifiers::SHIFT;
    }
    if hotkey_lower.contains("alt") {
        modifiers = modifiers | Modifiers::ALT;
    }
    if hotkey_lower.contains("cmd") || hotkey_lower.contains("command") {
        modifiers = modifiers | Modifiers::META;
    }

    // 解析按键
    let key_code = if hotkey_lower.contains("f1") {
        Code::F1
    } else if hotkey_lower.contains("f2") {
        Code::F2
    } else if hotkey_lower.contains("f3") {
        Code::F3
    } else if hotkey_lower.contains("f4") {
        Code::F4
    } else if hotkey_lower.contains("f5") {
        Code::F5
    } else if hotkey_lower.contains("f6") {
        Code::F6
    } else if hotkey_lower.contains("f7") {
        Code::F7
    } else if hotkey_lower.contains("f8") {
        Code::F8
    } else if hotkey_lower.contains("f9") {
        Code::F9
    } else if hotkey_lower.contains("f10") {
        Code::F10
    } else if hotkey_lower.contains("f11") {
        Code::F11
    } else if hotkey_lower.contains("f12") {
        Code::F12
    } else if hotkey_lower.contains("s") {
        Code::KeyS
    } else if hotkey_lower.contains("a") {
        Code::KeyA
    } else if hotkey_lower.contains("c") {
        Code::KeyC
    } else if hotkey_lower.contains("v") {
        Code::KeyV
    } else if hotkey_lower.contains("n") {
        Code::KeyN
    } else {
        Code::F2  // 默认 F2
    };

    (Some(modifiers), key_code)
}

fn main() {
    let base_dir = "/Users/jszpc/Desktop/快捷总结笔记";

    // 获取配置的快捷键
    let configured_hotkey = get_configured_hotkey();
    println!("配置的快捷键: {}", configured_hotkey);

    // 解析快捷键
    let (modifiers, key_code) = parse_shortcut(&configured_hotkey);

    // 检查并启动 API 服务器
    let check = Command::new("curl")
        .arg("-s")
        .arg("http://localhost:5000/api/notes")
        .output();

    if check.is_err() || !check.unwrap().status.success() {
        let _child = Command::new("python3")
            .arg("api_server.py")
            .current_dir(base_dir)
            .spawn();
        std::thread::sleep(std::time::Duration::from_secs(3));
    }

    // 启动前端 HTTP 服务器
    start_frontend_server();

    // 等待前端服务器启动
    std::thread::sleep(std::time::Duration::from_millis(500));

    // 保存快捷键信息供 setup 使用
    let hotkey_for_setup = configured_hotkey.clone();

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_clipboard_manager::init())
        .setup(move |app| {
            // 注册全局快捷键（从配置读取）
            use tauri_plugin_global_shortcut::{GlobalShortcutExt, Shortcut, Code, Modifiers};

            let (mods, key) = parse_shortcut(&hotkey_for_setup);
            let shortcut = Shortcut::new(mods, key);

            println!("注册全局快捷键: {}", hotkey_for_setup);

            let app_handle = app.handle().clone();
            app.global_shortcut().on_shortcut(shortcut, move |_app, _shortcut, _event| {
                println!("全局快捷键触发！");

                // 1. 先激活前台窗口（模拟按键切换到前台）
                let _ = Command::new("osascript")
                    .arg("-e")
                    .arg("tell application \"System Events\" to keystroke \"a\" using command down")
                    .output();

                // 等待一小段时间让选中完成
                std::thread::sleep(std::time::Duration::from_millis(100));

                // 2. 复制选中内容
                let _ = Command::new("osascript")
                    .arg("-e")
                    .arg("tell application \"System Events\" to keystroke \"c\" using command down")
                    .output();

                // 等待复制完成
                std::thread::sleep(std::time::Duration::from_millis(200));

                // 3. 执行总结
                let output = Command::new("python3")
                    .arg("src/main.py")
                    .arg("--once")
                    .current_dir("/Users/jszpc/Desktop/快捷总结笔记")
                    .output();

                match output {
                    Ok(result) => {
                        if result.status.success() {
                            println!("总结成功: {}", String::from_utf8_lossy(&result.stdout));
                            // 显示通知
                            let _ = app_handle.emit("summary-done", "总结完成！");
                        } else {
                            println!("总结失败: {}", String::from_utf8_lossy(&result.stderr));
                        }
                    }
                    Err(e) => {
                        println!("执行失败: {}", e);
                    }
                }
            }).unwrap();

            if let Some(window) = app.get_webview_window("main") {
                let _ = window.eval("window.location.href = 'http://localhost:8080'");
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            summarize_once,
            get_notes_list,
            read_note,
            delete_note,
            get_notes_dir,
            start_api_server
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}