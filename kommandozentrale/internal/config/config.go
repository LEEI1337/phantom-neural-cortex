package config

import (
	"os"

	"gopkg.in/yaml.v3"
)

// Config holds TUI configuration
type Config struct {
	PNCURL       string `yaml:"pnc_url"`
	RefreshMs    int    `yaml:"refresh_ms"`
	MaxLogLines  int    `yaml:"max_log_lines"`
	KillshortCut string `yaml:"kill_shortcut"`
}

// Load reads config from YAML file
func Load(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	cfg := &Config{
		PNCURL:       "http://localhost:18789",
		RefreshMs:    2000,
		MaxLogLines:  500,
		KillshortCut: "ctrl+k",
	}

	if err := yaml.Unmarshal(data, cfg); err != nil {
		return nil, err
	}

	return cfg, nil
}
