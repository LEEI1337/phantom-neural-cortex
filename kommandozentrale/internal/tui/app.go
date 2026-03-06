package tui

import (
	"fmt"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/LEEI1337/phantom-neural-cortex/kommandozentrale/internal/client"
	"github.com/LEEI1337/phantom-neural-cortex/kommandozentrale/internal/config"
)

// Styles
var (
	titleStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color("#7D56F4")).
			PaddingLeft(1)

	statusOK = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#04B575"))

	statusKilled = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FF0000")).
			Bold(true)

	statusOffline = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#888888"))

	headerStyle = lipgloss.NewStyle().
			BorderStyle(lipgloss.NormalBorder()).
			BorderBottom(true).
			Bold(true)

	helpStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#888888"))
)

// Messages
type tickMsg time.Time
type agentsMsg struct {
	agents map[string]client.AgentInfo
	err    error
}
type healthMsg struct {
	healthy bool
	err     error
}
type killResultMsg struct {
	agent string
	err   error
}

// App is the main TUI model
type App struct {
	cfg       *config.Config
	pnc       *client.PNCClient
	agents    map[string]client.AgentInfo
	healthy   bool
	logs      []string
	viewport  viewport.Model
	width     int
	height    int
	selected  int
	agentKeys []string
	err       error
}

// NewApp creates a new TUI application
func NewApp(cfg *config.Config) *App {
	return &App{
		cfg:    cfg,
		pnc:    client.NewPNCClient(cfg.PNCURL),
		agents: make(map[string]client.AgentInfo),
		logs:   make([]string, 0),
	}
}

func (a *App) Init() tea.Cmd {
	return tea.Batch(
		tick(a.cfg.RefreshMs),
		fetchAgents(a.pnc),
		fetchHealth(a.pnc),
	)
}

func (a *App) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		a.width = msg.Width
		a.height = msg.Height

	case tea.KeyMsg:
		switch msg.String() {
		case "q", "esc":
			return a, tea.Quit
		case "ctrl+k":
			// Killswitch — kill selected agent
			if len(a.agentKeys) > 0 && a.selected < len(a.agentKeys) {
				name := a.agentKeys[a.selected]
				a.addLog(fmt.Sprintf("KILLSWITCH activated for %s", name))
				return a, killAgent(a.pnc, name)
			}
		case "r":
			// Revive selected agent
			if len(a.agentKeys) > 0 && a.selected < len(a.agentKeys) {
				name := a.agentKeys[a.selected]
				a.addLog(fmt.Sprintf("Reviving agent %s...", name))
				return a, reviveAgent(a.pnc, name)
			}
		case "up", "k":
			if a.selected > 0 {
				a.selected--
			}
		case "down", "j":
			if a.selected < len(a.agentKeys)-1 {
				a.selected++
			}
		}

	case tickMsg:
		return a, tea.Batch(
			tick(a.cfg.RefreshMs),
			fetchAgents(a.pnc),
			fetchHealth(a.pnc),
		)

	case agentsMsg:
		if msg.err != nil {
			a.err = msg.err
		} else {
			a.agents = msg.agents
			a.agentKeys = make([]string, 0, len(msg.agents))
			for k := range msg.agents {
				a.agentKeys = append(a.agentKeys, k)
			}
			a.err = nil
		}

	case healthMsg:
		a.healthy = msg.healthy
		if msg.err != nil {
			a.healthy = false
		}

	case killResultMsg:
		if msg.err != nil {
			a.addLog(fmt.Sprintf("Kill failed for %s: %v", msg.agent, msg.err))
		} else {
			a.addLog(fmt.Sprintf("Agent %s KILLED successfully", msg.agent))
		}
	}

	return a, nil
}

func (a *App) View() string {
	if a.width == 0 {
		return "Loading..."
	}

	var b strings.Builder

	// Header
	header := titleStyle.Render("PHANTOM AGENT SYSTEM — Kommandozentrale")
	gwStatus := statusOK.Render("ONLINE")
	if !a.healthy {
		gwStatus = statusOffline.Render("OFFLINE")
	}
	b.WriteString(fmt.Sprintf("%s  Gateway: %s\n", header, gwStatus))
	b.WriteString(headerStyle.Render(strings.Repeat("─", min(a.width, 70))) + "\n\n")

	// Agent List
	b.WriteString("  AGENTS\n")
	if len(a.agentKeys) == 0 {
		if a.err != nil {
			b.WriteString(fmt.Sprintf("  Error: %v\n", a.err))
		} else {
			b.WriteString("  No agents registered.\n")
		}
	} else {
		for i, key := range a.agentKeys {
			agent := a.agents[key]
			cursor := "  "
			if i == a.selected {
				cursor = "> "
			}

			status := statusOK.Render("ALIVE")
			if agent.Killed {
				status = statusKilled.Render("KILLED")
			}

			line := fmt.Sprintf("%s%-12s %-30s %s  Tasks: %d",
				cursor, agent.Name, agent.Role, status, agent.TaskCount)
			b.WriteString(line + "\n")
		}
	}

	// Logs
	b.WriteString("\n" + headerStyle.Render(strings.Repeat("─", min(a.width, 70))) + "\n")
	b.WriteString("  LOGS\n")
	logStart := 0
	maxLogs := 10
	if len(a.logs) > maxLogs {
		logStart = len(a.logs) - maxLogs
	}
	for _, log := range a.logs[logStart:] {
		b.WriteString("  " + log + "\n")
	}

	// Help
	b.WriteString("\n")
	b.WriteString(helpStyle.Render("  Ctrl+K: Kill  |  r: Revive  |  j/k: Navigate  |  q: Quit"))
	b.WriteString("\n")

	return b.String()
}

func (a *App) addLog(msg string) {
	ts := time.Now().Format("15:04:05")
	a.logs = append(a.logs, fmt.Sprintf("[%s] %s", ts, msg))
	if len(a.logs) > a.cfg.MaxLogLines {
		a.logs = a.logs[len(a.logs)-a.cfg.MaxLogLines:]
	}
}

// Commands

func tick(ms int) tea.Cmd {
	return tea.Tick(time.Duration(ms)*time.Millisecond, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

func fetchAgents(pnc *client.PNCClient) tea.Cmd {
	return func() tea.Msg {
		resp, err := pnc.GetAgents()
		if err != nil {
			return agentsMsg{err: err}
		}
		return agentsMsg{agents: resp.Agents}
	}
}

func fetchHealth(pnc *client.PNCClient) tea.Cmd {
	return func() tea.Msg {
		health, err := pnc.GetHealth()
		if err != nil {
			return healthMsg{err: err}
		}
		return healthMsg{healthy: health.Status == "healthy" || health.Status == "ok"}
	}
}

func killAgent(pnc *client.PNCClient, name string) tea.Cmd {
	return func() tea.Msg {
		err := pnc.KillAgent(name, "joe")
		return killResultMsg{agent: name, err: err}
	}
}

func reviveAgent(pnc *client.PNCClient, name string) tea.Cmd {
	return func() tea.Msg {
		err := pnc.ReviveAgent(name, "joe")
		if err != nil {
			return killResultMsg{agent: name, err: err}
		}
		return killResultMsg{agent: name, err: nil}
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
