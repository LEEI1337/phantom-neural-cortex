package client

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

// PNCClient communicates with the PNC Gateway API
type PNCClient struct {
	BaseURL    string
	HTTPClient *http.Client
}

// AgentInfo represents an agent's status
type AgentInfo struct {
	Name      string `json:"name"`
	Role      string `json:"role"`
	Killed    bool   `json:"killed"`
	TaskCount int    `json:"task_count"`
}

// AgentsResponse from /agents endpoint
type AgentsResponse struct {
	Agents map[string]AgentInfo `json:"agents"`
}

// HealthResponse from /health endpoint
type HealthResponse struct {
	Status     string            `json:"status"`
	Components map[string]string `json:"components"`
}

// NewPNCClient creates a new PNC Gateway client
func NewPNCClient(baseURL string) *PNCClient {
	return &PNCClient{
		BaseURL: strings.TrimRight(baseURL, "/"),
		HTTPClient: &http.Client{
			Timeout: 10 * time.Second,
		},
	}
}

// GetHealth checks gateway health
func (c *PNCClient) GetHealth() (*HealthResponse, error) {
	resp, err := c.HTTPClient.Get(c.BaseURL + "/health")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var health HealthResponse
	if err := json.NewDecoder(resp.Body).Decode(&health); err != nil {
		return nil, err
	}
	return &health, nil
}

// GetAgents lists all registered agents
func (c *PNCClient) GetAgents() (*AgentsResponse, error) {
	resp, err := c.HTTPClient.Get(c.BaseURL + "/agents")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var agents AgentsResponse
	if err := json.NewDecoder(resp.Body).Decode(&agents); err != nil {
		return nil, err
	}
	return &agents, nil
}

// KillAgent sends a killswitch signal to an agent
func (c *PNCClient) KillAgent(agentName, triggeredBy string) error {
	payload := fmt.Sprintf(`{"triggered_by":"%s","details":"via TUI Ctrl+K"}`, triggeredBy)
	url := fmt.Sprintf("%s/killswitch/agent/%s/kill", c.BaseURL, agentName)

	req, err := http.NewRequest("POST", url, strings.NewReader(payload))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("kill failed (%d): %s", resp.StatusCode, string(body))
	}
	return nil
}

// ReviveAgent revives a killed agent
func (c *PNCClient) ReviveAgent(agentName, authorizedBy string) error {
	payload := fmt.Sprintf(`{"triggered_by":"%s"}`, authorizedBy)
	url := fmt.Sprintf("%s/killswitch/agent/%s/revive", c.BaseURL, agentName)

	req, err := http.NewRequest("POST", url, strings.NewReader(payload))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("revive failed (%d): %s", resp.StatusCode, string(body))
	}
	return nil
}
