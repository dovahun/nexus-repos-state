package main

import (
	"encoding/json"
	"flag"
	"github.com/tidwall/gjson"
	"log"
	"log/slog"
	"nexus-repo-states/src"
	"os"
	"slices"
)

func main() {

	flagNexusUrl := flag.String("url", "http://127.0.0.1:8081/service/rest/v1/", "Set nexus url with base api path and version /v1/")
	flagNexusUser := flag.String("username", "", "Set nexus user for basic auth")
	flagNexusUserPassword := flag.String("password", "", "Set password from user for basic auth")
	flagNexusPathToConfigs := flag.String("configs", "", "Set path to dir with all json configs")
	flag.Parse()

	nexusUrl := *flagNexusUrl
	nexusUser := *flagNexusUser
	nexusUserPassword := *flagNexusUserPassword
	nexusPathToConfigs := *flagNexusPathToConfigs

	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))

	files, err := src.ReadAllFiles(nexusPathToConfigs)
	if err != nil {
		logger.Error("Error:", err)
		return
	}

	reposFromNexus := src.GetRequest(nexusUrl, "repositories", nexusUser, nexusUserPassword)
	var repos []map[string]any
	if err := json.Unmarshal([]byte(reposFromNexus), &repos); err != nil {
		log.Fatal(err)
	}

	listReposFromNexus := make([]string, 0, len(repos))
	for _, repo := range repos {
		if name, ok := repo["name"].(string); ok {
			listReposFromNexus = append(listReposFromNexus, name)
		}
	}

	for path, content := range files {
		logger.Info("Reading file: " + path)
		requestPath := gjson.Get(string(content), "RequestPath").String()
		requestBody := gjson.Get(string(content), "RequestBody").String()
		nameRepo := gjson.Get(string(content), "RequestBody.name").String()
		if slices.Contains(listReposFromNexus, nameRepo) {
			src.PutRequest(nexusUrl, nameRepo, requestPath, requestBody, nexusUser, nexusUserPassword)
		} else {
			src.PostRequest(nexusUrl, requestPath, requestBody, nexusUser, nexusUserPassword)
		}

	}

}
