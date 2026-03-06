package main

import (
	"flag"
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/LEEI1337/phantom-neural-cortex/kommandozentrale/internal/config"
	"github.com/LEEI1337/phantom-neural-cortex/kommandozentrale/internal/tui"
)

func main() {
	configPath := flag.String("config", "config.yaml", "Path to TUI config")
	pncURL := flag.String("pnc", "http://localhost:18789", "PNC Gateway URL")
	flag.Parse()

	cfg, err := config.Load(*configPath)
	if err != nil {
		// Use defaults if no config file
		cfg = &config.Config{
			PNCURL:       *pncURL,
			RefreshMs:    2000,
			MaxLogLines:  500,
			KillshortCut: "ctrl+k",
		}
	}

	// Override PNC URL from flag if provided
	if *pncURL != "http://localhost:18789" {
		cfg.PNCURL = *pncURL
	}

	app := tui.NewApp(cfg)
	p := tea.NewProgram(app, tea.WithAltScreen())

	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
